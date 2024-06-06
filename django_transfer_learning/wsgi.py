"""
WSGI config for django_transfer_learning project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_transfer_learning.settings')

application = get_wsgi_application()
