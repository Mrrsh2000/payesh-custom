from payesh.dynamic import *
from .views import *

urlpatterns = [
    path('ticket/create', TicketCreateView.as_view(), name='ticket_create'),
    path('ticket/list', TicketListView.as_view(), name='ticket_list'),

    path('message/create/<int:pk>', MessageCreateView.as_view(), name='message_create'),
    path('message/list/<int:pk>', MessageListView.as_view(), name='message_list'),
]
