"""
Django settings for config project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Définition de la racine du projet (BASE_DIR)
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Chargement explicite du fichier .env situé à la racine
load_dotenv(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == 'True'

# Autorise les connexions en local et développement
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librairies tierces
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    
    # Tes applications
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Doit être en premier
    'django.middleware.security.SecurityMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuration CORS pour Next.js / Frontend
CORS_ALLOW_ALL_ORIGINS = True 
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # Requis pour la gestion des images
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# REST Framework configuration

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}


# Database
# Les variables sont lues depuis ton fichier .env

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'fr-fr'  # Configuration en français
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# --- CONFIGURATION DES FICHIERS MEDIA (IMAGES / RIB / DOCUMENTS) ---

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Custom variables (JWT & Inscriptions)

JWT_TOKEN_DURATION = 3600 
DUREE_VALIDATION_INSCRIPTION = 300 


# Configuration Email (Gmail)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_PORT = 465                # On passe du port 587 au port 465
EMAIL_USE_TLS = False           # On désactive le TLS
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'misarabesa@gmail.com'
EMAIL_HOST_PASSWORD = 'diwi clxv fsky llfp'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Alternative de test (Mailtrap - Actuellement désactivée)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
# EMAIL_PORT = 2525
# EMAIL_HOST_USER = '5c63412d229a8f'
# EMAIL_HOST_PASSWORD = '59ddff6a8ca12d'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
