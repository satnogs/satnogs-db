#!/usr/bin/env python
import dotenv
from django.core.wsgi import get_wsgi_application

dotenv.read_dotenv(dotenv='.env')
application = get_wsgi_application()
