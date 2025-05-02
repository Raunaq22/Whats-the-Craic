#!/bin/bash
set -x

echo "========== DEBUGGING INFO =========="
echo "Current date: $(date)"
echo "Current directory: $(pwd)"
echo "Directory contents: $(ls -la)"
echo "Python version: $(python --version)"
echo "Node version: $(node --version 2>/dev/null || echo 'Node not installed')"
echo "NPM version: $(npm --version 2>/dev/null || echo 'NPM not installed')"
echo "Environment variables (excluding secrets):"
env | grep -v "SECRET\|KEY\|PASSWORD\|TOKEN" || true
echo "=================================="

# Create the .vercel directory if it doesn't exist
mkdir -p .vercel
echo "Created .vercel directory"

# Copy app files to root directory
echo "Copying app files to root directory..."
cp -r event_management/* .
echo "Files copied to root directory. Current directory structure:"
ls -la

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Found requirements.txt: $(cat requirements.txt)"
else
    echo "ERROR: requirements.txt not found!"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully"

# Prepare static files directory
echo "Preparing static files directory..."
mkdir -p staticfiles/css staticfiles/js staticfiles/images
echo "Static files directories created"

# Copy static files to ensure they're included
echo "Copying template static files to build directly..."
if [ -d "events/templates/static" ]; then
    cp -r events/templates/static/* staticfiles/ || true
    echo "Copied template static files"
else
    echo "WARNING: events/templates/static directory does not exist"
fi

if [ -d "events/static" ]; then
    cp -r events/static/* staticfiles/ || true
    echo "Copied events static files"
else
    echo "WARNING: events/static directory does not exist"
fi

echo "Static files directory content:"
ls -la staticfiles/

# Check if manage.py exists
if [ -f "manage.py" ]; then
    echo "Found manage.py"
else
    echo "ERROR: manage.py not found!"
    exit 1
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "WARNING: collectstatic command failed"
else
    echo "Static files collected successfully"
fi

# Check database configuration
echo "Database configuration:"
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()
from django.conf import settings
print(f'Engine: {settings.DATABASES[\"default\"][\"ENGINE\"]}')
print(f'Name: {settings.DATABASES[\"default\"][\"NAME\"]}')
print(f'Host: {settings.DATABASES[\"default\"].get(\"HOST\", \"none\")}')
print(f'Port: {settings.DATABASES[\"default\"].get(\"PORT\", \"none\")}')
" || echo "Failed to get database configuration"

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "WARNING: Database migration failed"
else
    echo "Database migrations applied successfully"
fi

echo "===== Build Complete ====="

# Display environment (excluding secrets)
echo "Environment Variables:"
env | grep -v "SECRET\|KEY\|PASSWORD\|TOKEN" || true

# List installed packages
pip list

# Print structure before collection
echo "Directory structure before static collection:"
find . -type d -name "static*" | sort

# Make sure staticfiles directory exists in the RIGHT place
mkdir -p /tmp/static_root
export STATIC_ROOT=/tmp/static_root

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "WARNING: Second collectstatic command failed"
else
    echo "Static files collected successfully to $STATIC_ROOT"
fi

# Create the target staticfiles directory
mkdir -p staticfiles

# Copy collected static files to the deployment directory
echo "Copying collected static files..."
cp -r /tmp/static_root/* staticfiles/
echo "Static files copied to final location"

# Print structure after collection 
echo "Directory structure after static collection:"
find . -type d -name "static*" | sort
ls -la staticfiles/

# Check Django settings module
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "Testing Django configuration..."
python -c "
import os
import sys
import django
print(f'Python path: {sys.path}')
print(f'Current working directory: {os.getcwd()}')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
print(f'Django settings module: {os.environ.get(\"DJANGO_SETTINGS_MODULE\")}')
django.setup()
print('Django setup complete')
from django.conf import settings
print(f'Debug mode: {settings.DEBUG}')
print(f'Allowed hosts: {settings.ALLOWED_HOSTS}')
" || echo "Failed to test Django configuration"

# Create a test API file to verify server functionality
echo "Creating test API endpoint..."
mkdir -p api/test
cat > api/test/index.py << 'EOL'
import os
import sys
import json
from datetime import datetime

def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Test endpoint is working',
            'timestamp': datetime.now().isoformat(),
            'python_version': sys.version,
            'env': dict(os.environ),
            'event': event,
        }, default=str)
    }
EOL
echo "Test API endpoint created at api/test/index.py"

# Show available tables in database
echo "Checking database tables..."
python -c "
import os
import django
import traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute(\"\"\"
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
            ORDER BY table_name;
        \"\"\")
        rows = cursor.fetchall()
        for row in rows:
            print(row[0])
except Exception as e:
    print(f'Error checking database: {str(e)}')
    print(traceback.format_exc())
" || echo "Failed to check database tables"

echo "========== BUILD SCRIPT COMPLETED =========="
echo "Timestamp: $(date)" 