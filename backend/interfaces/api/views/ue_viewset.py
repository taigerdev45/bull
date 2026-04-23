from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from interfaces.api.serializers.ue_serializer import UESerializer, MatiereSerializer

from rest_framework.permissions import AllowAny

@extend_schema(tags=['Académique'])
class UEViewSet(viewsets.ViewSet):
    """ViewSet pour les Unités d'Enseignement (UE)."""
    permission_classes = [AllowAny]
    
    @inject
    def __init__(self, ue_repo=Provide[Container.ue_repo], matiere_repo=Provide[Container.matiere_repo], **kwargs):
        super().__init__(**kwargs)
        self.ue_repo = ue_repo
        self.matiere_repo = matiere_repo

    def list(self, request):
        ues = self.ue_repo.list_all()
        # Enrichir avec les matières
        for ue in ues:
            ue.matieres = self.matiere_repo.get_by_ue(ue.code)
        serializer = UESerializer(ues, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        ue = self.ue_repo.get_by_id(pk)
        if not ue:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ue.matieres = self.matiere_repo.get_by_ue(ue.code)
        serializer = UESerializer(ue)
        return Response(serializer.data)

    def create(self, request):
        serializer = UESerializer(data=request.data)
        if serializer.is_valid():
            from domain.entities.ue import UE
            ue = UE(
                code=serializer.validated_data['code'],
                libelle=serializer.validated_data['libelle'],
                credits=serializer.validated_data['credits'],
                semestre_id=serializer.validated_data['semestre_id']
            )
            try:
                self.ue_repo.save(ue)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        ue = self.ue_repo.get_by_id(pk)
        if not ue:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = UESerializer(data=request.data)
        if serializer.is_valid():
            ue._code = serializer.validated_data['code']
            ue._libelle = serializer.validated_data['libelle']
            ue._credits = serializer.validated_data['credits']
            ue._semestre_id = serializer.validated_data['semestre_id']
            self.ue_repo.save(ue)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.ue_repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='semestre/(?P<semestre>[^/.]+)')
    def semestre(self, request, semestre=None):
        """Filtre les UEs par semestre."""
        try:
            s_val = int(semestre)
            ues = self.ue_repo.get_by_semestre(s_val)
            for ue in ues:
                ue.matieres = self.matiere_repo.get_by_ue(ue.code)
            serializer = UESerializer(ues, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({"error": "Semestre invalide"}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Académique'])
class MatiereViewSet(viewsets.ViewSet):
    """ViewSet pour les Matières."""
    permission_classes = [AllowAny]

    @inject
    def __init__(self, matiere_repo=Provide[Container.matiere_repo], **kwargs):
        super().__init__(**kwargs)
        self.matiere_repo = matiere_repo

    def list(self, request):
        matieres = self.matiere_repo.list_all()
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        matiere = self.matiere_repo.get_by_id(pk)
        if not matiere:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MatiereSerializer(matiere)
        return Response(serializer.data)

    def create(self, request):
        serializer = MatiereSerializer(data=request.data)
        if serializer.is_valid():
            from domain.entities.matiere import Matiere
            from domain.value_objects.coefficient import Coefficient
            matiere = Matiere(
                libelle=serializer.validated_data['libelle'],
                coefficient=Coefficient(serializer.validated_data['coefficient']),
                credits=serializer.validated_data['credits'],
                ue_id=serializer.validated_data['ue_id'],
                enseignant_id=serializer.validated_data.get('enseignant_id')
            )
            try:
                self.matiere_repo.save(matiere)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        matiere = self.matiere_repo.get_by_id(pk)
        if not matiere:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = MatiereSerializer(data=request.data)
        if serializer.is_valid():
            from domain.value_objects.coefficient import Coefficient
            matiere._libelle = serializer.validated_data['libelle']
            matiere._coefficient = Coefficient(serializer.validated_data['coefficient'])
            matiere._credits = serializer.validated_data['credits']
            matiere._ue_id = serializer.validated_data['ue_id']
            matiere._enseignant_id = serializer.validated_data.get('enseignant_id')
            self.matiere_repo.save(matiere)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.matiere_repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='ue/(?P<ue_id>[^/.]+)')
    def ue(self, request, ue_id=None):
        """Filtre les matières par UE."""
        matieres = self.matiere_repo.get_by_ue(ue_id)
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='enseignant/(?P<teacher_id>[^/.]+)')
    def enseignant(self, request, teacher_id=None):
        """Filtre les matières par enseignant."""
        matieres = self.matiere_repo.get_by_enseignant(teacher_id)
        serializer = MatiereSerializer(matieres, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='attribuer_enseignant')
    def attribuer_enseignant(self, request, pk=None):
        """Assigne un enseignant à une matière."""
        enseignant_id = request.data.get('enseignant_id')
        if not enseignant_id:
            return Response({"error": "enseignant_id requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        # On pourrait vérifier si la matière existe ici
        self.matiere_repo.attribuer_enseignant(pk, enseignant_id)
        return Response({"status": "enseignant attribué"})
