from os import getenv
from dj_database_url import parse as db_url
from unipath import Path


ROOT = Path(__file__).parent.parent

ENVIRONMENT = getenv('ENVIRONMENT', 'production')
DEBUG = getenv('DEBUG', False)

# Apps
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)
THIRD_PARTY_APPS = (
    'avatar',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'compressor',
    'csp',
    'opbeat.contrib.django',
)
LOCAL_APPS = (
    'db.base',
    'db.api',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middlware
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
    'opbeat.contrib.django.middleware.Opbeat404CatchMiddleware',
)

# Email
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_TIMEOUT = 300
DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL', 'noreply@satnogs.org')
ADMINS = (
    (
        getenv('ADMINS_FROM_NAME', 'SatNOGS Admins'),
        getenv('ADMINS_FROM_EMAIL', DEFAULT_FROM_EMAIL)
    ),
)
MANAGERS = ADMINS
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Cache
CACHES = {
    'default': {
        'BACKEND': getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': getenv('CACHE_LOCATION', 'unique-snowflake'),
        'OPTIONS': {
            'CLIENT_CLASS': getenv('CACHE_CLIENT_CLASS', None),
        },
        'KEY_PREFIX': 'db-{0}'.format(ENVIRONMENT),
    }
}
CACHE_TTL = int(getenv('CACHE_TTL', 300))

# Internationalization
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            Path('db/templates').resolve(),
        ],
        'OPTIONS': {
            'debug': False,
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'db.base.context_processors.analytics',
                'db.base.context_processors.stage_notice',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },

    },
]

# Static & Media
STATIC_ROOT = Path('staticfiles').resolve()
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    Path('db/static').resolve(),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
MEDIA_ROOT = Path('media').resolve()
MEDIA_URL = '/media/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
SATELLITE_DEFAULT_IMAGE = '/static/img/sat.png'

# App conf
ROOT_URLCONF = 'db.urls'
WSGI_APPLICATION = 'db.wsgi.application'
SITE_URL = getenv('SITE_URL', 'https://db.satnogs.org/')

# Auth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
LOGIN_REDIRECT_URL = 'home'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s - %(process)d %(thread)d - %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'opbeat': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
        },
    },
    'loggers': {
        'django.request': {
            'level': 'ERROR',
            'handlers': ['opbeat'],
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['opbeat'],
            'propagate': False,
        },
        'db': {
            'level': 'WARNING',
            'handlers': ['console', 'opbeat'],
            'propagate': False,
        },
        'opbeat.errors': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

# Celery
CELERY_ENABLE_UTC = USE_TZ
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_RESULTS_EXPIRES = 3600
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_TASK_ALWAYS_EAGER = True
CELERY_DEFAULT_QUEUE = 'db-{0}-queue'.format(ENVIRONMENT)
CELERY_BROKER_URL = getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')

# API
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    )
}

# Security
SECRET_KEY = getenv('SECRET_KEY', 'changeme')
CSP_DEFAULT_SRC = (
    "'self'",
    'https://*.mapbox.com',
)
CSP_SCRIPT_SRC = (
    "'self'",
    'https://*.google-analytics.com',
)
CSP_IMG_SRC = (
    "'self'",
    'https://*.gravatar.com',
    'https://*.mapbox.com',
    'https://*.google-analytics.com',
)
SECURE_HSTS_SECONDS = getenv('SECURE_HSTS_SECONDS', 31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
ALLOWED_HOSTS = [
    getenv('ALLOWED_HOSTS', '*')
]

# Database
DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
DATABASES = {'default': db_url(DATABASE_URL)}

# NETWORK API
NETWORK_API_ENDPOINT = getenv('NETWORK_API_ENDPOINT', 'https://network.satnogs.org/api/')
DATA_FETCH_DAYS = getenv('DATA_FETCH_DAYS', 10)
SATELLITE_POSITION_ENDPOINT = getenv('SATELLITE_POSITION_ENDPOINT',
                                     'https://network.satnogs.org/satellite_position/')

# Mapbox API
MAPBOX_GEOCODE_URL = 'https://api.tiles.mapbox.com/v4/geocode/mapbox.places/'
MAPBOX_MAP_ID = getenv('MAPBOX_MAP_ID', '')
MAPBOX_TOKEN = getenv('MAPBOX_TOKEN', '')

# Metrics
OPBEAT = {
    'ORGANIZATION_ID': getenv('OPBEAT_ORGID', None),
    'APP_ID': getenv('OPBEAT_APPID', None),
    'SECRET_TOKEN': getenv('OPBEAT_SECRET', None),
}
