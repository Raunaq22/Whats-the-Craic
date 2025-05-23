# Generated by Django 5.0.2 on 2024-03-29 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_remove_event_tags_delete_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(to='events.tag'),
        ),
    ]
