"""
این ماژول شامل توابع و کلاس های کاربردی در نرم
افزار میشود
"""
import re
from random import randint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.views import View
import datetime
from django.conf import settings
from django.db.models import Q
from django.apps import apps
from rest_framework_simplejwt.tokens import RefreshToken

from abresani.settings import JWT_AUTH

from abresani.logging import log
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect

from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView


class CustomAccessMixin(AccessMixin):
    def handle_no_permission(self):
        messages.error(self.request, 'شما دسترسی ' + Permission.objects.filter(
            codename=self.permission_required.split('.')[1]).last().name + ' را ندارید')
        return redirect('/')


class CustomPermissionRequiredMixin(CustomAccessMixin):
    """Verify that the current user has all specified permissions."""
    permission_required = None

    def get_permission_required(self):
        """
        Override this method to override the permission_required attribute.
        Must return an iterable.
        """
        if self.permission_required is None:
            raise ImproperlyConfigured(
                '{0} is missing the permission_required attribute. Define {0}.permission_required, or override '
                '{0}.get_permission_required().'.format(self.__class__.__name__)
            )
        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def jalali_to_gregorian(jy, jm, jd):
    if (jy > 979):
        gy = 1600
        jy -= 979
    else:
        gy = 621
    if (jm < 7):
        days = (jm - 1) * 31
    else:
        days = ((jm - 7) * 30) + 186
    days += (365 * jy) + ((int(jy / 33)) * 8) + (int(((jy % 33) + 3) / 4)) + 78 + jd
    gy += 400 * (int(days / 146097))
    days %= 146097
    if (days > 36524):
        gy += 100 * (int(--days / 36524))
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (int(days / 1461))
    days %= 1461
    if (days > 365):
        gy += int((days - 1) / 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13):
        v = sal_a[gm]
        if (gd <= v):
            break
        gd -= v
        gm += 1
    return [gy, gm, gd]


def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if (gy > 1600):
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    if (gm > 2):
        gy2 = gy + 1
    else:
        gy2 = gy
    days = (365 * gy) + (int((gy2 + 3) / 4)) - (int((gy2 + 99) / 100)) + (int((gy2 + 399) / 400)) - 80 + gd + g_d_m[
        gm - 1]
    jy += 33 * (int(days / 12053))
    days %= 12053
    jy += 4 * (int(days / 1461))
    days %= 1461
    if (days > 365):
        jy += int((days - 1) / 365)
        days = (days - 1) % 365
    if (days < 186):
        jm = 1 + int(days / 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + int((days - 186) / 30)
        jd = 1 + ((days - 186) % 30)
    return [jy, jm, jd]


def change_date_to_english(value, mtime, mode=1):
    """
    برای تبدیل تاریخ شمسی به میلادی استفاده میشود
    تاریخ میلادی را دریافت میکند و تاریخ شمسی را در
    قالب رشته خروجی میدهد

    Arguments:
        value(str):
            تاریخ شمسی
        mtime(str):
            زمان
        mode(int):
            حالت تبدیل را مشخص میکند
    """
    if mode == 2:
        y, m, d = unidecode(value).split('/')
        time = mtime.split(':')
        s = 0
        try:
            if time[2] is not None:
                s = time[2]
        except:
            pass
        pdate = jalali_to_gregorian(int(y), int(m), int(d))
        date_time = datetime.datetime(pdate[0], pdate[1], pdate[2], int(time[0]), int(time[1]), int(s))
        return date_time
    value = unidecode(value)
    stime, date = value.split(' ')
    stime = unidecode(stime)
    year, month, day = date.split('/')
    date = jalali_to_gregorian(int(year), int(month), int(day))
    string_date = "{y} {m} {d} ".format(y=date[0], m=date[1], d=date[2])
    string_date_time = string_date + stime
    date_time = datetime.datetime.strptime(string_date_time, "%Y %m %d %H:%M:%S")
    return date_time


def change_date_to_english_mamad(value, mode=1):
    """
    برای تبدیل تاریخ شمسی به میلادی استفاده میشود
    تاریخ میلادی را دریافت میکند و تاریخ شمسی را در
    قالب رشته خروجی میدهد

    Arguments:
        value(str):
            تاریخ شمسی
        mode(int):
            حالت تبدیل را مشخص میکند
    """
    if mode == 2:
        try:
            y, m, d = unidecode(value).split('/')
        except:
            y, m, d = unidecode(value).split('-')
        pdate = jalali_to_gregorian(int(y), int(m), int(d))
        date_time = datetime.date(pdate[0], pdate[1], pdate[2])
        return date_time
    value = unidecode(value)
    stime, date = value.split(' ')
    stime = unidecode(stime)
    year, month, day = date.split('/')
    date = jalali_to_gregorian(int(year), int(month), int(day))
    string_date = "{y} {m} {d} ".format(y=date[0], m=date[1], d=date[2])
    string_date_time = string_date + stime
    date_time = datetime.datetime.strptime(string_date_time, "%Y %m %d %H:%M:%S")
    return date_time


def custom_change_date(value, mode=1):
    """
    برای تبدیل تاریخ استفاده میشود
    تاریخ را دریافت میکند و فرمت مورد نیاز را در
    قالب خروجی مورد نظر میدهد

    Arguments:
        value(str):
            تاریخ
        mode(int):
            حالت تبدیل را مشخص میکند
    """
    # Change Str Date to Str Persian Date
    if mode == 2:
        value = str(unidecode(str(value)))
        year, month, day = value.split('-')
        date = gregorian_to_jalali(int(year), int(month), int(day))
        string_date = "{y}/{m}/{d}".format(y=date[0], m=date[1], d=date[2])
        return string_date

    # Str Persian DateTime to DjangoDateTime
    if mode == 3:
        d = unidecode(value).split(' -- ')
        y, m, day = d[0].split('/')
        hour, min = d[1].split(':')
        pdate = jalali_to_gregorian(int(y), int(m), int(day))
        date_time = datetime.datetime(int(pdate[0]), int(pdate[1]), int(pdate[2]), int(hour), int(min))
        return date_time
    # Change DjangoDateTime to PersianDateTime
    if mode == 4:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        hour, min, sec = time[0].split(':')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{y}/{m}/{d} {h}:{min}:{s}".format(y=pdate[0], m=pdate[1], d=pdate[2], h=hour, min=min, s=sec)
        return date_time
    # Change DateTime To DjangoDateTime
    if mode == 5:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        hour, min, sec = time[0].split(':')
        date_time = datetime.datetime(int(y), int(m), int(day), int(hour), int(min), int(sec))
        return date_time
    # Change Persian Date to DjangoDate
    if mode == 6:
        y, m, day = value.split('/')
        pdate = jalali_to_gregorian(int(y), int(m), int(day))
        djangodate = datetime.date(int(pdate[0]), int(pdate[1]), int(pdate[2]))
        return djangodate
    # Change DjangoDateTime to PersianMonthDay
    if mode == 7:
        monthlist = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن',
                     'اسفند']
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{d} {m}".format(m=monthlist[pdate[1] - 1], d=pdate[2])
        return date_time

    # Change DjangoDateTime to PersianDateTime For Tables
    if mode == 8:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        hour, min, sec = time[0].split(':')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{h}:{min}:{s} {y}/{m}/{d}".format(y=pdate[0], m=pdate[1], d=pdate[2], h=hour, min=min, s=sec)
        return date_time

    # Change DjangoDateTime to Year
    if mode == 9:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        return pdate[0]

    # Change DjangoDateTime to Month
    if mode == 10:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        return pdate[1]

    if mode == 11:
        d = str(value).split(' ')
        y, m, day = d[0].split('-')
        time = d[1].split('+')
        time = time[0].split('.')
        hour, min, sec = time[0].split(':')
        pdate = gregorian_to_jalali(int(y), int(m), int(day))
        date_time = "{y}-{m}-{d} {h}:{min}:{s}".format(y=pdate[0], m=pdate[1], d=pdate[2], h=hour, min=min, s=sec)
        return date_time

    # 1398/3 => (1398/3/31 : 23:59:59) => DjangoDateTime
    if mode == 12:
        pdate = []
        y, m = value.split('/')
        for i in [28, 29, 30, 31]:
            if jalali_to_gregorian(int(y), int(m), i)[2] != jalali_to_gregorian(int(y), int(m) + 1, 1)[2]:
                pdate = jalali_to_gregorian(int(y), int(m), i)
        djangodate = datetime.datetime(int(pdate[0]), int(pdate[1]), int(pdate[2]), 23, 59, 59)
        return djangodate

    # 1398/3 => (1398/3/1 : 00:00:00) => DjangoDateTime
    if mode == 14:
        y, m = value.split('/')
        pdate = jalali_to_gregorian(int(y), int(m), 1)
        djangodate = datetime.datetime(int(pdate[0]), int(pdate[1]), int(pdate[2]), 00, 00, 00)
        return djangodate

    # get Current Persian Date => [ 1399 , 4 , 16 ]
    if mode == 13:
        now = datetime.datetime.now()
        return gregorian_to_jalali(now.year, now.month, now.day)
    return 0


def change_date_to_persian(value, mtime, mode=1):
    """
    برای تبدیل تاریخ میلادی به شمسی استفاده میشود
    تاریخ میلادی را دریافت میکند و تاریخ شمسی را در
    قالب رشته خروجی میدهد

    Arguments:
        value(str):
            تاریخ میلادی
        mtime(str):
            زمان
        mode(int):
            حالت تبدیل را مشخص میکند
    """
    year = ""
    month = ""
    day = ""
    if mode == 2:
        value = str(unidecode(str(value)))
        year, month, day = value.split('-')
        h, mi, s, rest = mtime.split(':')
        if s.find('.') != -1:
            s, unusf = s.split('.')
        if s.find('+') != -1:
            s, unusf = s.split('+')
    date = gregorian_to_jalali(int(year), int(month), int(day))
    string_date = "{y}/{m}/{d}--{h}:{M}:{s}".format(y=date[0], m=date[1], d=date[2], h=h, M=mi, s=s)
    return string_date

    value = str(unidecode(str(value)))
    date, stime = str(value).split(' ')
    stime = unidecode(stime)
    date = str(date)
    year, month, day = date.split('-')
    date = gregorian_to_jalali(int(year), int(month), int(day))
    string_date = "{stime} {y}/{m}/{d}".format(y=date[0], m=date[1], d=date[2], stime=stime)
    return string_date


def change_date_to_persian_mamad(value, mode=1):
    """
    برای تبدیل تاریخ میلادی به شمسی استفاده میشود
    تاریخ میلادی را دریافت میکند و تاریخ شمسی را در
    قالب رشته خروجی میدهد

    Arguments:
        value(str):
            تاریخ میلادی
        mtime(str):
            زمان
        mode(int):
            حالت تبدیل را مشخص میکند
    """
    year = ""
    month = ""
    day = ""
    if mode == 2:
        value = str(unidecode(str(value)))
        year, month, day = value.split('-')
    date = gregorian_to_jalali(int(year), int(month), int(day))
    string_date = "{y}/{m}/{d}".format(y=date[0], m=date[1], d=date[2])
    return string_date

    value = str(unidecode(str(value)))
    date = str(value)
    date = str(date)
    year, month, day = date.split('-')
    date = gregorian_to_jalali(int(year), int(month), int(day))
    string_date = "{y}/{m}/{d}".format(y=date[0], m=date[1], d=date[2])
    return string_date


class LoginRequiredMixin(object):
    """
    این کلاس در بررسی لاگین بودن یا نبودن
    کاربر کاربرد دارد.
    """

    @classmethod
    def as_view(cls, **kwargs):
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        return login_required(view)


class CustomDeleteView(LoginRequiredMixin, View):
    """
    این کلاس برای حذف از همه مدل ها استفاده میشود
    """

    def get_model(self):
        """
        مدل را خالی ارسال میکند
        """
        return None

    def get(self, request, pk):
        """
         برای حذف کردن رکورد از جدول پایگاه داده استفاده میشود

         Arguments:
             request:
                درخواست ارسال شده به صفحه است
             pk:
                مقدار کلید اصلی رکور است
        """
        try:
            log(self.request.user, 3, 5, True, self.get_model().objects.get(pk=pk))
            self.before_delete()
            self.get_model().objects.get(pk=pk).delete()
            self.after_delete()
            return HttpResponse(status=200)
        except Exception as e:
            raise Http404

    def after_delete(self):
        pass

    def before_delete(self):
        pass


def clean_cost(cost: str):
    cost = cost.split(' ')
    fcost = cost[0].split(',')
    ffcost = ''.join(fcost)
    return ffcost


def gd(what, _default):
    """
    اگر what خالی باشد ویا موجود نباشد
    مقدار _default برگردانده میشود
    Args:
        what:
        _default:

    Returns:

    """
    if what:
        return what
    return _default


def dynamic_permision():
    apps1 = assignable_app_names()
    permission = dict()
    for app in apps1:

        data_to_return = []
        if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
            perms = Permission.objects.filter(~Q(name__icontains='can'), content_type__app_label=app.app_label)
        else:
            perms = Permission.objects.filter(~Q(name__icontains='can'), content_type__app_label=app['app_label'])

        for perm in perms:
            data_to_return.append(perm)
        if len(data_to_return) != 0:
            if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
                permission[apps.get_app_config(app.app_label).verbose_name] = data_to_return
            else:
                permission[apps.get_app_config(app['app_label']).verbose_name] = data_to_return

    return permission


def assignable_app_names():
    if settings.DATABASES['default']['ENGINE'] != 'django.db.backends.sqlite3':
        apps1 = ContentType.objects.filter().distinct('app_label')
    else:
        apps1 = ContentType.objects.filter().values('app_label').distinct()
    return apps1


def is_valid_iran_code(input):
    if not re.search(r'^\d{10}$', input):
        return False

    check = int(input[9])
    s = sum([int(input[x]) * (10 - x) for x in range(9)]) % 11
    return (s < 2 and check == s) or (s >= 2 and check + s == 11)


class PermissionsApi(APIView):
    user_permission = None

    def check_permissions(self, request):
        """
         برای دادن پرمیشن ها به هر کاربر برای حق دسترسی به قسمت های مختلف
        """
        if not self.request.user.is_authenticated:
            self.permission_denied(
                request, message=getattr('Login Required', 'message', None)
            )
        if self.user_permission:
            exists = self.request.user.user_permissions.filter(
                codename=self.user_permission.split('.')[1]).exists()
            if not self.request.user.is_superuser and not exists:
                self.permission_denied(
                    request, message=getattr(self.user_permission, 'message', None)
                )


def getToken(user):
    return RefreshToken.for_user(user)


def checkEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


def has_numbers(string):
    #  hasNumbers("I own 1 dog") => True
    #  hasNumbers("I own no dog") => False
    return any(char.isdigit() for char in string)
