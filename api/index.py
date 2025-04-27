import os
import sys

# Add the project root to the Python path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

# Add the event_management directory to Python path
app_path = os.path.join(project_path, 'event_management')
if app_path not in sys.path:
    sys.path.insert(0, app_path)

# Set Django settings - using just 'event_management.settings' rather than the nested path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')

# Import and configure Django
import django
django.setup()

# Import Django WSGI handler
from django.core.wsgi import get_wsgi_application
app = application = get_wsgi_application()

# This file is required by Vercel for Python serverless functions
# It imports the WSGI application from your Django project 