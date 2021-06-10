from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError

from payesh.dynamic_models import PersianDateField


def file_size(value):  # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    try:
        if value and value.size > limit:
            raise ValidationError('حجم فایل باید کمتر از 5 مگابایت باشد!')
    except:
        print(value.url + ' NOT FOUND!!!')


class User(AbstractUser):
    class Meta:
        verbose_name = 'استاد یا دانشجو'
        verbose_name_plural = 'استاد یا دانشجو'

    ROLES = (
        ('student', 'دانشجو'),
        ('teacher', 'استاد راهنما'),
        ('education', 'آموزش'),
        ('admin', 'مدیر گروه'),
    )
    role = models.CharField(max_length=15, choices=ROLES, default='student', verbose_name='نوع حساب')
    code_student = models.CharField(max_length=15, null=True, verbose_name='کد دانشجویی')
    code_meli = models.CharField(max_length=11, null=True, verbose_name='کد ملی')

    def fullname(self):
        return self.first_name + ' ' + self.last_name

    def project(self):
        return self.projects.first()

    def is_student(self):
        return self.role == 'student'

    def is_teacher(self):
        return self.role == 'teacher'

    def is_education(self):
        return self.role == 'education'

    def is_admin(self):
        return self.role == 'admin'

    def has_role(self, roles):

        return self.is_superuser or self.role in roles

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def find_by_std_code(std_code):
        return User.objects.filter(code_student=std_code).first()


class Project(models.Model):
    class Meta:
        verbose_name = 'پروژه'
        verbose_name_plural = 'پروژه ها'
        permissions = (
            ('can_project', 'مدیریت پروژه'),
        )

    title = models.CharField(max_length=255, verbose_name='عنوان')
    code = models.CharField(max_length=255, verbose_name='کد پروژه')
    start_date = PersianDateField(blank=True, null=True, verbose_name='تاریخ شروع')
    end_date = PersianDateField(blank=True, null=True, verbose_name='تاریخ پایان')
    score = models.FloatField(blank=True, null=True, verbose_name='نمره')
    progress = models.IntegerField(default=0, blank=True, verbose_name='درصد پیشرفت')
    teacher = models.ForeignKey(User, related_name='std_projects', on_delete=models.CASCADE,
                                verbose_name='استاد راهنما')
    user = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE,
                             verbose_name='دانشجو')
    is_ready = models.BooleanField(default=False, blank=True, verbose_name='آماده ثبت نمره')
    is_finish = models.BooleanField(default=False, blank=True, verbose_name='ثبت نمره')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title + ' - ' + self.user.get_full_name()


class Ticket(models.Model):
    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'

    title = models.CharField(max_length=255, verbose_name='عنوان')
    user = models.CharField(max_length=255, verbose_name='دانشجو')
    teacher = models.CharField(max_length=255, verbose_name='استاد راهنما')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')

    def __str__(self):
        return self.title


class Message(models.Model):
    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    text = models.TextField(blank=True, verbose_name='متن پیام')
    sender = models.CharField(max_length=255, verbose_name='فرستنده')
    file = models.FileField(blank=True, verbose_name='فایل', validators=[file_size])
    ticket = models.ForeignKey(Ticket, related_name='message', on_delete=models.CASCADE,
                               verbose_name='بخش')
    is_seen = models.BooleanField(blank=True, verbose_name='مشاهده شده')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.text
