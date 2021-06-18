from django.db import models
from rest_framework.exceptions import ValidationError

from user.models import User


def file_size(value):  # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    try:
        if value and value.size > limit:
            raise ValidationError('حجم فایل باید کمتر از 10 مگابایت باشد!')
    except:
        print(value.url + ' NOT FOUND!!!')


class Ticket(models.Model):
    class Meta:
        verbose_name = 'پیام سیستمی'
        verbose_name_plural = 'پیام های سیستمی'
        permissions = (
        )

    user = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE, verbose_name='کاربر')
    title = models.CharField(max_length=255, verbose_name='عنوان')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    is_closed = models.BooleanField(default=False, verbose_name='بسته شده')

    def __str__(self):
        return self.title + ' (' + str(self.user.username) + ')'


class Message(models.Model):
    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
        permissions = (
        )

    ticket = models.ForeignKey('Ticket', related_name='messages', on_delete=models.CASCADE, verbose_name='تیکت')
    text = models.TextField(verbose_name='متن پیام')
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE, verbose_name='کاربر')
    file = models.FileField(upload_to='messages/', blank=True, null=True, verbose_name="فایل", validators=[file_size])
    is_seen = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_seen_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط مدیر')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='زمان ارسال')

    def __str__(self):
        return self.ticket.title + ' - ' + self.user.get_full_name()
