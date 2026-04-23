from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from interfaces.api.views.etudiant_view import EtudiantViewSet
from interfaces.api.views.absence_viewset import AbsenceViewSet
from interfaces.api.views.evaluation_viewset import EvaluationViewSet
from interfaces.api.views.resultat_view import ResultatSemestreView, ResultatAnnuelView, PromotionStatsView
from interfaces.api.views.bulletin_view import BulletinView
from interfaces.api.views.import_export_view import ImportEvaluationsView, ExportResultatsView
from interfaces.api.views.ue_viewset import UEViewSet, MatiereViewSet
from interfaces.api.views.audit_viewset import AuditViewSet
from interfaces.api.views.parametres_view import ParametresView
from interfaces.api.views.semestre_view import SemestreViewSet
from interfaces.api.views.enseignant_view import EnseignantViewSet
from interfaces.api.views.auth_view import ChangePasswordView, LoginView
from interfaces.api.views.personnel_viewset import PersonnelViewSet
from application.startup import initialiser_abonnements

# Initialisation de l'audit
initialiser_abonnements()

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')
router.register(r'absences', AbsenceViewSet, basename='absence')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')
router.register(r'ues', UEViewSet, basename='ue')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'semestres', SemestreViewSet, basename='semestre')
router.register(r'enseignants', EnseignantViewSet, basename='enseignant')
router.register(r'personnel', PersonnelViewSet, basename='personnel')
router.register(r'audit', AuditViewSet, basename='audit')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('resultats/semestre/<str:etudiant_id>/', ResultatSemestreView.as_view()),
    path('resultats/annuel/<str:etudiant_id>/', ResultatAnnuelView.as_view()),
    path('resultats/promotion/stats/', PromotionStatsView.as_view()),
    path('bulletins/donnees/<str:etudiant_id>/', BulletinView.as_view()),
    path('import/evaluations/', ImportEvaluationsView.as_view()),
    path('export/resultats/', ExportResultatsView.as_view()),
    path('parametres/', ParametresView.as_view(), name='parametres'),
]
