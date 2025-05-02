# Import all views from specific modules to maintain compatibility
from .page_views import (
    styled_sitemap,
    home,
    contact,
    dashboard,
    profile,
    ChangeUsername,
)

from .event_views import (
    event_detail,
    event_create,
    event_update,
    event_delete,
    my_events,
    my_tickets,
)

from .payment_views import (
    purchase_tickets,
    payment_success,
    payment_cancel,
)

from .list_views import (
    get_all_events,
    event_list,
)

# This file now serves as a facade that imports and re-exports all views
# from their respective modules. This maintains backward compatibility
# while allowing for better code organization. 