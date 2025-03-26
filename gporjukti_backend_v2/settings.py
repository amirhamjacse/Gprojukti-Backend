from datetime import timedelta
from pathlib import Path
from decouple import config

from django.utils import timezone

import os
import environ
env = environ.Env()


from gporjukti_backend_v2.all_settings.app_vars import *
from gporjukti_backend_v2.all_settings.swagger_setup import *


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['stagingapi.gprojukti.com', '128.199.68.121', '128.199.68.121:3000', 'http://128.199.68.121:3000/', '*']


# Application definition

ON_TOP_APPS = [
    'corsheaders',
    
    
]
THIRD_PARTY_APPS = [
    'channels',
    'rest_framework',
    'django_filters',

    'actstream',
    'django_extensions', 
    'drf_spectacular',
    'rest_framework_simplejwt',
    'debug_toolbar',
    'dj_rest_auth.registration',
    
    'drf_spectacular_sidecar',
    'django_q',
    # 'django.contrib.gis'
    
    # 'django_extensions',
    
]

LOCAL_APPS = [
    'user_activity',
    'base',
    
    'user',
    'human_resource_management',
    'product_management',
    'location',
    'reports',
    'purchase_management',
    
    'discount',
    'order',
    'courier_management',
    'settings_management',
    
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = ON_TOP_APPS + DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


# Middleware 
THIRD_PARTY_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    
    # 'middleware.auth.AuthMiddleware',
#     'middleware.RequestResponseLogMiddleware',
]

DJANGO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE

ROOT_URLCONF = 'gporjukti_backend_v2.urls'

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

WSGI_APPLICATION = 'gporjukti_backend_v2.wsgi.application'
ASGI_APPLICATION = 'gporjukti_backend_v2.asgi.application'


if DATABASE_URL:
    DATABASES = {
        'default': {
            # 'ENGINE': 'django_db_geventpool.backends.postgresql_psycopg2',
            'ENGINE': 'django.db.backends.postgresql',
            # 'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASS,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
            # 'CONN_MAX_AGE': 60,
            # 'DB_MAX_CONNECTIONS': 200,
            # 'DB_MAX_IDLE_CONNECTIONS': 150,
            # 'OPTIONS': {
            #     'MAX_CONNS': 20,  # Example of a geventpool setting
            # },
        }
    }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': 'db.sqlite3',
#         }
#     }



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join('static_cdn', 'static_root')
MEDIA_ROOT = os.path.join('static_cdn', 'media_root')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GRAPH_MODELS = {
  'all_applications': True,
  'group_models': True,
  'app_labels': [],
}

SITE_ID = 1

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

AUTH_USER_MODEL = 'user.UserAccount'


# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

# MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_MEDIA_LOCATION)

#CELERY Setup


TODAY = timezone.now()
# TODAY = timezone.now() + timedelta(hours=6)

CURRENT_TIME = TODAY.time()


BASE_URL = 'http://productionapi.gprojukti.com/static/'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('productionapi.gprojukti.com', 6379)],
        },
    },
}


DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

CSRF_TRUSTED_ORIGINS = [
    'https://productionapi.gprojukti.com'
]


print(f"Today = {TODAY}, Database = {DATABASES}")