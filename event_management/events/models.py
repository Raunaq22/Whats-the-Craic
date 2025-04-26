from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    capacity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('nightlife', 'Nightlife'),
        ('performing_visual_arts', 'Performing & Visual Arts'),
        ('holidays', 'Holidays'),
        ('health', 'Health'),
        ('hobbies', 'Hobbies'),
        ('business', 'Business'),
        ('food_drink', 'Food & Drink'),
    ]
    categories = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='-')
    tags = models.ManyToManyField(Tag)
    
    county = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("change_owned_event", "Can change owned event"),
        ]
        
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'event_id': self.id})

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Ticket for {self.event.title} - {self.user.username}"

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name