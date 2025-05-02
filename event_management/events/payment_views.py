from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from .models import Event, Ticket

import stripe

@login_required
def purchase_tickets(request, event_id):
    """Handle the ticket purchase process."""
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
    """Handle successful payment completion."""
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
    """Handle payment cancellation."""
    return render(request, 'payments/cancel.html') 