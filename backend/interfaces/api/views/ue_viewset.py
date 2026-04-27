from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from interfaces.api.serializers.ue_serializer import UESerializer, MatiereSerializer
from interfaces.api.permissions.role_permissions import IsAdmin, IsSecretariat

def ue_to_dict(ue, matieres=None):
    """Convertit une entité UE en dict JSON-serializable."""
    return {
        "id": ue.id,
        "code": ue.code,
        "libelle": ue.libelle,
        "credits": ue.credits,
        "semestre_id": ue._semestre_id,
        "matieres": [matiere_to_dict(m) for m in (matieres or [])],
    }

def matiere_to_dict(m):
    """Convertit une entité Matiere en dict JSON-serializable."""
    return {
        "id": m.id,
        "libelle": m.libelle,
        "coefficient": m.coefficient,
        "credits": m.credits,
        "ue_id": m._ue_id,
        "enseignant_id": m.enseignant_id,
    }

@extend_schema(tags=['Académique'])
class UEViewSet(viewsets.ViewSet):
    """ViewSet pour les Unités d'Enseignement (UE)."""
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSecretariat()]
        return [permissions.IsAuthenticated()]

    @inject
    def __init__(self, ue_repo=Provide[Container.ue_repo], matiere_repo=Provide[Container.matiere_repo], **kwargs):
        super().__init__(**kwargs)
        self.ue_repo = ue_repo
        self.matiere_repo = matiere_repo

    def list(self, request):
        try:
            role = getattr(request.user, 'role', 'etudiant')
            is_staff = role in ['admin', 'super_admin', 'secretariat']
            
            ues = self.ue_repo.list_all()
            
            # Si c'est un enseignant, on pré-charge ses matières pour éviter le N+1
            mes_matieres_all = []
            if not is_staff and role == 'enseignant':
                uid = getattr(request.user, 'uid', request.user.username)
                mes_matieres_all = self.matiere_repo.get_by_enseignant(uid)
            
            result = []
            for ue in ues:
                matieres = self.matiere_repo.get_by_ue(ue.id)
                
                # Filtrage pour enseignant
                if not is_staff and role == 'enseignant':
                    # On filtre les matières de cet UE parmi celles de l'enseignant
                    matieres = [m for m in mes_matieres_all if m._ue_id == ue.id]
                    if not matieres:
                        continue
                
                result.append(ue_to_dict(ue, matieres))
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            ue = self.ue_repo.get_by_id(pk)
            if not ue:
                return Response(status=status.HTTP_404_NOT_FOUND)
            matieres = self.matiere_repo.get_by_ue(ue.id)
            return Response(ue_to_dict(ue, matieres))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                return Response(ue_to_dict(ue), status=status.HTTP_201_CREATED)
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
            try:
                self.ue_repo.save(ue)
                return Response(ue_to_dict(ue))
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        try:
            self.ue_repo.delete(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='semestre/(?P<semestre>[^/.]+)')
    def semestre(self, request, semestre=None):
        """Filtre les UEs par semestre."""
        try:
            s_val = int(semestre)
            ues = self.ue_repo.get_by_semestre(s_val)
            result = [ue_to_dict(ue, self.matiere_repo.get_by_ue(ue.id)) for ue in ues]
            return Response(result)
        except ValueError:
            return Response({"error": "Semestre invalide"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(tags=['Académique'])
class MatiereViewSet(viewsets.ViewSet):
    """ViewSet pour les Matières."""
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'attribuer_enseignant']:
            return [IsSecretariat()]
        return [permissions.IsAuthenticated()]

    @inject
    def __init__(self, 
                 matiere_repo=Provide[Container.matiere_repo], 
                 audit_service=Provide[Container.audit_service],
                 **kwargs):
        super().__init__(**kwargs)
        self.matiere_repo = matiere_repo
        self.audit_service = audit_service

    def list(self, request):
        try:
            is_staff = getattr(request.user, 'is_staff', False)
            role = getattr(request.user, 'role', 'etudiant')
            
            # Si c'est un enseignant, on ne renvoie que ses matières
            if role == 'enseignant' and not is_staff:
                matieres = self.matiere_repo.get_by_enseignant(request.user.username)
            else:
                matieres = self.matiere_repo.list_all()
                
            return Response([matiere_to_dict(m) for m in matieres])
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            matiere = self.matiere_repo.get_by_id(pk)
            if not matiere:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(matiere_to_dict(matiere))
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                return Response(matiere_to_dict(matiere), status=status.HTTP_201_CREATED)
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
            try:
                self.matiere_repo.save(matiere)
                return Response(matiere_to_dict(matiere))
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        try:
            self.matiere_repo.delete(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='ue/(?P<ue_id>[^/.]+)')
    def ue(self, request, ue_id=None):
        """Filtre les matières par UE."""
        matieres = self.matiere_repo.get_by_ue(ue_id)
        return Response([matiere_to_dict(m) for m in matieres])

    @action(detail=False, methods=['get'], url_path='enseignant/(?P<teacher_id>[^/.]+)')
    def enseignant(self, request, teacher_id=None):
        """Filtre les matières par enseignant."""
        matieres = self.matiere_repo.get_by_enseignant(teacher_id)
        return Response([matiere_to_dict(m) for m in matieres])

    @action(detail=True, methods=['patch'], url_path='attribuer_enseignant')
    def attribuer_enseignant(self, request, pk=None):
        """Assigne un enseignant à une matière."""
        enseignant_id = request.data.get('enseignant_id')
        if not enseignant_id:
            return Response({"error": "enseignant_id requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        matiere = self.matiere_repo.get_by_id(pk)
        if not matiere:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        self.matiere_repo.attribuer_enseignant(pk, enseignant_id)
        
        # Notification à l'enseignant
        try:
            enseignant_repo = Container.enseignant_repo()
            notification_repo = Container.notification_repo()
            enseignant = enseignant_repo.get_by_id(enseignant_id)
            if enseignant and enseignant.user_id:
                from domain.entities.notification import Notification
                notif = Notification(
                    destinataire_uid=enseignant.user_id,
                    titre="Nouvelle matière assignée",
                    message=f"La matière '{matiere.libelle}' vous a été attribuée.",
                    type="INFO"
                )
                notification_repo.save(notif)
        except Exception as e:
            print(f"[NOTIF ERROR] {str(e)}")

        # Traçabilité (Notification système)
        self.audit_service.logger_action({
            "action_type": "USER_MGMT",
            "user_name": request.user.username,
            "target_id": pk,
            "details": f"Attribution de la matière '{matiere.libelle}' à l'enseignant {enseignant_id}",
            "status": "SUCCESS"
        })
        
        return Response({"status": "enseignant attribué"})
