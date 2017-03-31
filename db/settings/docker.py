from base import *  # flake8: noqa

ENVIRONMENT = 'dev'

# Debug
DEBUG = True

# Mail
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache
CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        },
        'KEY_PREFIX': 'db-{0}'.format(ENVIRONMENT)
    }
}

# Celery
CELERY_DEFAULT_QUEUE = 'db-{0}-queue'.format(ENVIRONMENT)
CELERY_BROKER_URL = getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
