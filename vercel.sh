#!/bin/bash
set -x
# Create the .vercel directory if it doesn't exist
mkdir -p .vercel

# Copy app files to root directory
echo "Copying app files to root directory..."
cp -r event_management/* .

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Prepare static files directory
echo "Preparing static files directory..."
mkdir -p staticfiles/css staticfiles/js staticfiles/images

# Copy static files to ensure they're included
echo "Copying template static files to build directly..."
cp -r events/templates/static/* staticfiles/ || true
cp -r events/static/* staticfiles/ || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

echo "===== Build Complete ====="

# Display environment (excluding secrets)
echo "Environment Variables:"
env | grep -v "SECRET\|KEY\|PASSWORD" || true

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

# Create the target staticfiles directory
mkdir -p staticfiles

# Copy collected static files to the deployment directory
echo "Copying collected static files..."
cp -r /tmp/static_root/* staticfiles/

# Print structure after collection 
echo "Directory structure after static collection:"
find . -type d -name "static*" | sort
ls -la staticfiles/

# Show available tables in database
echo "Checking database tables..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()
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
" 