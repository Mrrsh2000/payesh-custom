from payesh.dynamic_api import DynamicModelApi
from payesh.settings import ROLES_JUST_ADMIN
from ticket.models import Ticket, Message
from ticket.serializers import TicketCreateSerializer, MessageCreateSerializer


class TicketViewSet(DynamicModelApi):
    columns = ['id', 'user', 'title', 'created_at', 'is_closed', ]
    order_columns = ['id', 'user', 'title', 'created_at', 'is_closed', ]
    model = Ticket
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer
    custom_perms = {
        'datatable': ROLES_JUST_ADMIN,
        'create': ROLES_JUST_ADMIN,
        'update': ROLES_JUST_ADMIN,
        'destroy': ROLES_JUST_ADMIN,
        'retrieve': ROLES_JUST_ADMIN,
        'list': ROLES_JUST_ADMIN,
    }

    def filter_queryset(self, qs):
        return super().filter_queryset(qs)

    def get_queryset(self):
        return self.queryset


class MessageViewSet(DynamicModelApi):
    columns = ['id', 'ticket', 'text', 'user', 'file', 'is_seen', 'is_seen_by_admin', 'created_at', ]
    order_columns = ['id', 'ticket', 'text', 'user', 'file', 'is_seen', 'is_seen_by_admin', 'created_at', ]
    model = Message
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
    custom_perms = {
        'datatable': ROLES_JUST_ADMIN,
        'create': ROLES_JUST_ADMIN,
        'update': ROLES_JUST_ADMIN,
        'destroy': ROLES_JUST_ADMIN,
        'retrieve': ROLES_JUST_ADMIN,
        'list': ROLES_JUST_ADMIN,
    }

    def filter_queryset(self, qs):
        return super().filter_queryset(qs)

    def get_queryset(self):
        return self.queryset
