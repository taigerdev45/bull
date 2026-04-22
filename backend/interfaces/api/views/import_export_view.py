from rest_framework import views, status
from rest_framework.response import Response
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from interfaces.api.serializers.import_excel_serializer import ImportExcelSerializer
from infrastructure.config.dependency_injection import Container

@extend_schema(tags=['Évaluations'], summary="Importation massive de notes via Excel")
class ImportEvaluationsView(views.APIView):
    """Vue pour l'importation massive des notes."""

    def post(self, request):
        serializer = ImportExcelSerializer(data=request.data)
        if serializer.is_valid():
            fichier = serializer.validated_data['fichier']
            service = Container.import_export_service()
            
            # On récupère l'utilisateur depuis les claims Firebase (ou request.user)
            saisie_par = request.user.email if request.user.is_authenticated else "ADMIN_IMPORT"
            
            resultat = service.importer_evaluations(fichier.read(), saisie_par)
            return Response(resultat, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Résultats'], 
    summary="Exportation des résultats en Excel",
    parameters=[OpenApiParameter("promotion", OpenApiTypes.STR, OpenApiParameter.QUERY)]
)
class ExportResultatsView(views.APIView):
    """Vue pour l'exportation des résultats en Excel."""

    def get(self, request):
        promo_id = request.query_params.get('promotion')
        service = Container.import_export_service()
        contenu_excel = service.exporter_resultats_promotion(promo_id)
        
        response = HttpResponse(
            contenu_excel,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=resultats_{promo_id}.xlsx'
        return response
