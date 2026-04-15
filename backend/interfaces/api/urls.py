from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interfaces.api.views.etudiant_view import EtudiantViewSet, EvaluationView
from interfaces.api.views.absence_viewset import AbsenceViewSet
from interfaces.api.views.evaluation_viewset import EvaluationViewSet

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')
router.register(r'absences', AbsenceViewSet, basename='absence')
router.register(r'evaluations', EvaluationViewSet, basename='evaluation')

urlpatterns = [
    path('', include(router.urls)),
    path('evaluations/', EvaluationView.as_view(), name='evaluation-create'),
]
