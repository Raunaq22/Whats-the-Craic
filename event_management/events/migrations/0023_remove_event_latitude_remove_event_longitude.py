# Generated by Django 5.0.2 on 2024-03-29 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_event_latitude_event_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='event',
            name='longitude',
        ),
    ]
