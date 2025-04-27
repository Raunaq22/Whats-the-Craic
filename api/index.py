import os
import sys
import traceback

# Add the project root to the Python path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

# Add the event_management directory to Python path
app_path = os.path.join(project_path, 'event_management')
if app_path not in sys.path:
    sys.path.insert(0, app_path)

# Print environment for debugging
print("Python version:", sys.version)
print("PYTHONPATH:", sys.path)
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir())

# Set Django settings - using just 'event_management.settings' rather than the nested path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')

# Force DEBUG mode for troubleshooting
os.environ['DEBUG'] = 'True'

try:
    # Import and configure Django
    import django
    django.setup()

    # Import Django WSGI handler
    from django.core.wsgi import get_wsgi_application
    app = application = get_wsgi_application()
except Exception as e:
    # Print detailed error information
    print("ERROR INITIALIZING APPLICATION:", str(e))
    traceback.print_exc()
    
    # Create a simple error handler
    def app(event, context):
        return {
            'statusCode': 500,
            'body': f'Server initialization error: {str(e)}\n{traceback.format_exc()}'
        }

# This file is required by Vercel for Python serverless functions
# It imports the WSGI application from your Django project 