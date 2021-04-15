from django.db import models


class City(models.Model):
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
        verbose_name = 'شهرستان'
        verbose_name_plural = 'شهرستان ها'
        permissions = (
            ('can_city', 'مدیریت شهرستان'),
        )

    title = models.CharField(max_length=255, unique=True, verbose_name='عنوان')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title


class Part(models.Model):
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
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش ها'
        permissions = (
            ('can_part', 'مدیریت بخش'),
        )

    title = models.CharField(max_length=255, verbose_name='عنوان')
    father = models.ForeignKey(City, related_name='parts', on_delete=models.CASCADE,
                               verbose_name='شهر')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title


class Town(models.Model):
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

    title = models.CharField(max_length=255, verbose_name='عنوان')
    father = models.ForeignKey(Part, related_name='towns', on_delete=models.CASCADE,
                               verbose_name='بخش')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title


class Village(models.Model):
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
    father = models.ForeignKey(Town, related_name='villages', on_delete=models.CASCADE,
                               verbose_name='دهستان')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='تاریخ آخرین ویرایش')

    def __str__(self):
        return self.title

    def get_full(self):
        return self.title + ' < ' + self.father.title + ' < ' + self.father.father.title + ' < ' + self.father.father.father.title


class FileModel(models.Model):
    excel_file = models.FileField()
