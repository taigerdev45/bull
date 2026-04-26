from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from rest_framework import serializers
from interfaces.api.permissions.role_permissions import IsAdmin, IsSecretariat

class EnseignantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    matricule = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)

@extend_schema(tags=['Administration'])
class EnseignantViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion des Enseignants."""
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'assign_matieres']:
            return [IsSecretariat()]
        return [permissions.IsAuthenticated()]

    @inject
    def __init__(self, repo=Provide[Container.enseignant_repo], **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def list(self, request):
        try:
            role = getattr(request.user, 'role', 'etudiant')
            
            if role == 'etudiant':
                return Response({"error": "Accès refusé"}, status=status.HTTP_403_FORBIDDEN)
                
            if role == 'enseignant':
                # On utilise user.uid qui est plus robuste
                uid = getattr(request.user, 'uid', request.user.username)
                enseignants = [self.repo.get_by_user_id(uid)]
                enseignants = [e for e in enseignants if e]
            else:
                enseignants = self.repo.list_all()
                
            serializer = EnseignantSerializer(enseignants, many=True)
            return Response(serializer.data)
        except Exception as e:
            import traceback
            return Response({
                "error": str(e),
                "traceback": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = EnseignantSerializer(data=request.data)
        if serializer.is_valid():
            from domain.entities.enseignant import Enseignant
            
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            matricule = serializer.validated_data['matricule']
            auth_service = Container.auth_service()
            
            try:
                display_name = f"{serializer.validated_data['prenom']} {serializer.validated_data['nom']}"
                user_id = auth_service.create_user(
                    email=email,
                    password=password,
                    display_name=display_name
                )
                auth_service.set_user_claims(user_id, 'enseignant')
                
                enseignant = Enseignant(
                    nom=serializer.validated_data['nom'],
                    prenom=serializer.validated_data['prenom'],
                    email=email,
                    matricule=matricule,
                    user_id=user_id
                )
                
                enseignant.valider()
                self.repo.save(enseignant)
                
                return_data = serializer.data
                return_data.pop('password', None)
                return Response(return_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        enseignant = self.repo.get_by_id(pk)
        if not enseignant:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = EnseignantSerializer(data=request.data)
        if serializer.is_valid():
            enseignant._nom = serializer.validated_data['nom']
            enseignant._prenom = serializer.validated_data['prenom']
            enseignant._email = serializer.validated_data['email']
            enseignant._matricule = serializer.validated_data['matricule']
            self.repo.save(enseignant)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        enseignant = self.repo.get_by_id(pk)
        if not enseignant:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        for key, value in request.data.items():
            if hasattr(enseignant, f"_{key}"):
                setattr(enseignant, f"_{key}", value)
        
        self.repo.save(enseignant)
        return Response(EnseignantSerializer(enseignant).data)

    @action(detail=True, methods=['post'], url_path='assign-matieres')
    def assign_matieres(self, request, pk=None):
        """Assigne plusieurs matières à un enseignant."""
        matiere_ids = request.data.get('matiere_ids', [])
        if not isinstance(matiere_ids, list):
            return Response({"error": "liste attendue"}, status=status.HTTP_400_BAD_REQUEST)
        
        matiere_repo = Container.matiere_repo()
        for m_id in matiere_ids:
            matiere_repo.attribuer_enseignant(m_id, pk)
            
        return Response({"status": "matières assignées"})

    def destroy(self, request, pk=None):
        self.repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
