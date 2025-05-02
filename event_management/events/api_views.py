from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import Event, Ticket, Tag, Comment
from .serializers import (
    EventSerializer, 
    EventCreateSerializer,
    TicketSerializer, 
    TagSerializer, 
    CommentSerializer
)
from .utils import extract_county, add_event_tags

class EventViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing Event instances."""
    queryset = Event.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location', 'county', 'categories']
    ordering_fields = ['date', 'price', 'capacity']
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return EventCreateSerializer
        return EventSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """Save the event and add tags."""
        event = serializer.save()
        # Extract county from location
        event.county = extract_county(event.location)
        # Add tags based on properties
        add_event_tags(event)
        event.save()
    
    def perform_update(self, serializer):
        """Update the event and refresh tags."""
        event = serializer.save()
        # Extract county from location
        event.county = extract_county(event.location)
        # Add tags based on updated properties
        add_event_tags(event)
        event.save()
        
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Tag instances."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class TicketViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Ticket instances."""
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return tickets for the current user only."""
        return Ticket.objects.filter(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and creating Comment instances."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_permissions(self):
        """
        Anonymous users can create comments but only authenticated users can view them.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
        
@api_view(['GET'])
def upcoming_events(request):
    """Return events that are coming up in the next 30 days."""
    now = timezone.now().date()
    events = Event.objects.filter(
        date__gte=now,
        date__lte=now + timezone.timedelta(days=30)
    ).order_by('date')[:10]
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def events_by_county(request, county):
    """Return events for a specific county."""
    events = Event.objects.filter(county__iexact=county)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_ticket(request, event_id):
    """Purchase a ticket for an event."""
    # Get the event
    event = get_object_or_404(Event, id=event_id)
    
    # Check if there's available capacity
    if event.capacity <= 0:
        return Response(
            {"detail": "This event is fully booked."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create a ticket
    ticket = Ticket.objects.create(
        user=request.user,
        event=event,
        title=event.title,
        price=event.price
    )
    
    # Decrease event capacity
    event.capacity -= 1
    event.save()
    
    # Return the ticket
    serializer = TicketSerializer(ticket)
    return Response(serializer.data, status=status.HTTP_201_CREATED) 