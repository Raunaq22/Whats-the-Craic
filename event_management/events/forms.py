from django import forms
from django.forms import DateInput, TimeInput
from .models import Event, Comment

class EventForm(forms.ModelForm):
    
    date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'placeholder': 'Select Date'}))
    time = forms.TimeField(widget=TimeInput(attrs={'type': 'time', 'placeholder': 'Select Time'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Description'}))
    capacity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Capacity'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price'}))
    categories = forms.ChoiceField(choices=Event.CATEGORY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'date', 'time', 'image', 'capacity', 'price', 'categories']
        
        labels = {
            'title': 'Event Title',
            'location': 'Event Location',
            'image': 'Event Image',
            'capacity': 'Event Capacity',
            'price': 'Event Price',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']