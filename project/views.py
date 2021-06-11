from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi
from payesh.settings import ROLES_EXCEPT_STUDENT
from project.models import Project
from project.serializers import ProjectSerializer
from user.models import User


class ProjectViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'title', 'code', 'start_date', 'end_date', 'score', 'progress', 'teacher', 'user',
               'is_ready', 'is_finish', 'created_at', ]
    order_columns = ['id', 'title', 'code', 'start_date', 'end_date', 'score', 'progress', 'teacher',
                     'user',
                     'is_ready', 'is_finish', 'created_at', ]
    model = Project
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    custom_perms = {
        'datatable': ROLES_EXCEPT_STUDENT,
        'create': ROLES_EXCEPT_STUDENT,
        'update': ROLES_EXCEPT_STUDENT,
        'destroy': ROLES_EXCEPT_STUDENT,
        'retrieve': ROLES_EXCEPT_STUDENT,
        'list': ROLES_EXCEPT_STUDENT,
    }

    def filter_queryset(self, qs):
        return super().filter_queryset(qs)

    def get_queryset(self):
        return self.queryset


class ProjectListView(DynamicListView):
    permission_required = ROLES_EXCEPT_STUDENT
    model = Project
    datatable_cols = ['#',
                      'عنوان',
                      'کد پروژه',
                      'تاریخ شروع',
                      'تاریخ پایان',
                      'نمره',
                      'درصد پیشرفت',
                      'استاد راهنما',
                      'دانشجو',
                      'آماده ثبت نمره',
                      'خاتمه یافته',
                      'تاریخ ایجاد',
                      ]


class ProjectCreateView(DynamicCreateView):
    model = Project
    success_url = '/project/list'
    datatableEnable = False
    permission_required = ROLES_EXCEPT_STUDENT
    form_fields = [
        'title',
        'code',
        'start_date',
        'end_date',
        'teacher',
        'user',
        'description',
    ]

    def get_extra_context(self, context):
        context['form'].fields['teacher'].queryset = User.teachers()
        context['form'].fields['user'].queryset = User.students().filter(projects__isnull=True)
        return super().get_extra_context(context)


class ProjectUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
    model = Project
    success_url = '/project/list'
    template_name = 'project/project_update.html'
    permission_required = ROLES_EXCEPT_STUDENT
    form_fields = [
        'title',
        'code',
        'start_date',
        'end_date',
        'teacher',
        'user',
        'description',
    ]
