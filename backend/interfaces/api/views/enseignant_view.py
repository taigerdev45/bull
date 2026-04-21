from rest_framework import viewsets, status
from rest_framework.response import Response
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from rest_framework import serializers

class EnseignantSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()

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
            enseignant = Enseignant(
                nom=serializer.validated_data['nom'],
                prenom=serializer.validated_data['prenom'],
                email=serializer.validated_data['email']
            )
            self.repo.save(enseignant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        self.repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
