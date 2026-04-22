from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from rest_framework import serializers

class EnseignantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    matricule = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

@extend_schema(tags=['Administration'])
class EnseignantViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion des Enseignants."""

    @inject
    def __init__(self, repo=Provide[Container.enseignant_repo], **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def list(self, request):
        enseignants = self.repo.list_all()
        serializer = EnseignantSerializer(enseignants, many=True)
        return Response(serializer.data)

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

    def destroy(self, request, pk=None):
        self.repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
