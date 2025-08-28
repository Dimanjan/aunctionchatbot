"""
WSGI config for aliaunction project on PythonAnywhere.
"""

import os
import sys

# Add the project directory to the Python path
path = '/home/aliaunction/aliaunction_clean'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliaunction.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 