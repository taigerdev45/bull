import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY and not DEBUG:
    raise ValueError("DJANGO_SECRET_KEY doit être configuré en production.")

DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,.onrender.com').split(',')

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Pour les actions Admin
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET") # Pour la validation des tokens

# CORS Configuration
default_origins = 'http://localhost:3000,http://127.0.0.1:3000'
CORS_ALLOWED_ORIGINS = [
    origin.rstrip('/') for origin in os.getenv('CORS_ALLOWED_ORIGINS', default_origins).split(',') if origin
]

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = [
    origin.rstrip('/') for origin in os.getenv('CSRF_TRUSTED_ORIGINS', default_origins).split(',') if origin
]

# Autoriser les prévisualisations Vercel via Regex
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]

CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'drf_spectacular',

    # Local layers (interfaces)
    'interfaces.api.apps.ApiConfig',
    'infrastructure.persistence.django_models.apps.DjangoModelsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'infrastructure.middleware.error_logger.DRFErrorLoggingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'infrastructure.middleware.csrf_middleware.DisableCSRFMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

WSGI_APPLICATION = 'config.wsgi.application'

import dj_database_url

# Database (PostgreSQL Supabase ou SQLite local)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'interfaces.api.permissions.supabase_auth.SupabaseAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '50/minute',
    },
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Bull-Asur Notes API',
    'DESCRIPTION': (
        'API Enterprise de gestion des bulletins de notes (DDD Architecture).\n\n'
        '### Authentification\n'
        'Cette API utilise des tokens JWT fournis par Supabase. \n'
        '1. Récupérez un token sur `/api/auth/login/` (ou via le frontend).\n'
        '2. Cliquez sur le bouton **Authorize** en haut à droite.\n'
        '3. Saisissez votre token dans le champ `Value` (format: `your_token_here`).'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'Support Technique Bull',
        'url': 'https://github.com/taigerdev45/bull',
    },
    'LICENSE': {
        'name': 'Proprietary',
    },
    'TAGS': [
        {'name': 'Authentification', 'description': 'Gestion des comptes et tokens'},
        {'name': 'Étudiants', 'description': 'Gestion des dossiers scolaires'},
        {'name': 'Évaluations', 'description': 'Saisie et gestion des notes'},
        {'name': 'Absences', 'description': 'Gestion de l\'assiduité'},
        {'name': 'Académique', 'description': 'Référentiels UE, Matières, Semestres'},
        {'name': 'Résultats', 'description': 'Consultation des moyennes et bulletins'},
        {'name': 'Administration', 'description': 'Audit et configuration système'},
    ],
    'SECURITY': [
        {
            'bearerAuth': [],
        }
    ],
    'APPEND_COMPONENTS': {
        'securitySchemes': {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
}

