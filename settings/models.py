from django.db import models


class User(models.Model):
    """
    جدول یوزر شامل فیلد های زیر میباشد

    Arguments:
        title(models.CharField):
            عنوان - از نوع کاراکتر است
        created_at(models.DateTimeField):
            تاریخ ایجاد - از نوع تاریخ است
        updated_at(models.DateTimeField):
            تاریخ آخرین ویرایش - از نوع تاریخ است - میتواند خالی باشد
    """

    class Meta:
        verbose_name = 'شهرستان'
        verbose_name_plural = 'شهرستان ها'
        permissions = (
            ('can_city', 'مدیریت شهرستان'),
        )

    username = models.CharField(max_length=255, unique=True, verbose_name='نام کاربری')
    idCodeSTU = models.CharField(max_length=15, unique=True, verbose_name='کد دانشجویی')
    idCodeMELI = models.CharField(max_length=11, unique=True, verbose_name='کد ملی')
    Password = models.CharField(max_length=255, unique=True, verbose_name='پسوورد')
    Input = models.DateField(max_length=255, unique=True, verbose_name='ورودی')
    Role = models.IntegerField(unique=True, verbose_name='نوع')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.username


class Project(models.Model):
    """
    جدول پروژه ها شامل فیلد های زیر میباشد

    Arguments:
        title(models.CharField):
            عنوان - از نوع کاراکتر است
        created_at(models.DateTimeField):
            تاریخ ایجاد - از نوع تاریخ است
        updated_at(models.DateTimeField):
            تاریخ آخرین ویرایش - از نوع تاریخ است - میتواند خالی باشد
    """

    class Meta:
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش ها'
        permissions = (
            ('can_part', 'مدیریت بخش'),
        )

    title = models.CharField(max_length=255, verbose_name='عنوان')
    codeNumber = models.CharField(max_length=255, verbose_name='کد پروژه')
    startDate = models.DateField(auto_now_add=False, blank=True, verbose_name='تاریخ شروع')
    endDate = models.DateField(auto_now_add=False, blank=True, verbose_name='تاریخ پایان')
    score = models.FloatField(blank=True, verbose_name='نمره')
    progress = models.IntegerField(blank=True, verbose_name='درصد پیشرفت')
    professorHelper = models.ForeignKey(User, related_name='Project', on_delete=models.CASCADE,
                                        verbose_name='استاد راهنما')
    daneshjo = models.ForeignKey(User, related_name='project', on_delete=models.CASCADE,
                                 verbose_name='دانشجو')
    is_ready = models.BooleanField(blank=True, verbose_name='آماده')
    is_finish = models.BooleanField(blank=True, verbose_name='اتمام')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title


class Ticket(models.Model):
    """
    جدول شهر شامل فیلد های زیر میباشد

    Arguments:
        title(models.CharField):
            عنوان - از نوع کاراکتر است
        created_at(models.DateTimeField):
            تاریخ ایجاد - از نوع تاریخ است
        updated_at(models.DateTimeField):
            تاریخ آخرین ویرایش - از نوع تاریخ است - میتواند خالی باشد
    """

    class Meta:
        verbose_name = 'روستا'
        verbose_name_plural = 'روستا ها'
        permissions = (
            ('can_village', 'مدیریت روستا'),
        )

    title = models.CharField(max_length=255, verbose_name='عنوان')
    daneshjo = models.CharField(max_length=255, verbose_name='دانشجو')
    professorHelper = models.CharField(max_length=255, verbose_name='استاد راهنما')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title


class Message(models.Model):
    """
    جدول شهر شامل فیلد های زیر میباشد

    Arguments:
        title(models.CharField):
            عنوان - از نوع کاراکتر است
        created_at(models.DateTimeField):
            تاریخ ایجاد - از نوع تاریخ است
        updated_at(models.DateTimeField):
            تاریخ آخرین ویرایش - از نوع تاریخ است - میتواند خالی باشد
    """

    class Meta:
        verbose_name = 'دهستان'
        verbose_name_plural = 'دهستان ها'
        permissions = (
            ('can_town', 'مدیریت دهستان'),
        )

    title = models.CharField(max_length=255, verbose_name='متن پیام')
    sender = models.CharField(max_length=255, verbose_name='فرستنده')
    dateSend = models.DateTimeField(auto_now_add=False, verbose_name='تاریخ ارسال')
    file = models.FilePathField(blank=True, verbose_name='فایل')
    ticket = models.ForeignKey(Ticket, related_name='message', on_delete=models.CASCADE,
                               verbose_name='بخش')
    is_seen = models.BooleanField(blank=True, verbose_name='مشاهده شده')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title


class FileModel(models.Model):
    excel_file = models.FileField()
