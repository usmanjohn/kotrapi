import os
from pathlib import Path

import dj_database_url
import environ
from storages.backends.s3boto3 import S3Boto3Storage

from kotrainapi.storage_backends import StaticStorage, MediaStorage


# Initialize environment variables
env = environ.Env()
# Read .env file
environ.Env.read_env(os.path.join(Path(__file__).resolve().parent.parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = env('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    'rest_framework',
    'rest_framework_simplejwt',
    #
    'storages',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    #apps
    'accounts',
    'topics',

    
    #3rd party
    'taggit',
    
    

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'kotrainapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #'topics.context_processors.logo_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'kotrainapi.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(conn_max_age=0, ssl_require=False)
}
DATABASES['default'] = DATABASES['default']

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Ensure emails are sent from your actual email
SERVER_EMAIL = EMAIL_HOST_USER 

# Static files (CSS, JavaScript, Images)
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
AWS_LOCATION = env('AWS_LOCATION')

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'



STATICFILES_STORAGE = 'kotrainapi.storage_backends.StaticStorage'
DEFAULT_FILE_STORAGE = 'kotrainapi.storage_backends.MediaStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CORS_ALLOW_ALL_ORIGINS = True

# Miscellaneous settings
DATA_UPLOAD_MAX_NUMBER_FIELDS = 11240
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication

AUTH_USER_MODEL = 'accounts.CustomUser'

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT_URL = 'home'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

## Rest Framework auth

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}
