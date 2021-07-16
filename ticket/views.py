from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.settings import ROLES_ADMIN_TEACHER
from ticket.models import Message, Ticket
from user.models import User


class TicketListView(DynamicListView):
    permission_required = ROLES_ADMIN_TEACHER
    model = Ticket
    datatable_cols = ['#', 'کاربر', 'عنوان', 'تاریخ ایجاد', 'بسته شده', ]


class TicketCreateView(DynamicCreateView):
    model = Ticket
    success_url = '/ticket/ticket/list'
    permission_required = ROLES_ADMIN_TEACHER
    form_fields = ['title', 'user']
    # updateURL = '/ticket/ticket/update/0'

    def get_extra_context(self, context):
        context['form'].fields['user'].queryset = User.students()
        return super().get_extra_context(context)


class TicketUpdateView(DynamicUpdateView):
    model = Ticket
    success_url = '/ticket/ticket/list'
    template_name = 'settings/dynamic/update.html'
    permission_required = ROLES_ADMIN_TEACHER
    form_fields = ['title', 'user', 'is_closed']

    def get_extra_context(self, context):
        context['form'].fields['user'].queryset = User.students()
        context['updateApiURL'] = '/api/v1/ticket/' + str(self.kwargs['pk']) + '/'
        context['successURL'] = self.success_url
        return super().get_extra_context(context)


class MessageListView(DynamicListView):
    permission_required = ROLES_ADMIN_TEACHER
    model = Message
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'نقش']


class MessageCreateView(DynamicCreateView):
    model = Message
    success_url = '/message/list'
    datatableEnable = False
    permission_required = ROLES_ADMIN_TEACHER
