from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from dependency_injector.wiring import inject, Provide
from infrastructure.config.dependency_injection import Container
from rest_framework import serializers

class SemestreSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    libelle = serializers.CharField(max_length=100)
    annee_universitaire = serializers.CharField(max_length=20)

@extend_schema(tags=['Académique'])
class SemestreViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion des Semestres."""

    @inject
    def __init__(self, repo=Provide[Container.semestre_repo], **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def list(self, request):
        semestres = self.repo.list_all()
        serializer = SemestreSerializer(semestres, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = SemestreSerializer(data=request.data)
        if serializer.is_valid():
            from domain.entities.semestre import Semestre
            semestre = Semestre(
                libelle=serializer.validated_data['libelle'],
                annee_universitaire=serializer.validated_data['annee_universitaire']
            )
            self.repo.save(semestre)
            return Response(SemestreSerializer(semestre).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        semestre = self.repo.get_by_id(pk)
        if not semestre:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = SemestreSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            if 'libelle' in serializer.validated_data:
                semestre._libelle = serializer.validated_data['libelle']
            if 'annee_universitaire' in serializer.validated_data:
                semestre._annee_universitaire = serializer.validated_data['annee_universitaire']
            self.repo.save(semestre)
            return Response(SemestreSerializer(semestre).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        self.repo.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
