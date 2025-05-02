from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Event
from .forms import EventForm
from .utils import extract_county, add_event_tags

def event_detail(request, event_id):
    """Display details of a specific event."""
    event = Event.objects.get(id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def event_create(request):
    """Create a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()  # Save the event first
            form.save_m2m()  # Save many-to-many relationships after the event is saved
            
            # Add tags programmatically
            add_event_tags(event)
            event.county = extract_county(event.location)
            event.save()
            
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

@login_required
def event_update(request, event_id):
    """Update an existing event."""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the current user is the creator of the event
    if request.user != event.organizer:
        return HttpResponseForbidden("You do not have permission to update this event.")
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()  # Save the event first
            form.save_m2m()  # Save many-to-many relationships after the event is saved
            add_event_tags(event)
            event.county = extract_county(event.location)
            event.save()
            return redirect('event_detail', event_id=event_id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_update.html', {'form': form})

@login_required
def event_delete(request, event_id):
    """Delete an existing event."""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if the current user is the creator of the event
    if request.user != event.organizer:
        return HttpResponseForbidden("You do not have permission to delete this event.")
    
    if request.method == 'POST':
        # Remove the associated image file from the media folder
        if event.image:
            event.image.delete(save=False)
        
        event.delete()
        return redirect('/my-events')

@login_required
def my_events(request):
    """Display events created by the logged-in user."""
    user_events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/my_events.html', {'user_events': user_events})

@login_required
def my_tickets(request):
    """Display tickets purchased by the logged-in user."""
    from .models import Ticket
    user_tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'events/my_tickets.html', {'user_tickets': user_tickets}) 