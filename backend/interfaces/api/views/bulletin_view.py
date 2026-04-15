from rest_framework import views, status
from rest_framework.response import Response
from interfaces.api.serializers.resultat_serializer import BulletinSerializer
from infrastructure.config.dependency_injection import Container

class BulletinView(views.APIView):
    """Vue pour récupérer les données complètes d'un bulletin."""

    def get(self, request, etudiant_id):
        type_bulletin = request.query_params.get('type', 'SEMESTRIEL')
        semestre = request.query_params.get('semestre')
        
        service = Container.bulletin_service()
        try:
            donnees = service.préparer_donnees_bulletin(
                etudiant_id=etudiant_id,
                type_bulletin=type_bulletin,
                semestre=int(semestre) if semestre else None
            )
            
            if not donnees:
                return Response({"error": "Données bulletin indisponibles"}, status=status.HTTP_404_NOT_FOUND)
                
            serializer = BulletinSerializer(donnees)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
