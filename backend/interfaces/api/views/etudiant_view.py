from rest_framework import viewsets, status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from interfaces.api.serializers.etudiant_serializer import EtudiantSerializer
from interfaces.api.serializers.evaluation_serializer import EvaluationSerializer
from interfaces.api.permissions.role_permissions import IsSecretariat, IsEnseignant
from infrastructure.config.dependency_injection import Container

@extend_schema(tags=['Étudiants'])
class EtudiantViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion CRUD des étudiants via le repository."""
    permission_classes = [IsSecretariat]

    def list(self, request):
        repo = Container.etudiant_repo()
        etudiants = repo.list_all()
        serializer = EtudiantSerializer(etudiants, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = EtudiantSerializer(data=request.data)
        if serializer.is_valid():
            from domain.entities.etudiant import Etudiant
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            auth_service = Container.auth_service()
            repo = Container.etudiant_repo()
            
            try:
                # Création Firebase
                display_name = f"{serializer.validated_data['prenom']} {serializer.validated_data['nom']}"
                user_id = auth_service.create_user(
                    email=email,
                    password=password,
                    display_name=display_name
                )
                auth_service.set_user_claims(user_id, 'etudiant')
                
                etudiant = Etudiant(
                    nom=serializer.validated_data['nom'],
                    prenom=serializer.validated_data['prenom'],
                    matricule=serializer.validated_data['matricule'],
                    email=email,
                    user_id=user_id,
                    date_naissance=serializer.validated_data['date_naissance'],
                    lieu_naissance=serializer.validated_data.get('lieu_naissance'),
                    bac=serializer.validated_data.get('bac'),
                    provenance=serializer.validated_data.get('provenance')
                )
                
                repo.save(etudiant)
                
                return_data = serializer.data
                return_data.pop('password', None)
                return Response(return_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        repo = Container.etudiant_repo()
        etudiant = repo.get_by_id(pk)
        if not etudiant:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = EtudiantSerializer(data=request.data)
        if serializer.is_valid():
            etudiant._nom = serializer.validated_data['nom']
            etudiant._prenom = serializer.validated_data['prenom']
            etudiant._matricule = serializer.validated_data['matricule']
            etudiant._date_naissance = serializer.validated_data['date_naissance']
            etudiant._lieu_naissance = serializer.validated_data.get('lieu_naissance')
            etudiant._bac = serializer.validated_data.get('bac')
            etudiant._provenance = serializer.validated_data.get('provenance')
            repo.save(etudiant)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        repo = Container.etudiant_repo()
        repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(tags=['Évaluations'])
class EvaluationView(views.APIView):
    """Vue pour la saisie de notes déclenchant les commandes applicatives."""
    permission_classes = [IsEnseignant]

    def post(self, request):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            service = Container.evaluation_service()
            try:
                eval_id = service.saisir_note(
                    etudiant_id=serializer.validated_data['etudiant_id'],
                    matiere_id=serializer.validated_data['matiere_id'],
                    type_eval=serializer.validated_data['type'],
                    note=serializer.validated_data['note']
                )
                return Response({'id': eval_id, 'status': 'Calculé'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
