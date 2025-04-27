from django.shortcuts import render, get_object_or_404, redirect
import re
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Event, Ticket, Tag
from .forms import EventForm,CommentForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.db.models import Count
from django.conf import settings
from django.contrib import messages
from django.urls import reverse

import stripe

from django.http import HttpResponse
from django.template.loader import render_to_string

def styled_sitemap(request):
    sitemap_xml = render_to_string('sitemap.xml')
    return HttpResponse(sitemap_xml, content_type='text/xml')

def home(request):
    try:
        # Get featured events if tables exist
        featured_events = Event.objects.all().order_by('-date')[:4]
        return render(request, 'pages/home.html', {'featured_events': featured_events})
    except Exception as e:
        # If database tables don't exist, render the template without events
        print(f"Database error in home view: {str(e)}")
        return render(request, 'pages/home.html', {'featured_events': []})

def contact(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contact-us')  # Redirect to a success page
    else:
        form = CommentForm()
    return render(request, 'pages/contact.html', {'comment_form': form})

def dashboard(request):
    return render(request, 'pages/dashboard.html')

def profile(request):
    return render(request, 'pages/profile.html')

class ChangeUsername(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ['username']
    template_name = 'pages/change_username.html'
    success_message = "Username updated successfully"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('account_login')

def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

def extract_county(location_string):
    parts = [part.strip() for part in location_string.split(',')]
    county_part = next((part for part in parts if re.match(r'\bCounty\b', part)), None)
    if county_part:
        county = re.sub(r'\bCounty\b', '', county_part).strip()
        return county
    else:
        return ''

@login_required
def event_create(request):
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

def add_event_tags(event):
    newly_added_tag, _ = Tag.objects.get_or_create(name='Newly Added')
    closing_soon_tag, _ = Tag.objects.get_or_create(name='Closing Soon')
    event.tags.clear()  # Clear existing tags before adding new ones
    
    if event.capacity < 50:
        event.tags.add(closing_soon_tag)
        
    if event.date >= timezone.now().date() - timezone.timedelta(days=10):
        event.tags.add(newly_added_tag)


@login_required
def event_delete(request, event_id):
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
    # Retrieve events created by the logged-in user
    user_events = Event.objects.filter(organizer=request.user)
    return render(request, 'events/my_events.html', {'user_events': user_events})

@login_required
def my_tickets(request):
    # Retrieve tickets belonging to the logged-in user
    user_tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'events/my_tickets.html', {'user_tickets': user_tickets})

@login_required
def purchase_tickets(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Store event ID and user ID in the session
            request.session['event_id'] = event_id
            request.session['user_id'] = request.user.id

            # Create a Stripe Checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': event.title,
                        },
                        'unit_amount': int(event.price * 100),  # Convert price to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(reverse('payment_success')),  # Redirect URL after successful payment
                cancel_url=request.build_absolute_uri(reverse('payment_cancel')),   # Redirect URL if payment is canceled
            )

            return redirect(session.url)
        except stripe.error.StripeError as e:
            # Handle Stripe errors
            messages.error(request, str(e))
            return redirect('event_detail', event_id=event_id)
    else:
        return redirect('event_detail', event_id=event_id)

@login_required
def payment_success(request):
    # Retrieve event and user IDs from the session
    event_id = request.session.get('event_id')
    user_id = request.session.get('user_id')

    if event_id and user_id:
        # Retrieve the event and the user
        event = get_object_or_404(Event, id=event_id)
        user = get_object_or_404(User, id=user_id)

        # Check if there is available capacity for the event
        if event.capacity > 0:
            # Decrement the event capacity by one
            event.capacity -= 1
            event.save()  # Save the changes to the database

            # Create a new Ticket object upon successful payment
            ticket = Ticket.objects.create(
                user=user,
                event=event,
                title=event.title,
                price=event.price,
            )

            # Clear the session data
            del request.session['event_id']
            del request.session['user_id']

            return render(request, 'payments/success.html')
        else:
            # Handle the case where there's no available capacity
            messages.error(request, "This event is already fully booked.")
            return redirect('event_list')
    else:
        # Handle missing session data
        messages.error(request, "Session data not found.")
        return redirect('event_list')


@login_required
def payment_cancel(request):
    return render(request, 'payments/cancel.html')

def get_all_events(request):
    all_events = Event.objects.all()
    counties = Event.objects.values_list('county', flat=True).distinct()
    tags = Tag.objects.annotate(total_events=Count('event')).values_list('name', flat=True)
    categories = [choice[1] for choice in Event.CATEGORY_CHOICES]
    return render(request, 'events/get_events.html', {'events': all_events, 'counties': counties, 'tags': tags, 'categories': categories})

def event_list(request):
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
    

    




