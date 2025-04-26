from django.contrib.sitemaps import Sitemap
from .models import Event
from django.utils import timezone

class EventSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Event.objects.all()

    def lastmod(self, obj):
        # Use the updated_at field of the Event model or return the current time
        if hasattr(obj, 'updated_at'):
            return obj.updated_at
        else:
            # Return the current time if updated_at attribute is not available
            return timezone.now()
