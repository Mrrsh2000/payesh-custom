from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import LoginView
from django.db.models import Q
# Create your views here.
from django.http import Http404
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework.decorators import action
from rest_framework.response import Response

from abresani.dynamic import DynamicCreateView, DynamicListView, DynamicUpdateView
from abresani.dynamic_api import DynamicModelApi, CustomValidation
from abresani.logging import log
from abresani.utils import PermissionsApi
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
    columns = ['id', 'username', 'first_name', 'last_name', 'mobile_number', 'groups', 'is_confirmed']
    order_columns = ['id', 'username', 'first_name', 'last_name', 'mobile_number', 'groups', 'is_confirmed']
    model = User
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    custom_perms = {
        'datatable': 'can_user',
        'create': 'can_user',
        'update': 'can_user',
        'destroy': 'can_user',
        'retrive': 'can_user',
        'list': 'can_user',
    }

    def get_object(self):
        if self.action == 'self':
            return self.request.user
        return super().get_object()

    @action(methods=['get', 'put'], detail=False)
    def self(self, request, *args, **kwargs):
        """
        از این متد برای برای ثبت نقش های کاربر و تعیین نوع کاربر استفاده میشود
        """
        if request._request.method == 'PUT':
            return self.update(request, *args, *kwargs)
        return Response(self.get_serializer(self.request.user).data)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if self.request.user == user:
            raise CustomValidation('', 'نمی توانید حساب کاربری خود را حذف کنید!')
        if not self.request.user.is_superuser and user.groups.filter(name='کارشناس'):
            raise CustomValidation('', 'شما دسترسی حذف کاربر کارشناس را ندارید!')
        return super().destroy(request, *args, **kwargs)


class UserDataTableView(PermissionsApi, BaseDatatableView):
    """
    برای نمایش کاربر کاشف در سامانه از این کلاس استفاده میشود

    Arguments:
        form_class(UserCreateForm):
          فرمی که کلاس از آن استفاده میشود
        template_name(str):
           آردس تمپلت مورد استفاده در کلاس
        success_url(str):
           آدرس url که در صورت موفق بودن فرم، کاربر به آن هدایت خواهد شد
    """
    model = User
    columns = ['id', 'username', 'first_name', 'last_name']
    user_permission = 'user.can_user'

    def filter_queryset(self, qs):
        """
        برای جستجو در عنوان آخرین وضیعت هاست

        Arguments:
            qs:
                کوئری مورد جستجو است
        """
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search))
        return qs


class UserCreateView(DynamicCreateView):
    """
    برای ایجاد یک کاربرجدید که عضو کاشف هست  در سامانه از این کلاس استفاده میشود

    Arguments:
        form_class(UserCreateForm):
          فرمی که کلاس از آن استفاده میشود
        template_name(str):
           آردس تمپلت مورد استفاده در کلاس
        success_url(str):
           آدرس url که در صورت موفق بودن فرم، کاربر به آن هدایت خواهد شد
    """
    model = User
    success_url = '/user/list'
    form = user_form(['username', 'password', 'first_name', 'last_name', 'mobile_number', 'groups'])
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
    form = user_form(['username', 'first_name', 'last_name', 'mobile_number', 'groups', 'is_confirmed'], update=True)
    success_url = '/user/list'
    template_name = 'user/user_update.html'


class SelfUpdateView(DynamicUpdateView):
    """
    این کلاس برای ویرایش کاربران کاشف استفاده می شود
    """
    model = User
    form = user_form(['username', 'first_name', 'last_name', 'mobile_number'], update=True)
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
