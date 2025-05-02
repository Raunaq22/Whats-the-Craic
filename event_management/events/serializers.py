from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, Ticket, Tag, Comment

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        
class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    class Meta:
        model = Tag
        fields = ['id', 'name']

class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""
    organizer = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location', 'date', 'time', 
            'organizer', 'image', 'capacity', 'price', 'categories', 
            'tags', 'county'
        ]
        
class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket model."""
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'event', 'title', 'price', 'date']
        
class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model."""
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'message', 'created_at']
        
# Serializers for write operations with simplified fields
class EventCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating Event objects."""
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'location', 'date', 'time',
            'capacity', 'price', 'categories', 'image'
        ]
        
    def create(self, validated_data):
        """Create and return a new event."""
        # Set the current user as the organizer
        user = self.context['request'].user
        event = Event.objects.create(organizer=user, **validated_data)
        return event 