from django.db import models


# Create your models here.
from user.models import User


class Log(models.Model):
    """
    جدول لاگ شامل فیلد های زیر میباشد

    Arguments:
        title:
            عنوان - از نوع کاراکتر هست
        user:
            کاربر - کلید خارجی به جدول کاربر است
        priority:
            اولویت - از نوع عددی است
        status:
            وضعیت - از نوع بولین است
        discription:
            توضیحات - از نوع متن است
        created_at:
            تاریخ ایجاد - از نوع تاریخ است
        updated_at:
            تاریخ آخرین ویرایش - از نوع تاریخ است - میتواند خالی باشد
    """

    class Meta:
        verbose_name = 'گزارشات سامانه'
        verbose_name_plural = 'گزارشات سامانه'
        permissions = (
            ('can_add_log', 'افزودن گزارشات سامانه'),
            ('can_edit_log', 'ویرایش گزارشات سامانه'),
            ('can_view_log', 'مشاهده گزارشات سامانه'),
        )

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, related_name='logs', on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.IntegerField()
    status = models.BooleanField(default=True)
    ip = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title
