from rest_framework import viewsets, views, status
from rest_framework.response import Response
from interfaces.api.serializers.resultat_serializer import ResultatSemestreSerializer, ResultatAnnuelSerializer
from infrastructure.config.dependency_injection import Container
from application.queries.obtenir_stats_promotion_query import ObtenirStatsPromotionQuery

class ResultatSemestreView(views.APIView):
    def get(self, request, etudiant_id):
        semestre = request.query_params.get('semestre')
        if not semestre:
            return Response({"error": "Paramètre 'semestre' requis"}, status=status.HTTP_400_BAD_REQUEST)
        handler = Container.resultat_query_handler()
        resultat = handler.obtenir_resultat_semestre(etudiant_id, int(semestre))
        if not resultat:
            return Response({"error": "Résultat non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResultatSemestreSerializer(resultat)
        return Response(serializer.data)

class ResultatAnnuelView(views.APIView):
    def get(self, request, etudiant_id):
        handler = Container.resultat_query_handler()
        resultat = handler.obtenir_resultat_annuel(etudiant_id)
        if not resultat:
            return Response({"error": "Résultat annuel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResultatAnnuelSerializer(resultat)
        return Response(serializer.data)

class PromotionStatsView(views.APIView):
    """Vue pour les statistiques globales d'une promotion."""

    def get(self, request):
        promo_id = request.query_params.get('promo_id')
        query = ObtenirStatsPromotionQuery(
            promotion_id=promo_id,
            semestre=request.query_params.get('semestre')
        )
        handler = Container.resultat_query_handler()
        stats = handler.executer_stats_query(query)
        return Response(stats)
