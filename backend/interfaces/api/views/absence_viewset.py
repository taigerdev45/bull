from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from interfaces.api.permissions.role_permissions import IsAdmin, IsSecretariat, IsEtudiant
from interfaces.api.serializers.absence_serializer import AbsenceSerializer
from application.commands.creer_absence_command import CreerAbsenceCommand, CreerAbsenceHandler
from infrastructure.config.dependency_injection import Container
from dependency_injector.wiring import inject, Provide

@extend_schema(tags=['Absences'])
class AbsenceViewSet(viewsets.ViewSet):
    """
    API pour la gestion des absences.
    Saisie : Secrétariat/Admin
    Consultation : Admin/Secrétariat/Étudiant (ses propres données)
    """

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            return [IsSecretariat()]
        return [permissions.IsAuthenticated()]

    @inject
    def create(self, request, handler: CreerAbsenceHandler = Provide[Container.creer_absence_handler]):
        serializer = AbsenceSerializer(data=request.data)
        if serializer.is_valid():
            # Utiliser username comme fallback si request.user.id est manquant (Firebase UID)
            user_id = getattr(request.user, 'username', 'system')
            command = CreerAbsenceCommand(
                etudiant_id=serializer.validated_data['etudiant_id'],
                matiere_id=serializer.validated_data['matiere_id'],
                nombre_heures=serializer.validated_data['nombre_heures'],
                date_absence=serializer.validated_data['date_absence'],
                saisie_par_id=user_id
            )
            absence_id = handler.handle(command)
            return Response({'id': absence_id, 'status': 'created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @inject
    def list(self, request, repo=Provide[Container.absence_repo]):
        # On récupère le rôle de l'utilisateur
        auth = request.auth if isinstance(request.auth, dict) else {}
        role = (auth.get('role') or getattr(request.user, 'role', 'etudiant')).lower()
        uid = request.user.username  # UID Firebase stocké dans username
        
        if role == 'etudiant':
            absences = repo.obtenir_par_etudiant(uid)
        else:
            # Pour le staff, on peut filtrer par etudiant_id si présent, sinon tout renvoyer
            etudiant_id = request.query_params.get('etudiant_id')
            if etudiant_id:
                absences = repo.obtenir_par_etudiant(etudiant_id)
            else:
                absences = repo.obtenir_tout() if hasattr(repo, 'obtenir_tout') else []
        
        serializer = AbsenceSerializer([a.to_dict() for a in absences], many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='etudiant/(?P<etudiant_id>[^/.]+)')
    @inject
    def par_etudiant(self, request, etudiant_id=None, repo=Provide[Container.absence_repo]):
        claims = getattr(request.user, 'firebase_claims', {})
        role = claims.get('role')
        uid = getattr(request.user, 'username', None)
        
        if role == 'etudiant' and uid != etudiant_id:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
            
        absences = repo.obtenir_par_etudiant(etudiant_id)
        serializer = AbsenceSerializer([a.to_dict() for a in absences], many=True)
        return Response(serializer.data)

    @inject
    def update(self, request, pk=None, repo=Provide[Container.absence_repo]):
        absence = repo.get_by_id(pk)
        if not absence:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = AbsenceSerializer(data=request.data)
        if serializer.is_valid():
            absence._etudiant_id = serializer.validated_data['etudiant_id']
            absence._matiere_id = serializer.validated_data['matiere_id']
            absence._nombre_heures = serializer.validated_data['nombre_heures']
            absence._date_absence = serializer.validated_data['date_absence']
            repo.save(absence)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @inject
    def destroy(self, request, pk=None, repo=Provide[Container.absence_repo]):
        repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
