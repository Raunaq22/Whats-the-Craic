import os
import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = 'Run migrations and seed initial data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database migrations'))
        
        # Run migrations
        call_command('migrate')
        
        # Check if tables exist
        self.check_tables()
        
        self.stdout.write(self.style.SUCCESS('Database setup complete'))
    
    def check_tables(self):
        """Check which tables exist in the database"""
        self.stdout.write(self.style.SUCCESS('Checking database tables...'))
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public'
                ORDER BY table_name;
            """)
            rows = cursor.fetchall()
            
            self.stdout.write(self.style.SUCCESS(f'Found {len(rows)} tables:'))
            for row in rows:
                self.stdout.write(f'  - {row[0]}') 