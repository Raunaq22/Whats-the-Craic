from django.urls import path, include
from . import views
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from .views import home, contact, dashboard, profile, ChangeUsername
from django.conf import settings
from django.conf.urls.static import static
from .sitemaps import EventSitemap  

sitemaps = {
    'events': EventSitemap,  
}

urlpatterns = [
    path('events_list', views.event_list, name='event_list'),                      
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  
    path('event/create/', views.event_create, name='event_create'),
    path('event/<int:event_id>/update/', views.event_update, name='event_update'),
    path('event/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    
    path('home/', home, name='home'),
    path('', home, name='home'),
    path('contact-us/', contact, name='contact-us'),
    
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile, name='profile'),
    
    path('accounts/', include('allauth.urls')),
    path('accounts/change-username/', ChangeUsername.as_view(), name='account_change_username'),
    path('accounts/profile/', TemplateView.as_view(template_name='pages/profile.html'),name='profile'),
    
    path('my-events/', views.my_events, name='my_events'),
    
    path('event/<int:event_id>/purchase/', views.purchase_tickets, name='purchase_tickets'),
    
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    
    path('my_tickets/', views.my_tickets, name='my_tickets'),
    path('get-events/', views.get_all_events, name='get_all_events'),
    
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    )
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)