import os
from base import *  # flake8: noqa

ENVIRONMENT = 'production'

# Opbeat
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'opbeat.contrib.django.middleware.Opbeat404CatchMiddleware',
)
INSTALLED_APPS = INSTALLED_APPS + (
    'opbeat.contrib.django',
)

# Cache
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'unix://var/run/redis/redis.sock',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'db-{0}'.format(ENVIRONMENT)
    }
}

# Security
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
ALLOWED_HOSTS = [
    os.getenv('ALLOWED_HOSTS', '*')
]

# Email
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_TIMEOUT = 300
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Metrics
OPBEAT = {
    'ORGANIZATION_ID': os.getenv('OPBEAT_ORGID', None),
    'APP_ID': os.getenv('OPBEAT_APPID', None),
    'SECRET_TOKEN': os.getenv('OPBEAT_SECRET', None),
}
