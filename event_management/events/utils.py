import re
from django.utils import timezone
from .models import Tag

def extract_county(location_string):
    """
    Extract county name from a location string.
    
    Example: "123 Main St, Dublin County, Ireland" => "Dublin"
    """
    parts = [part.strip() for part in location_string.split(',')]
    county_part = next((part for part in parts if re.match(r'\bCounty\b', part)), None)
    if county_part:
        county = re.sub(r'\bCounty\b', '', county_part).strip()
        return county
    else:
        return ''

def add_event_tags(event):
    """
    Add appropriate tags to an event based on its properties.
    
    - 'Closing Soon' tag if capacity is less than 50
    - 'Newly Added' tag if the event was created within the last 10 days
    """
    newly_added_tag, _ = Tag.objects.get_or_create(name='Newly Added')
    closing_soon_tag, _ = Tag.objects.get_or_create(name='Closing Soon')
    event.tags.clear()  # Clear existing tags before adding new ones
    
    if event.capacity < 50:
        event.tags.add(closing_soon_tag)
        
    if event.date >= timezone.now().date() - timezone.timedelta(days=10):
        event.tags.add(newly_added_tag)
