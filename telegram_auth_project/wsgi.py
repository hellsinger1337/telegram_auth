import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_auth_project.settings')

application = get_wsgi_application()