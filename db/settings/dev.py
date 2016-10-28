from base import *  # flake8: noqa

ENVIRONMENT = 'dev'

# Debug
DEBUG = True

# Mail
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
