from django.urls import path, include
from rest_framework.routers import DefaultRouter
from interfaces.api.views.etudiant_view import EtudiantViewSet, EvaluationView

router = DefaultRouter()
router.register(r'etudiants', EtudiantViewSet, basename='etudiant')

urlpatterns = [
    path('', include(router.urls)),
    path('evaluations/', EvaluationView.as_view(), name='evaluation-create'),
]
