from django.apps import AppConfig

class DjangoModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infrastructure.persistence.django_models'
    verbose_name = 'Modèles de Persistance Django'
