from django.db import models

from payesh.dynamic_models import PersianDateField
from user.models import User


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
