from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.settings import ROLES_ADMIN_TEACHER
from ticket.models import Message, Ticket


class TicketListView(DynamicListView):
    permission_required = ROLES_ADMIN_TEACHER
    model = Ticket
    datatable_cols = ['#', 'کاربر', 'عنوان', 'تاریخ ایجاد', 'بسته شده', ]


class TicketCreateView(DynamicCreateView):
    model = Ticket
    success_url = '/ticket/list'
    datatableEnable = False
    permission_required = ROLES_ADMIN_TEACHER


class MessageListView(DynamicListView):
    permission_required = ROLES_ADMIN_TEACHER
    model = Message
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'نقش']


class MessageCreateView(DynamicCreateView):
    model = Message
    success_url = '/message/list'
    datatableEnable = False
    permission_required = ROLES_ADMIN_TEACHER
