from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, render_to_response
from django.utils import timezone
# @login_required
from django.views import View
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from payesh.logging import log
from payesh.utils import LoginRequiredMixin, checkEmail, getToken
from user.models import User
import re


def my_custom_page_not_found_view(request, *args, **argv):
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


@login_required
def index(request):
    """
    برای  نمایش صفحه اصلی سامانه است

    Arguments:
        request:
            درخواست ارسال شده است
    """
    return render(request, 'index.html')


class CompleteTemplateView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        return render(self.request, 'complete.html')


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


class NotFound404(TemplateView):
    """
    این کلاس برای ایجاد افراد حقوقی استفاده میشود

    Arguments:
        template_name(str):
            آدرس تمپلیتی که کلاس از ان استفاده میکند
        form_class(ModelForm):
            فرمی که کلاس از آن استفاده میکند را مشخص میکند
        success_url(str):
            آدرسی که پس از موفقیت صفحه به ان منتقل میشود.
    """
    template_name = '404.html'


@login_required
def user_logout(request):
    """
    برای خروج کاربر یا اصطلاحاً لاگ آوت استفاده میشود
    و پس از لاگ اوت کاربر را به صفحه لاگین هدایت میکند

    Arguments:
        request:
           درخواست ارسال شده به صفحه است

    """
    request.user.last_logout = timezone.now()
    request.user.last_activity = None
    request.user.save()
    log(request.user, 1, 2, True)
    logout(request)

    return redirect('/')


class UserLogout(LoginRequiredMixin, View):
    """
    برای خروج کاربر یا اصطلاحاً لاگ آوت استفاده میشود
    و پس از لاگ اوت کاربر را به صفحه لاگین هدایت میکند

    Arguments:
        request:
           درخواست ارسال شده به صفحه است

    """

    def get(self, request):
        request.user.last_logout = timezone.now()
        request.user.last_activity = timezone.now()
        request.user.save()
        log(request.user, 1, 2, True)
        logout(request)

        return redirect('/')


class SignUp(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        data = {}

        # email = self.request.data.get('email')
        mobile_number = self.request.data.get('mobile_number')
        password = self.request.data.get('password')
        username = self.request.data.get('username')
        first_name = self.request.data.get('first_name')
        last_name = self.request.data.get('last_name')
        if not first_name:
            return Response({'first_name': ['نام الزامی می باشد']},
                            status=status.HTTP_400_BAD_REQUEST)
        if not last_name:
            return Response({'last_name': ['نام خانوادگی الزامی می باشد']},
                            status=status.HTTP_400_BAD_REQUEST)
        if not username or len(username) < 3 or not re.match("^[a-zA-Z0-9_.-]+$", username):
            return Response({'username': ['نام کاربری حداقل باید 3 حرفی و فقط حروف و عدد باشد']},
                            status=status.HTTP_400_BAD_REQUEST)
        if not password or len(password) < 6:
            return Response({'username': ['رمز عبور حداقل باید 6 حرفی و فقط حروف و عدد باشد']},
                            status=status.HTTP_400_BAD_REQUEST)
        # if not checkEmail(email):
        #     return Response({'email': ['ایمیل وارد شده معتبر نمی باشد']}, status=status.HTTP_400_BAD_REQUEST)
        if not mobile_number or not mobile_number.isnumeric() or len(mobile_number) != 11:
            return Response({'mobile_number': ['شماره تماس وارد شده معتبر نمی باشد']},
                            status=status.HTTP_400_BAD_REQUEST)
        # elif User.objects.filter(email=email).exists():
        #     return Response({'email': ['ایمیل وارد شده قبلا در سامانه ثبت شده است!']},
        #                     status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'username': ['این نام کاربری قبلا در سامانه ثبت شده است!']},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User()
        # user.email = email
        user.password = make_password(password)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.mobile_number = mobile_number
        user.is_confirmed = False
        user.save()

        refresh = getToken(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        login(request, user)
        return Response(data, status=status.HTTP_200_OK)
