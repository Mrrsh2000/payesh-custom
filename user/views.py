from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import LoginView
from django.db.models import Q
# Create your views here.
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework.decorators import action
from rest_framework.response import Response

from payesh.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from payesh.dynamic_api import DynamicModelApi, CustomValidation
from payesh.logging import log
from payesh.utils import PermissionsApi
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
        """
        برای تغییر در برخی از فیلد های فرم استفاده میشود
        مانند تغییر کلاس css در فیلد های فرم یا تغییر پبغام های خطای فرم


        مثال:
           مثال تغییر attribute های فیلد

        .. code:: python

           form.fields['username'].required = True
           form.fields['username'].widget.attrs = {'class': 'form-control', 'placeholder': 'نام کاربری',
                                                'autocomplete': 'off'}


        مثال:
           مثال تغییر پیغام های خطا های فرم

        .. code:: python

           form.error_messages = {
               "invalid_login": "نام کاربری یا رمز عبور اشتباه !",
               "inactive": "دسترسی شما به سامانه غیر فعال شده است !",
               }

        """

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
    """
    برای ایجاد یک کاربر جدید در سامانه از این کلاس استفاده میشود

    Arguments:
        form_class(UserCreateForm):
          فرمی که کلاس از آن استفاده میشود
        template_name(str):
           آردس تمپلت مورد استفاده در کلاس
        success_url(str):
           آدرس url که در صورت موفق بودن فرم، کاربر به آن هدایت خواهد شد
    """
    model = User
    datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'شماره تماس', 'نقش ها', 'مورد تایید']


# class OtherUserList(LoginRequiredMixin, ListView):
#     model = User
#     template_name = 'user/other_user_list.html'
#     extra_context = {'title': 'لیست کاربران'}
#     ordering = 'id'


# class UserDeleteView(DynamicApiDeleteView):
#     model = User


class UserViewSet(DynamicModelApi):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    columns = ['id', 'username', 'first_name', 'last_name', 'role', 'code_student', 'code_meli']
    order_columns = ['id', 'username', 'first_name', 'last_name', 'role', 'code_student', 'code_meli']
    model = User
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    custom_perms = {
        'datatable': ['admin', 'education', 'teacher'],
        'create': ['admin', 'education', 'teacher'],
        'update': ['admin', 'education', 'teacher'],
        'destroy': ['admin', 'education', 'teacher'],
        'retrieve': ['admin', 'education', 'teacher'],
        'list': ['admin', 'education', 'teacher'],
    }

    def destroy(self, request, *args, **kwargs):
        selected_user = self.get_object()
        if not selected_user.is_student and not self.request.user.is_admin:
            raise CustomValidation('', 'شما دسترسی حذف مدیر گروه را ندارید!')
        else:
            return super().destroy(request, *args, **kwargs)


class UserCreateView(DynamicCreateView):
    model = User
    success_url = '/user/list'
    form = user_form(['username', 'password', 'first_name', 'last_name', 'groups'])
    datatableEnable = False

    def get_extra_context(self, context):
        gp, is_created = Group.objects.get_or_create(name="کارشناس")
        gp.permissions.set([x.id for x in Permission.objects.all()])
        gp.save()
        return super().get_extra_context(context)


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
