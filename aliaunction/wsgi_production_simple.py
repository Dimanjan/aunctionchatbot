"""
WSGI config for aliaunction project on PythonAnywhere (Simplified version).
"""

import os
import sys

# Add the project directory to the Python path
path = '/home/aliaunction/aliaunction_clean'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables directly (replace with your actual values)
os.environ['SECRET_KEY'] = 'your-secret-key-here'  # Replace with actual secret key
os.environ['DEBUG'] = 'False'
os.environ['OPENAI_API_KEY'] = 'your-openai-api-key-here'  # Replace with actual API key
os.environ['EMAIL_HOST_USER'] = 'your-email@gmail.com'  # Optional
os.environ['EMAIL_HOST_PASSWORD'] = 'your-app-password'  # Optional
os.environ['DEFAULT_FROM_EMAIL'] = 'no-reply@aliaunction.com'

# Set the Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aliaunction.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() 