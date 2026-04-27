from rest_framework import views, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from interfaces.api.serializers.resultat_serializer import BulletinSerializer
from infrastructure.config.dependency_injection import Container
from dependency_injector.wiring import inject, Provide

@extend_schema(tags=['Résultats'])
class SummaryBulletinListView(views.APIView):
    """Fournit le bilan synthétique de tous les étudiants pour le registre."""
    
    @inject
    def __init__(self, etudiant_repo=Provide[Container.etudiant_repo], 
                 resultat_handler=Provide[Container.resultat_query_handler], **kwargs):
        super().__init__(**kwargs)
        self.etudiant_repo = etudiant_repo
        self.resultat_handler = resultat_handler

    def get(self, request):
        etudiants = self.etudiant_repo.list_all()
        resultats = []
        for e in etudiants:
            try:
                res_s5 = self.resultat_handler.obtenir_resultat_semestre(e.matricule, 5)
                res_annuel = self.resultat_handler.obtenir_resultat_annuel(e.matricule)
                resultats.append({
                    "id": e.id,
                    "matricule": e.matricule,
                    "nom": e.nom,
                    "prenom": e.prenom,
                    "moyenne_S5": round(res_s5.moyenne_generale, 2) if res_s5 else None,
                    "moyenne_S6": None,
                    "moyenne_annuelle": round(res_annuel.moyenne_generale, 2) if res_annuel else None,
                    "decision_jury": res_annuel.decision if res_annuel else "En cours"
                })
            except Exception:
                resultats.append({
                    "id": e.id, "matricule": e.matricule, "nom": e.nom, "prenom": e.prenom,
                    "moyenne_S5": None, "moyenne_S6": None, "moyenne_annuelle": None, "decision_jury": "N/A"
                })
        return Response(resultats)

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
        is_staff = getattr(request.user, 'is_staff', False)
        user_role = getattr(request.user, 'role', 'etudiant').lower()
        if not is_staff and user_role == 'etudiant' and request.user.username != etudiant_id:
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
