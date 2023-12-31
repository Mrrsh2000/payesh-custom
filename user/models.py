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
        return User.objects.filter(role='teacher')

