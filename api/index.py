import os
import sys

# Add the project root to the Python path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)

# Add the event_management directory to Python path
app_path = os.path.join(project_path, 'event_management')
if app_path not in sys.path:
    sys.path.insert(0, app_path)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')

try:
    # Import and configure Django
    import django
    django.setup()
    
    # Import Django WSGI handler
    from django.core.wsgi import get_wsgi_application
    
    # Create WSGI app
    django_app = get_wsgi_application()
    
    # Add WhiteNoise middleware for static files
    from whitenoise import WhiteNoise
    app = application = WhiteNoise(django_app)
    
    # Check possible locations for static files
    possible_static_dirs = [
        os.path.join(os.getcwd(), 'staticfiles'),
        os.path.join(app_path, 'staticfiles'),
        os.path.join(project_path, 'staticfiles')
    ]
    
    # Add static files from all available directories
    for static_dir in possible_static_dirs:
        if os.path.exists(static_dir):
            app.add_files(static_dir, prefix='static/')
            
    # Log success message
    print("Django application initialized successfully with REST API support")
            
except Exception as e:
    # Create a simple error handler for any initialization errors
    def app(event, context):
        return {
            'statusCode': 500,
            'body': f'Server initialization error: {str(e)}'
        }

# This file is required by Vercel for Python serverless functions 