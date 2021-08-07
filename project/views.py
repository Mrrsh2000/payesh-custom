from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi
from payesh.settings import ROLES_EXCEPT_STUDENT, ROLES_ADMIN_TEACHER, ROLES_JUST_ADMIN, ROLES_ADMIN_EDUCATION
from project.models import Project
from project.serializers import ProjectSerializer
from user.models import User


class ProjectViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'title', 'code', 'start_date', 'end_date', 'score', 'teacher', 'user',
               'is_ready', 'is_finish', 'created_at', ]
    order_columns = ['id', 'title', 'code', 'start_date', 'end_date', 'score', 'teacher',
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
        'education': ROLES_ADMIN_EDUCATION,
    }

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        if self.action == 'education':
            return qs.filter(is_ready=True)
        if self.request.user.is_teacher():
            return qs.filter(teacher=self.request.user)
        return qs

    def get_queryset(self):
        if self.action == 'self':
            return self.request.user.project()
        return self.queryset

    @action(methods=['post'], detail=False, url_path='number/(?P<pk>[^/.]+)')
    def number(self, request, pk, *args, **kwargs):
        project = Project.objects.filter(pk=pk).first()
        if request.user.role not in ROLES_ADMIN_TEACHER or not project or (
                request.user.is_teacher() and project.teacher != self.request.user):
            return Response({
                'message': 'شما دسترسی به ثبت نمره ندارید!'
            }, status=status.HTTP_404_NOT_FOUND)
        number = request.data.get('number')
        if number:
            number = float(number)
            if number <= 20 and number >= 0:
                project.score = float(number)
                project.save()
                return Response({
                    'message': 'نمره با موفقیت تغییر یافت!'
                }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'مشکلی پیش آمده است!'
        }, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=False, url_path='edu_toggle/(?P<pk>[^/.]+)')
    def edu_toggle(self, request, pk, *args, **kwargs):
        project = Project.objects.filter(pk=pk).first()
        if request.user.role not in ROLES_ADMIN_TEACHER or not project or (
                request.user.is_teacher() and project.teacher != self.request.user):
            return Response({
                'message': 'شما دسترسی به ثبت نمره ندارید!'
            }, status=status.HTTP_404_NOT_FOUND)
        project.is_ready = not project.is_ready
        project.save()
        return Response({
            'message': 'نمره با موفقیت تغییر یافت!'
        }, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False)
    def self(self, request, *args, **kwargs):
        pj = self.request.user.project()
        if pj:
            instance = pj
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response({}, status=HTTP_404_NOT_FOUND)

    @action(methods=['get', 'post'], detail=False)
    def education(self, request, *args, **kwargs):
        return self.datatable(request, *args, **kwargs)


class ProjectListView(DynamicListView):
    permission_required = ROLES_EXCEPT_STUDENT
    model = Project
    datatable_cols = ['#', 'عنوان', 'کد پروژه', 'تاریخ شروع', 'تاریخ پایان', 'نمره', 'استاد راهنما', 'دانشجو',
                      'آماده ثبت نمره', 'خاتمه یافته', 'تاریخ ایجاد', ]


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

    def has_permission(self):
        if self.request.user.is_teacher():
            return False if self.get_object().teacher != self.request.user else True
        return super().has_permission()

    def get_extra_context(self, context):
        context['form'].fields['teacher'].queryset = User.teachers()
        context['form'].fields['user'].queryset = User.students().filter(projects__isnull=True) | User.objects.filter(
            pk=self.get_object().user.pk)
        return super().get_extra_context(context)


class ProjectEducationListView(DynamicListView):
    permission_required = ROLES_ADMIN_EDUCATION
    model = Project
    datatable_cols = ['#', 'عنوان', 'کد پروژه', 'تاریخ شروع', 'تاریخ پایان', 'نمره', 'استاد راهنما', 'دانشجو',
                      'آماده ثبت نمره', 'خاتمه یافته', 'تاریخ ایجاد', ]
