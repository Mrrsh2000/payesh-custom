from django.contrib.auth.views import LoginView

from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi
from payesh.logging import log
from payesh.settings import ROLES_JUST_ADMIN
from user.forms import user_form
from user.models import User
from user.serializers import UserCreateSerializer


class UserLoginView(LoginView):
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
        res = super().form_valid(form)
        log(self.request.user, 1, 1, True)
        return res


class UserListView(DynamicListView):
    permission_required = ROLES_JUST_ADMIN
    model = User
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'نقش']
    model_name = 'اساتید'


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

    def filter_queryset(self, qs):
        return super().filter_queryset(qs).exclude(role='student')

    def get_queryset(self):
        return self.queryset


class UserCreateView(DynamicCreateView):
    model = User
    success_url = '/user/list'
    form = user_form(['username', 'password', 'first_name', 'last_name', 'role'])
    datatableEnable = False
    permission_required = ROLES_JUST_ADMIN
    model_name = 'اساتید'


class UserUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
    model = User
    form = user_form(['username', 'first_name', 'last_name', 'role'], update=True)
    success_url = '/user/list'
    template_name = 'user/user_update.html'
    permission_required = ROLES_JUST_ADMIN
    model_name = 'اساتید'


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
    model_name = 'اساتید'

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
