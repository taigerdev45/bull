from rest_framework import views, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from interfaces.api.serializers.resultat_serializer import BulletinSerializer
from infrastructure.config.dependency_injection import Container

@extend_schema(
    tags=['Résultats'],
    parameters=[
        OpenApiParameter("type", OpenApiTypes.STR, OpenApiParameter.QUERY, enum=['SEMESTRIEL', 'ANNUEL']),
        OpenApiParameter("semestre", OpenApiTypes.INT, OpenApiParameter.QUERY)
    ]
)
class BulletinView(views.APIView):
    """Vue pour récupérer les données complètes d'un bulletin."""

    def get(self, request, etudiant_id):
        # Sécurité : un étudiant ne doit voir que son bulletin
        auth = request.auth if isinstance(request.auth, dict) else {}
        user_role = (auth.get('role') or getattr(request.user, 'role', 'etudiant')).lower()
        if user_role == 'etudiant' and request.user.username != etudiant_id:
            return Response({"error": "Accès refusé"}, status=status.HTTP_403_FORBIDDEN)
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
