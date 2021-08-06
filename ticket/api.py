from django.http import JsonResponse, Http404
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from payesh.dynamic_api import DynamicModelApi
from payesh.settings import ROLES_JUST_ADMIN
from payesh.utils import custom_change_date
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
        # 'messages': ROLES,
    }

    @action(methods=['get'], detail=False, url_path='ticket/(?P<pk>[^/.]+)')
    def ticket(self, request, pk, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=pk)
        if ticket.user != self.request.user and self.request.user.is_student():
            raise Http404()
        messages = ticket.messages.all().order_by('pk')
        res = [
            {
                'pk': msg.pk,
                'text': msg.text,
                'is_admin': False if msg.user.is_student() else True,
                'file': msg.file.url if msg.file else None,
                'is_seen': msg.is_seen,
                'is_seen_by_admin': msg.is_seen_by_admin,
                'created_at': custom_change_date(msg.created_at, 4),
            } for msg in messages
        ]
        return JsonResponse({'response': res, 'ticket': {
            'fullname': ticket.user.get_full_name(),
            'title': ticket.title,
            'is_closed': ticket.is_closed,
            'created_at': custom_change_date(ticket.created_at, 4),
        }})

    def filter_queryset(self, qs):
        return super().filter_queryset(qs)

    def get_queryset(self):
        return self.queryset
