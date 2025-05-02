import os
import sys
import traceback
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Log system information
logger.info(f"Python version: {sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Directory contents: {os.listdir('.')}")

# Add the project root to the Python path
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_path)
logger.info(f"Project path: {project_path}")
logger.info(f"Project directory contents: {os.listdir(project_path)}")

# Add the event_management directory to Python path
app_path = os.path.join(project_path, 'event_management')
if app_path not in sys.path:
    sys.path.insert(0, app_path)
logger.info(f"App path: {app_path}")
if os.path.exists(app_path):
    logger.info(f"App directory contents: {os.listdir(app_path)}")
else:
    logger.error(f"App directory does not exist: {app_path}")

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
logger.info(f"Set DJANGO_SETTINGS_MODULE to {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# Log environment variables (excluding sensitive data)
safe_env = {k: v for k, v in os.environ.items() 
            if not any(s in k.lower() for s in ['key', 'password', 'secret', 'token'])}
logger.info(f"Environment variables: {safe_env}")

# Capture the exception at the module level
initialization_error = None

try:
    logger.info("Importing Django...")
    import django
    logger.info(f"Django version: {django.get_version()}")
    
    logger.info("Setting up Django...")
    django.setup()
    logger.info("Django setup complete")
    
    logger.info("Importing WSGI application...")
    from django.core.wsgi import get_wsgi_application
    
    logger.info("Creating WSGI application...")
    django_app = get_wsgi_application()
    logger.info("WSGI application created")
    
    logger.info("Importing WhiteNoise...")
    from whitenoise import WhiteNoise
    logger.info(f"WhiteNoise version: {WhiteNoise.__version__ if hasattr(WhiteNoise, '__version__') else 'unknown'}")
    
    logger.info("Setting up WhiteNoise...")
    app = application = WhiteNoise(django_app)
    logger.info("WhiteNoise setup complete")
    
    # Check possible locations for static files
    possible_static_dirs = [
        os.path.join(os.getcwd(), 'staticfiles'),
        os.path.join(app_path, 'staticfiles'),
        os.path.join(project_path, 'staticfiles')
    ]
    
    logger.info(f"Checking static file directories: {possible_static_dirs}")
    # Add static files from all available directories
    for static_dir in possible_static_dirs:
        if os.path.exists(static_dir):
            logger.info(f"Adding static files from: {static_dir}")
            logger.info(f"Static directory contents: {os.listdir(static_dir)}")
            app.add_files(static_dir, prefix='static/')
        else:
            logger.warning(f"Static directory not found: {static_dir}")
            
    # Database connection test
    logger.info("Testing database connection...")
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        logger.info("Database connection successful")
    except Exception as db_error:
        logger.error(f"Database connection error: {str(db_error)}")
        logger.error(traceback.format_exc())
    
    # Log success message
    logger.info("Django application initialized successfully with REST API support")
            
except Exception as e:
    initialization_error = e
    logger.error(f"Initialization error: {str(e)}")
    logger.error(traceback.format_exc())
    
    # Create a simple error handler for any initialization errors
    def app(event, context):
        error_message = f"Server initialization error: {str(initialization_error)}\n{traceback.format_exc()}"
        logger.error(f"Error handling request: {error_message}")
        return {
            'statusCode': 500,
            'body': error_message
        }

# Wrap the application to log any runtime errors
if 'app' in locals() and callable(app):
    original_app = app
    def error_logging_app(event, context):
        try:
            logger.info(f"Handling request: {event}")
            response = original_app(event, context)
            return response
        except Exception as runtime_error:
            error_message = f"Runtime error: {str(runtime_error)}\n{traceback.format_exc()}"
            logger.error(error_message)
            return {
                'statusCode': 500,
                'body': error_message
            }
    app = application = error_logging_app

# This file is required by Vercel for Python serverless functions 