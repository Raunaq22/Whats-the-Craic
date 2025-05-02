from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Event
from .forms import CommentForm

def styled_sitemap(request):
    """Generate a styled sitemap."""
    sitemap_xml = render_to_string('sitemap.xml')
    return HttpResponse(sitemap_xml, content_type='text/xml')

def home(request):
    """Render the home page with featured events."""
    try:
        # Get featured events if tables exist
        featured_events = Event.objects.all().order_by('-date')[:4]
        return render(request, 'pages/home.html', {'featured_events': featured_events})
    except Exception as e:
        # If database tables don't exist, render the template without events
        print(f"Database error in home view: {str(e)}")
        return render(request, 'pages/home.html', {'featured_events': []})

def contact(request):
    """Handle contact form submissions."""
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contact-us')  # Redirect to a success page
    else:
        form = CommentForm()
    return render(request, 'pages/contact.html', {'comment_form': form})

def dashboard(request):
    """Render the dashboard page."""
    return render(request, 'pages/dashboard.html')

def profile(request):
    """Render the user profile page."""
    return render(request, 'pages/profile.html')

class ChangeUsername(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Allow users to change their username."""
    model = User
    fields = ['username']
    template_name = 'pages/change_username.html'
    success_message = "Username updated successfully"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('account_login') 