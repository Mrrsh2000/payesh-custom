from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi
from payesh.settings import ROLES_EXCEPT_STUDENT
from user.forms import user_form
from user.models import User
from user.serializers import StudentCreateSerializer


class StudentViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'first_name', 'last_name', 'code_student', 'code_meli']
    order_columns = ['id', 'first_name', 'last_name', 'code_student', 'code_meli']
    model = User
    queryset = User.objects.filter(role='student')
    serializer_class = StudentCreateSerializer
    custom_perms = {
        'datatable': ROLES_EXCEPT_STUDENT,
        'create': ROLES_EXCEPT_STUDENT,
        'update': ROLES_EXCEPT_STUDENT,
        'destroy': ROLES_EXCEPT_STUDENT,
        'retrieve': ROLES_EXCEPT_STUDENT,
        'list': ROLES_EXCEPT_STUDENT,
    }

    def filter_queryset(self, qs):
        return super().filter_queryset(qs).filter(role='student')

    def get_queryset(self):
        return self.queryset


class StudentListView(DynamicListView):
    model = User
    datatable_cols = ['#', 'نام', 'نام خانوادگی', 'شماره دانشجویی', 'کد ملی']
    permission_required = ROLES_EXCEPT_STUDENT
    model_name = 'دانشجویان'
    template_name = 'student/student_list.html'


class StudentCreateView(DynamicCreateView):
    model = User
    success_url = '/student/list'
    form = user_form(['first_name', 'last_name', 'code_student', 'code_meli'])
    datatableEnable = False
    permission_required = ROLES_EXCEPT_STUDENT
    template_name = 'student/student_create.html'


class StudentUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
    model = User
    form = user_form(['username', 'first_name', 'last_name', 'code_student', 'code_meli'], update=True)
    success_url = '/student/list'
    template_name = 'student/student_update.html'
    permission_required = ROLES_EXCEPT_STUDENT
