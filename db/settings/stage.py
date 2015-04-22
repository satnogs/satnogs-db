import os
from base import *

# Security
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*')

# Mail
EMAIL_HOST = "localhost"
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@example.com')
SERVER_EMAIL = DEFAULT_FROM_EMAIL
