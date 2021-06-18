from payesh.dynamic_api import DynamicModelApi
from payesh.settings import ROLES_JUST_ADMIN
from ticket.models import Ticket
from ticket.serializers import TicketCreateSerializer


class TicketViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'ticketname', 'first_name', 'last_name', 'role']
    order_columns = ['id', 'ticketname', 'first_name', 'last_name', 'role']
    model = Ticket
    queryset = Ticket.objects.exclude(role='student')
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
        return super().filter_queryset(qs).exclude(role='student')

    def get_queryset(self):
        return self.queryset
