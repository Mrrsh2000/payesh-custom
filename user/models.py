from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    جدول کاربران شامل فیلد های زیر میباشد

    Arguments:
        mobile_number:
            امتیاز - از نوع کاراکتر است
    """

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
        permissions = (
            ('can_user', 'مدیریت کاربران'),
        )

    mobile_number = models.CharField(max_length=11, blank=True, null=True, verbose_name='شماره تماس')
    is_confirmed = models.BooleanField(default=True, verbose_name="مورد تایید")

    def fullname(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.first_name + ' ' + self.last_name
