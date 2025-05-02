from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'events', api_views.EventViewSet)
router.register(r'tags', api_views.TagViewSet)
router.register(r'tickets', api_views.TicketViewSet, basename='tickets')
router.register(r'comments', api_views.CommentViewSet)

# The API URLs are determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('upcoming/', api_views.upcoming_events, name='api-upcoming-events'),
    path('county/<str:county>/', api_views.events_by_county, name='api-events-by-county'),
    path('purchase-ticket/<int:event_id>/', api_views.purchase_ticket, name='api-purchase-ticket'),
] 