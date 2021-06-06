from django.contrib.auth.views import LoginView

from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi
from payesh.logging import log
from payesh.settings import ROLES_EXCEPT_STUDENT, ROLES_JUST_ADMIN
from user.forms import user_form
from user.models import User
from user.serializers import UserCreateSerializer


class UserLoginView(LoginView):
    """
    برای لاگین شدن کاربر استفاده میشود و
    از LoginView خود جانگو و فرم آن استفاده میکند

    """
    template_name = 'login.html'

    def get_form(self, form_class=None):
        form = super(UserLoginView, self).get_form(form_class)
        form.error_messages = {
            "invalid_login": "نام کاربری یا رمز عبور اشتباه !",
            "inactive": "دسترسی شما به سامانه غیر فعال شده است !",
        }

        form.fields['username'].required = True
        form.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'نام کاربری',
                                                'autocomplete': 'off'}
        form.fields['username'].error_messages = {
            'required': 'نام کاربری را وارد کنید'
        }

        form.fields['password'].required = True
        form.fields['password'].widget.attrs = {'class': 'form-control form-control-last', 'placeholder': 'رمز عبور',
                                                'type': 'password'}
        form.fields['password'].error_messages = {
            'required': 'رمز عبور را وارد کنید'
        }

        return form

    def form_valid(self, form):
        """
        برای لاگ کردن ورود کاربر استفاده میشود

        Arguments:
            form:
                فرم ارسال شده است
        """
        res = super().form_valid(form)
        log(self.request.user, 1, 1, True)
        return res


class UserListView(DynamicListView):
    model = User
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'شماره تماس', 'نقش ها', 'مورد تایید']


class StudentListView(DynamicListView):
    model = User
    datatable_cols = ['#', 'نام', 'نام خانوادگی', 'شماره دانشجویی', 'کد ملی']


class UserViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'username', 'first_name', 'last_name', 'role']
    order_columns = ['id', 'username', 'first_name', 'last_name', 'role']
    model = User
    queryset = User.objects.exclude(role='student')
    serializer_class = UserCreateSerializer
    custom_perms = {
        'datatable': ROLES_JUST_ADMIN,
        'create': ROLES_JUST_ADMIN,
        'update': ROLES_JUST_ADMIN,
        'destroy': ROLES_JUST_ADMIN,
        'retrieve': ROLES_JUST_ADMIN,
        'list': ROLES_JUST_ADMIN,
    }

    def get_queryset(self):
        return self.queryset


class StudentViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'first_name', 'last_name', 'code_student', 'code_meli']
    order_columns = ['id', 'first_name', 'last_name', 'code_student', 'code_meli']
    model = User
    queryset = User.objects.filter(role='student')
    serializer_class = UserCreateSerializer
    custom_perms = {
        'datatable': ROLES_EXCEPT_STUDENT,
        'create': ROLES_EXCEPT_STUDENT,
        'update': ROLES_EXCEPT_STUDENT,
        'destroy': ROLES_EXCEPT_STUDENT,
        'retrieve': ROLES_EXCEPT_STUDENT,
        'list': ROLES_EXCEPT_STUDENT,
    }

    def get_queryset(self):
        return self.queryset


class UserCreateView(DynamicCreateView):
    model = User
    success_url = '/user/list'
    form = user_form(['username', 'password', 'first_name', 'last_name', 'role'])
    datatableEnable = False
    permission_required = ROLES_JUST_ADMIN


class StudentCreateView(DynamicCreateView):
    model = User
    success_url = '/user/list'
    form = user_form(['first_name', 'last_name', 'code_student', 'code_meli'])
    datatableEnable = False
    permission_required = ROLES_EXCEPT_STUDENT


class UserUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
    model = User
    form = user_form(['username', 'first_name', 'last_name', 'groups'], update=True)
    success_url = '/user/list'
    template_name = 'user/user_update.html'


class SelfUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
    model = User
    form = user_form(['username', 'first_name', 'last_name'], update=True)
    success_url = '/'
    template_name = 'user/user_update.html'
    extra_context = {
        'self': True
    }

    def get_object(self, queryset=None):
        return self.request.user

# class RegisterView(CreateView):
#     form_class = user_form(['username', 'email', 'password'])
#     template_name = 'login.html'
#     success_url = '/'
#
#     def form_valid(self, form):
#         res = super(RegisterView, self).form_valid(form)
#
#         login(self.request, self.object)
#
#         return res


# class RegisterApiView(MessageApiResponseMixin, generics.CreateAPIView):
#     serializer_class = UserRegisterSerializer
#     permission_classes = []
#     success_message = 'ثبت نام شما با موفقیت انجام شد'
#
