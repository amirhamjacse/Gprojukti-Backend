from pathlib import Path
from decouple import config

import os
import environ
env = environ.Env()

# Database Information

DATABASE_URL = config('DATABASE_URL')

DB_NAME = config('DB_NAME')
DB_USER = config('DB_USER')
DB_PASS = config('DB_PASSWORD')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')

DATABASE_URL = config('DATABASE_URL')

# SECONDARY_DB_NAME = config('DB_NAME_2')
# SECONDARY_DB_USER = config('DB_USER_2')
# SECONDARY_DB_PASS = config('DB_PASSWORD_2')
# SECONDARY_DB_HOST = config('DB_HOST_2')
# SECONDARY_DB_PORT = config('DB_PORT_2')

# Email Information

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Email Information


# Load environment variables
GOOGLE_RECAPTCHA_SECRET_KEY = config('GOOGLE_RECAPTCHA_SECRET_KEY')

# Load environment variables
REDIS_HOST = config('REDIS_HOST')
RABBITMQ_URL = config('RABBITMQ_URL')

# Celery settings

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:6379/1".format(REDIS_HOST),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,
            "SOCKET_TIMEOUT": 5,
            "IGNORE_EXCEPTIONS": True,
            "SERIALIZER": "django_redis.serializers.json.JSONSerializer",
            "MASTER_CACHE": f"redis://{REDIS_HOST}:6379",
            "DB": 4,
        },
        "KEY_PREFIX": "gprojukti",
    }
}

CACHEOPS_REDIS = "redis://{}:6379/1".format(REDIS_HOST)

CACHEOPS_DEGRADE_ON_FAILURE = True
CACHEOPS_ENABLED = True

CACHEOPS = {
    'catalog.ProductGroup': {'ops': 'all', 'timeout': 60},
    'catalog.ProductCategory': {'ops': 'all', 'timeout': 60},
    'catalog.ProductSubCategory': {'ops': 'all', 'timeout': 60},
    'catalog.ProductVariant': {'ops': 'all', 'timeout': 60},
}


CELERY_BROKER_URL = 'redis://127.0.0.1:6380'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

# Other Celery configurations
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_DEFAULT_QUEUE = 'gprojukti.celery'

# CELERY_TASK_RESULT_EXPIRES = 3600
# CELERY_TASK_DEFAULT_QUEUE = 'gporjukti_backend_v2.celery'


# request setup
REQUEST_TIMEOUT = int(config('REQUEST_TIMEOUT', 8))

# AWS s3
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = config('SECRET_ACCESS_KEY')
S3_BUCKET = config('S3_BUCKET')

# SSL ECOMMERCE PAYMENT
SSL_STORE_ID = config('SSL_STORE_ID')
SSL_STORE_PASSWORD = config('SSL_STORE_PASSWORD')
SSL_BASE_URL = config('SSL_BASE_URL')

# Frontend
FRONTEND_BASE_URL = config('FRONTEND_BASE_URL')

# METABASE
METABASE_SITE_URL = config('METABASE_SITE_URL')
METABASE_SECRET_KEY = config('METABASE_SECRET_KEY')

# DIGITAL OCEAN SPACES
DIGITAL_OCEAN_SPACES_ACCESS_KEY_ID = config('DIGITAL_OCEAN_SPACES_ACCESS_KEY_ID')
DIGITAL_OCEAN_SPACES_SECRET_ACCESS_KEY = config('DIGITAL_OCEAN_SPACES_SECRET_ACCESS_KEY')
DIGITAL_OCEAN_SPACES_ENDPOINT_URL = config('DIGITAL_OCEAN_SPACES_ENDPOINT_URL')
DIGITAL_OCEAN_SPACES_BUCKET_NAME = config('DIGITAL_OCEAN_SPACES_BUCKET_NAME')


# Others Setup

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True

APPEND_SLASH = False

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# SSL Commerce SMS

SSL_SMS_API_TOKEN = config('SSL_SMS_API_TOKEN')
SSL_SID = config('SSL_SID')

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": config("FCM_SERVER_KEY"),
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}

NOT_FOUND_IMAGE = 'https://gprmain.sgp1.cdn.digitaloceanspaces.com/gprojukti-v2-test/product/5347d3f549a74d0d8524884e961585e9-2ad60ddd-c97a-4d46-ae86-dd1b522a8514.png'

Q_CLUSTER = {
    'name': 'DjangoQCluster',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',  # Using Django's ORM as the broker
}