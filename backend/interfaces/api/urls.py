from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interfaces.api.views.etudiant_view import EtudiantViewSet, EvaluationView
from interfaces.api.views.absence_viewset import AbsenceViewSet
from interfaces.api.views.evaluation_viewset import EvaluationViewSet
from interfaces.api.views.resultat_view import ResultatSemestreView, ResultatAnnuelView, PromotionStatsView
from interfaces.api.views.bulletin_view import BulletinView
from interfaces.api.views.import_export_view import ImportEvaluationsView, ExportResultatsView

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')
router.register(r'absences', AbsenceViewSet, basename='absence')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')

urlpatterns = [
    path('', include(router.urls)),
    path('resultats/semestre/<str:etudiant_id>/', ResultatSemestreView.as_view()),
    path('resultats/annuel/<str:etudiant_id>/', ResultatAnnuelView.as_view()),
    path('resultats/promotion/stats/', PromotionStatsView.as_view()),
    path('bulletins/donnees/<str:etudiant_id>/', BulletinView.as_view()),
    path('import/evaluations/', ImportEvaluationsView.as_view()),
    path('export/resultats/', ExportResultatsView.as_view()),
    path('evaluations/', EvaluationView.as_view(), name='evaluation-create'),
]
