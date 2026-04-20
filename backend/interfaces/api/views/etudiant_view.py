from rest_framework import viewsets, status, views
from rest_framework.response import Response
from interfaces.api.serializers.etudiant_serializer import EtudiantSerializer
from interfaces.api.serializers.evaluation_serializer import EvaluationSerializer
from interfaces.api.permissions.role_permissions import IsSecretariat, IsEnseignant
from infrastructure.config.dependency_injection import Container

class EtudiantViewSet(viewsets.ViewSet):
    """ViewSet pour la gestion CRUD des étudiants via le repository."""
    permission_classes = [IsSecretariat]

    def list(self, request):
        repo = Container.etudiant_repo()
        etudiants = repo.list_all()
        serializer = EtudiantSerializer(etudiants, many=True)
        return Response(serializer.data)

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
