"""
WSGI config for aliaunction project on PythonAnywhere.
"""

import os
import sys

# Add the project directory to the Python path
path = '/home/aliaunction/aliaunction_clean'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables from .env file
env_path = '/home/aliaunction/aliaunction_clean/.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                try:
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
                except ValueError:
                    # Skip lines that don't have proper key=value format
                    continue

# Set the Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliaunction.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 