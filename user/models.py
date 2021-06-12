from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


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
        if self.role == 'student':
            return self.first_name + ' ' + self.last_name + f' ( {self.code_student} ) '
        return self.first_name + ' ' + self.last_name

    @staticmethod
    def find_by_std_code(std_code):
        return User.objects.filter(code_student=std_code).first()

    @staticmethod
    def students():
        return User.objects.filter(role='student')

    @staticmethod
    def teachers():
        return User.objects.exclude(role='student')


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
