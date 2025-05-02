from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
from .models import Event, Tag

def get_all_events(request):
    """Get all events with filter information."""
    all_events = Event.objects.all()
    counties = Event.objects.values_list('county', flat=True).distinct()
    tags = Tag.objects.annotate(total_events=Count('event')).values_list('name', flat=True)
    categories = [choice[1] for choice in Event.CATEGORY_CHOICES]
    return render(request, 'events/get_events.html', {'events': all_events, 'counties': counties, 'tags': tags, 'categories': categories})

def event_list(request):
    """Display events with filtering capabilities."""
    all_events = Event.objects.all()
    counties = Event.objects.values_list('county', flat=True).distinct()
    
    newly_added_events = all_events.filter(tags__name='Newly Added')
    closing_soon_events = all_events.filter(tags__name='Closing Soon')
    
    hot_events = all_events.filter(Q(capacity__lt=50) | Q(date__gte=timezone.now().date() - timezone.timedelta(days=10)))
    
    tag_filtered_events = all_events.filter(tags__name='tag_name')
    
    selected_county = 'Dublin'
    if 'county' in request.GET:
        selected_county = request.GET['county']
    
    events_by_county = all_events.filter(county=selected_county)
    
    return render(request, 'events/event_list.html', {
        'counties': counties,
        'newly_added_events': newly_added_events,
        'closing_soon_events': closing_soon_events,
        'hot_events': hot_events,
        'tag_filtered_events': tag_filtered_events,
        'selected_county': selected_county,
        'events_by_county': events_by_county,
    }) 