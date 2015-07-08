import os
from base import *

ENVIRONMENT = 'production'

# Security
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*')

# Email
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_TIMEOUT = 300
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Metrics
MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    'opbeat.contrib.django.middleware.OpbeatAPMMiddleware',
)
INSTALLED_APPS = INSTALLED_APPS + (
    'opbeat.contrib.django',
)
OPBEAT = {
    'ORGANIZATION_ID': os.getenv('OPBEAT_ORGID', None),
    'APP_ID': os.getenv('OPBEAT_APPID', None),
    'SECRET_TOKEN': os.getenv('OPBEAT_SECRET', None),
}
GOOGLE_ANALYTICS_KEY = os.getenv('GOOGLE_ANALYTICS_KEY', None)
