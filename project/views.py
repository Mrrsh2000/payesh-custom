from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi
from payesh.settings import ROLES_EXCEPT_STUDENT
from project.models import Project
from project.serializers import ProjectSerializer


class ProjectViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'projectname', 'first_name', 'last_name', 'role']
    order_columns = ['id', 'projectname', 'first_name', 'last_name', 'role']
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
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'نقش']
    model_name = 'اساتید'


class ProjectCreateView(DynamicCreateView):
    model = Project
    success_url = '/project/list'
    datatableEnable = False
    permission_required = ROLES_EXCEPT_STUDENT
    model_name = 'اساتید'


class ProjectUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
    model = Project
    success_url = '/project/list'
    template_name = 'project/project_update.html'
    permission_required = ROLES_EXCEPT_STUDENT
    model_name = 'اساتید'
