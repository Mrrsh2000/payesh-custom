"""ماژول آخرین وضیعت

این ماژول جهت اضافه کردن، ویرایش کردن و حذف کردن
آخرین وضیعت ها استفاده میشود.

"""

import re

from django import forms
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.db.models import F
from django.db.models import Q, Model
from django.forms import ModelForm
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import path
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView

from payesh.dynamic_api import CustomValidation
from payesh.logging import log
from payesh.utils import LoginRequiredMixin, CustomPermissionRequiredMixin, custom_change_date

pattern_date = re.compile(r'(\d+/\d+/\d+)')


class DynamicSelect2(LoginRequiredMixin, View):
    """
    کلاس اصلی select2 است

    این کلاس برای صرفه جویی در زمان برای فیلد های select که اطلاعاتشان
    را از پایگاه داده میخانند ایجاد شده است و از Ajax استفاده میکند و همچنین
    قابلیت جستجو به کاربر میدهد
    """
    model = None
    qs = None
    id = 'id'
    text = 'title'
    per_page = 20
    string = False

    def get_model(self):
        return self.model.objects.all() if not self.qs else self.qs

    def get(self, request):
        page = request.GET.get('page', 1)
        search = request.GET.get('search')

        thing = self.get_model()

        if search is not None and len(search.strip()) > 0:
            thing = thing.filter(**{self.text + '__contains': search})
        if self.string:
            thing = thing.values('title')
        else:
            if self.id != 'id':
                thing = thing.annotate(id=F(self.id), text=self.get_text())
            else:
                thing = thing.annotate(text=self.get_text())
            thing = thing.values('id', 'text')

        paginator = Paginator(thing, self.per_page)
        results = paginator.page(int(page)).object_list
        results_bitten = list(results)
        if self.string:
            results_bitten = list(map(lambda x: {'id': x['title'], 'text': x['title']}, results_bitten))
        return JsonResponse({
            'results': results_bitten,
            "pagination": {
                "more": paginator.page(page).has_next()
            }
        }, safe=False)

    def get_text(self):
        return F(self.text)


def multi_generator_url(model, create=None, datatable=None, update=None, delete=None, list=None, add_model_to_url=True):
    # Use:
    #     urlpatterns = [] + multi_generator_url(Model,create=CreateView,update=UpdateView)
    response = []
    model_name = str(model._meta).split('.')[1]
    if create:
        response.append(path(model_name + "/create", create.as_view(), name=model_name + "_create"))
    if update:
        response.append(
            path(model_name + "/update/<int:pk>", update.as_view(), name=model_name + "_update"))
    if delete:
        response.append(
            path(model_name + "/delete/<int:pk>", delete.as_view(), name=model_name + "_delete"))
    if datatable:
        response.append(
            path(model_name + "/datatable", datatable.as_view(), name=model_name + "_datatable"))
    if list:
        response.append(
            path(model_name + "/list", list.as_view(), name=model_name + "_list"))
    return response


def generate_url(model: Model, create=None, datatable=None, update=None, delete=None, view=None, detail=None,
                 add_model_to_url=True):
    # Use:
    #     urlpatterns = [generate_url(Model,create=CreateView), ]
    model_name = str(model._meta).split('.')[1]
    model_url = model_name + '/' if add_model_to_url else ''
    if create:
        return path(model_url + "create", create.as_view(), name=model_name + "_create")
    if view:
        return path(model_url + "list", view.as_view(), name=model_name + "_list")
    if update:
        return path(model_url + "update/<int:pk>", update.as_view(), name=model_name + "_update")
    if delete:
        return path(model_url + "delete/<int:pk>", delete.as_view(), name=model_name + "_delete")
    if datatable:
        return path(model_url + "datatable", datatable.as_view(), name=model_name + "_datatable")
    if detail:
        return path(model_url + "<int:pk>", detail.as_view(), name=model_name + "_detail")
    raise Exception('Generate url Error')


def createURL(model):
    def a(_models):
        class A(DynamicCreateView):
            model = _models

        return A

    return path(str(model._meta).split('.')[1] + '/create', a(model)().as_view(),
                name=str(model._meta).split('.')[1] + "_create")


def dynamic_form(model_class, get_fields=None, form_fields_config=None, just_data=None, exclude_fields=None,
                 extra_widget=None):
    """
        این تابع مدل و فیلد ها رو درصورت کاستومایز دریافت میکند و فرم آن را میسازد
    """

    if get_fields is None:
        get_fields = []
    if extra_widget is None:
        extra_widget = {}
    if exclude_fields is None:
        exclude_fields = []
    labels = []
    required = []
    classes = []
    field_names = []
    types = []
    errors = {}
    if not get_fields:
        for field in model_class._meta.fields:
            if field.attname not in ['id', 'created_at', 'updated_at'] + exclude_fields:
                controller = {'class': 'form-control'}
                if isinstance(field, models.DateField):
                    controller['class'] = 'form-control date'
                    controller['autocomplete'] = 'off'
                elif isinstance(field, models.FloatField):
                    controller['step'] = "0.01"
                elif isinstance(field, models.DateTimeField):
                    controller['class'] = 'form-control date-time'
                    controller['autocomplete'] = 'off'
                elif isinstance(field, models.BigIntegerField):
                    controller['class'] = 'form-control currency'
                    controller['autocomplete'] = 'off'

                get_fields.append(field.attname.replace('_id', ''))
                field_names.append(field.attname.replace('_id', ''))
                if form_fields_config and form_fields_config.get(field.attname.replace('_id', '')):
                    if isinstance(field, models.BigIntegerField):
                        types.append(forms.CharField())
                    else:
                        types.append(
                            form_fields_config.get(field.attname.replace('_id', '')).get(
                                'type')) if form_fields_config.get(
                            field.attname.replace('_id', '')).get('type') else forms.CharField() if isinstance(field,
                                                                                                               models.DateField) or isinstance(
                            field, models.DateTimeField) else types.append(None)
                    current_field = form_fields_config.get(field.attname.replace('_id', ''))
                    labels.append(current_field.get('label') if current_field.get('label') else field.verbose_name)
                    required.append(current_field.get('required') if current_field.get('required') else not field.blank)
                    classes.append(
                        current_field.get('class') if current_field.get('class') else controller)
                    errors[field.attname.replace('_id', '')] = current_field.get('errors') if current_field.get(
                        'errors') else {
                        'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                        'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                        'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                    }
                else:
                    labels.append(field.verbose_name)
                    required.append(not field.blank)
                    types.append(forms.CharField() if isinstance(field, models.DateField) or isinstance(field,
                                                                                                        models.BigIntegerField) or isinstance(
                        field,
                        models.DateTimeField) else None)
                    classes.append(controller)
                    errors[field.attname.replace('_id', '')] = {
                        'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                        'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                        'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                    }
        for field in model_class._meta.many_to_many:
            get_fields.append(field.attname)
            field_names.append(field.attname)
            labels.append(field.verbose_name)
            types.append(None)
            if form_fields_config and form_fields_config.get(field.attname.replace('_id', '')):
                required.append(
                    form_fields_config.get(field.attname.replace('_id', '')).get('required') if form_fields_config.get(
                        field.attname.replace('_id', '')).get('required') else False)
            else:
                required.append(False)
            classes.append({'class': 'form-control'})
            errors[field.attname] = {
                'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
            }
    else:
        for field in model_class._meta.fields:
            if field.attname not in ['id', 'created_at', 'updated_at'] + exclude_fields:
                if field.attname.replace('_id', '') in get_fields:
                    controller = {'class': 'form-control'}
                    if isinstance(field, models.DateField):
                        controller['class'] = 'form-control date'
                        controller['autocomplete'] = 'off'
                    elif isinstance(field, models.FloatField):
                        controller['step'] = "0.01"
                    elif isinstance(field, models.DateTimeField):
                        controller['class'] = 'form-control date-time'
                        controller['autocomplete'] = 'off'
                    elif isinstance(field, models.BigIntegerField):
                        controller['class'] = 'form-control currency'
                        controller['autocomplete'] = 'off'

                    get_fields.append(field.attname.replace('_id', ''))
                    field_names.append(field.attname.replace('_id', ''))
                    if form_fields_config and form_fields_config.get(field.attname.replace('_id', '')):
                        types.append(
                            form_fields_config.get(field.attname.replace('_id', '')).get(
                                'type') if form_fields_config.get(
                                field.attname.replace('_id', '')).get('type') else forms.CharField() if isinstance(
                                field,
                                models.DateField) or isinstance(
                                field,
                                models.BigIntegerField) or isinstance(
                                field, models.DateTimeField) else None)
                        current_field = form_fields_config.get(field.attname.replace('_id', ''))
                        labels.append(current_field.get('label') if current_field.get('label') else field.verbose_name)
                        required.append(
                            current_field.get('required') if current_field.get('required') else not field.blank)
                        classes.append(
                            current_field.get('class') if current_field.get('class') else controller)
                        errors[field.attname.replace('_id', '')] = current_field.get('errors') if current_field.get(
                            'errors') else {
                            'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                            'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                            'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                        }
                    else:
                        types.append(forms.CharField() if isinstance(field, models.DateField) or isinstance(field,
                                                                                                            models.DateTimeField) else None)
                        labels.append(field.verbose_name)
                        required.append(not field.blank)
                        classes.append(controller)
                        errors[field.attname.replace('_id', '')] = {
                            'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                            'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                            'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                        }
        for field in model_class._meta.many_to_many:
            if field.attname in get_fields:
                get_fields.append(field.attname)
                field_names.append(field.attname)
                types.append(None)
                labels.append(field.verbose_name)
                required.append(False)
                classes.append({'class': 'form-control'})
                errors[field.attname] = {
                    'required': "پر کردن فیلد {0} اجباری می باشد!".format(field.verbose_name),
                    'unique': 'این {0} قبلا ثبت شده است!'.format(field.verbose_name),
                    'invalid': '{0} وارد شده صحیح نیست'.format(field.verbose_name)
                }
    if just_data == True:
        return {
            'model': model_class,
            'fields': get_fields,
            'error_messages': errors,
            'labels': labels,
            'required': required,
            'classes': classes,
            'field_names': field_names,
            'type': types,
        }

    class ModelFormCreator(ModelForm):

        class Meta:
            model = model_class
            fields = get_fields
            error_messages = errors
            widgets = extra_widget

        def __init__(self, *args, **kwargs):
            super(ModelFormCreator, self).__init__(*args, **kwargs)

            for key, field in enumerate(field_names):
                if types and types[key]:
                    self.fields[field] = types[key]
                self.fields[field].label = labels[key]
                self.fields[field].required = required[key]
                self.fields[field].widget.attrs = classes[key]
                self.fields[field].widget.attrs['placeholder'] = labels[key] + ' را وارد کنید ...'

    return ModelFormCreator


class DynamicListView(LoginRequiredMixin, CustomPermissionRequiredMixin, TemplateView):
    permission_required = None
    template_name = None
    success_message = None
    model_name = None
    model = None
    title = None
    datatable_cols = None
    searchDB = True
    lenDB = True
    datatableEnable = True
    datatableURL = None
    updateURL = None
    deleteURL = None
    deleteShow = True
    editShow = True

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        else:
            return str(self.model._meta).replace('.', '/') + '_list.html'

    def get_datatable_cols(self):
        return self.datatable_cols if self.datatable_cols else [field.verbose_name for field in
                                                                self.model._meta.fields] + [x.name for x in
                                                                                            self.model._meta.many_to_many]

    def get_success_url(self):
        split = str(self.model._meta).replace('.', '/')
        return '/' + split + '/list'

    def get_deleteURL(self):
        if self.deleteURL:
            return self.deleteURL
        return self.get_success_url().replace('list', 'delete/0')

    def get_updateURL(self):
        if self.updateURL:
            return self.updateURL
        return self.get_success_url().replace('list', 'update/0')

    def get_datatableURL(self):
        return self.datatableURL if self.datatableURL else self.get_success_url().replace('/list', '/datatable')

    def get_success_message(self):
        if self.success_message:
            return self.success_message
        return self.get_model_name() + ' با موفقیت ایجاد شد! '

    def get_model_name(self):
        if self.model_name:
            return self.model_name
        else:
            return self.model._meta.verbose_name

    def get_extra_context(self, context):
        # context['YOUR_DATA'] = ''
        return context

    def get_title(self):
        if self.title:
            return self.title
        elif self.model_name:
            return 'لیست ' + self.model_name
        return 'لیست ' + self.model._meta.verbose_name

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['model_name'] = self.get_model_name()
        if self.datatableEnable:
            context['datatableURL'] = self.get_datatableURL()
            context['cols'] = self.get_datatable_cols()
            context['searchDB'] = self.searchDB
            context['lenDB'] = self.lenDB
            context['deleteShow'] = self.deleteShow
            context['editShow'] = self.editShow
            context['deleteURL'] = self.get_deleteURL()
            context['editURL'] = self.get_updateURL()
        else:
            context['disableTable'] = True

        context = self.get_extra_context(context)
        return context


class DynamicCreateView(LoginRequiredMixin, CustomPermissionRequiredMixin, CreateView):
    permission_required = None
    template_name = None
    success_message = None
    model_name = None
    model = None
    title = None
    form = None
    datatable_cols = None
    searchDB = True
    lenDB = True
    form_fields = None
    form_fields_config = None
    datatableEnable = True
    datatableURL = None
    updateURL = None
    deleteURL = None
    deleteShow = True
    editShow = True
    extra_widget = None

    def __init__(self, custom_model=None):
        super().__init__()
        if custom_model:
            self.model = custom_model

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        else:
            return str(self.model._meta).replace('.', '/') + '_create.html'

    def get_datatable_cols(self):
        return self.datatable_cols if self.datatable_cols else [field.verbose_name for field in
                                                                self.model._meta.fields] + [x.name for x in
                                                                                            self.model._meta.many_to_many]

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        split = str(self.model._meta).replace('.', '/')
        return '/' + split + '/create'

    def get_deleteURL(self):
        if self.deleteURL:
            return self.deleteURL
        return self.get_success_url().replace('create', 'delete/0')

    def get_updateURL(self):
        if self.updateURL:
            return self.updateURL
        return self.get_success_url().replace('create', 'update/0')

    def get_extra_widget(self):
        return self.extra_widget

    def get_datatableURL(self):
        return self.datatableURL if self.datatableURL else self.get_success_url().replace('/create', '/datatable')

    def get_success_message(self):
        if self.success_message:
            return self.success_message
        return self.get_model_name() + ' با موفقیت ایجاد شد! '

    def get_form_fields_config(self):
        return self.form_fields_config

    def get_form_class(self):
        if self.form:
            return self.form
        if self.form_class:
            return self.form_class
        return dynamic_form(self.model, self.form_fields if self.form_fields else [], self.get_form_fields_config(),
                            extra_widget=self.get_extra_widget())

    def get_model_name(self):
        if self.model_name:
            return self.model_name
        else:
            return self.model._meta.verbose_name

    def get_extra_context(self, context):
        # context['YOUR_DATA'] = ''
        return context

    def get_title(self):
        if self.title:
            return self.title
        elif self.model_name:
            return 'افزودن ' + self.model_name
        return 'افزودن ' + self.model._meta.verbose_name

    def get_log(self, form):
        return log(self.request.user, 1, 3, True, form.instance)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['model_name'] = self.get_model_name()
        context['back'] = self.get_success_url()
        if self.datatableEnable:
            context['datatableURL'] = self.get_datatableURL()
            context['cols'] = self.get_datatable_cols()
            context['searchDB'] = self.searchDB
            context['lenDB'] = self.lenDB
            context['deleteShow'] = self.deleteShow
            context['editShow'] = self.editShow
            context['deleteURL'] = self.get_deleteURL()
            context['editURL'] = self.get_updateURL()
        else:
            context['disableTable'] = True

        context = self.get_extra_context(context)
        return context

    def form_valid(self, form):
        """
        پس از بررسی صحیح بودن اطلاعات وارد شده آخرین وضیعت را ایجاد کرده و
        پیغام موفقیت ارسال میکند

        Arguments:
            form:
                فرم دریافتی است
        """
        res = super().form_valid(form)
        self.get_log(form)
        messages.success(self.request, self.get_success_message())
        return res


class DynamicDatatableView(LoginRequiredMixin, CustomPermissionRequiredMixin, BaseDatatableView):
    """
    این کلاس برای نمایش جدول آخرین وضیعت ها ایجاد شده است

    Arguments:
        model:
            مدل کلاس که State است
        columns:
            ستونهای جدول را که آی دی(نمایش دادده نمیشود)، عنوان را مشخص میکند
        order_columns:
            مرتب سازی را تعیین میکند
    """
    model = None
    columns = None
    order_columns = None
    permission_required = None

    def get_columns(self):
        return self.columns if self.columns else [field.attname.replace('_id', '') for field in
                                                  self.model._meta.fields] + [x.name for x in
                                                                              self.model._meta.many_to_many]

    def get_order_columns(self):
        return self.order_columns if self.order_columns else [field.attname.replace('_id', '') for field in
                                                              self.model._meta.fields] + [x.name for x in
                                                                                          self.model._meta.many_to_many] + [
                                                                 '']

    def filter_queryset(self, qs):
        """
        برای جستجو در عنوان آخرین وضیعت هاست

        Arguments:
            qs:
                کوئری مورد جستجو است
        """
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(title__icontains=search))
        return qs

    def render_column(self, row, column):

        colType = type(getattr(row, column)).__name__
        value = getattr(row, column)
        if value is None or colType == 'str' or colType == 'int':
            return super().render_column(row, column)

        if colType == 'datetime':
            return custom_change_date(value, mode=8) if value else ''
        if colType == 'date':
            return custom_change_date(value, mode=2) if value else ''

        if colType == 'bool':
            return 'bool-true' if value else 'bool-false'

        if colType == 'ManyRelatedManager':
            return ' - '.join([str(x) for x in getattr(row, column).all()])

        if colType == 'FieldFile':
            return value.url if value else 'file-null'

        return super().render_column(row, column)


class DynamicUpdateView(LoginRequiredMixin, CustomPermissionRequiredMixin, UpdateView):
    """
    این کلاس برای ویرایش استان ایجاد شده است

    Arguments:
        model:
            مشخص کننده مدل کلاس که LastStatus است
        form_class:
            فرم کلاس که LastStatusFormاست
        template_name:
            آدرس تمپلیت کلاس است
        success_url:
            آدرسی که صفحه پس از موفق بودن به آن منتقل میشود
    """
    permission_required = None
    model = None
    form = None
    template_name = None
    success_url = None
    success_message = None
    form_fields = None
    model_name = None
    form_fields_config = None
    title = None
    extra_widget = None

    def get_extra_widget(self):
        return self.extra_widget

    def get_form_fields_config(self):
        return self.form_fields_config

    def get_form_class(self):
        if self.form:
            return self.form
        if self.form_class:
            return self.form_class
        return dynamic_form(self.model, self.form_fields if self.form_fields else [], self.get_form_fields_config(),
                            extra_widget=self.get_extra_widget())

    def get_template_names(self):
        if self.template_name:
            return self.template_name
        else:
            return str(self.model._meta).replace('.', '/') + '_update.html'

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        split = str(self.model._meta).replace('.', '/')
        return '/' + split + '/create'

    def get_success_message(self):
        if self.success_message:
            return self.success_message
        return self.get_model_name() + ' با موفقیت ویرایش شد! '

    def get_model_name(self):
        if self.model_name:
            return self.model_name
        else:
            return self.model._meta.verbose_name

    def get_extra_context(self, context):
        # context['YOUR_DATA'] = ''
        return context

    def get_title(self):
        if self.title:
            return self.title
        elif self.model_name:
            return 'ویرایش ' + self.model_name
        return "ویرایش " + self.model._meta.verbose_name

    def get_log(self, form):
        return log(self.request.user, 2, 4, True, form.instance)

    def get_context_data(self, *args, **kwargs):
        """
        برای تغییر عنوان یا title صفحه استفاده میشود

        Arguments:
            args:
                پارامتر های وروردی
            kwargs:
                پارامتر های ورودی
        """
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['model_name'] = self.get_model_name()
        context['back'] = self.get_success_url()
        context = self.get_extra_context(context)

        return context

    def form_valid(self, form):
        """
        پس از بررسی صحیح بودن اطلاعات وارد شده آخرین وضیعت را ویرایش کرده و
        پیغام موفقیت ارسال میکند

        Arguments:
            form:
                فرم دریافتی است
        """
        res = super().form_valid(form)
        self.get_log(form)
        messages.success(self.request, self.get_success_message())
        return res


class DynamicDeleteView(LoginRequiredMixin, CustomPermissionRequiredMixin, View):
    """
    این کلاس برای حذف از همه مدل ها استفاده میشود
    """
    model = None
    permission_required = None

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
            log(self.request.user, 3, 5, True, self.model.objects.get(pk=pk))
            self.before_delete()
            self.model.objects.get(pk=pk).delete()
            self.after_delete()
            return HttpResponse(status=200)
        except Exception as e:
            if e.args[1]:
                errorList = []
                for x in e.args[1]:
                    errorList.append(str(x))
                return HttpResponse(' - '.join(errorList), status=500)

    def after_delete(self):
        pass

    def before_delete(self):
        pass


def api_error_creator(model, error_fields: list, extra=None, required_fields=None, blank_fields=None):
    if blank_fields is None:
        blank_fields = []
    if required_fields is None:
        required_fields = []

    response = {}
    model_fields = model._meta.many_to_many + model._meta.fields
    for field in model_fields:
        if field.attname.replace('_id', '') in error_fields:
            response[field.attname.replace('_id', '')] = {"error_messages":
                {
                    "blank": "{0} را وارد کنید!".format(field.verbose_name),
                    "required": "{0} را وارد کنید!".format(field.verbose_name),
                    "invalid": "{0} وارد شده صحیح نمی باشد!".format(field.verbose_name),
                    "invalid_choice": "{0} وارد شده صحیح نمی باشد!".format(field.verbose_name),
                    "invalid_pk_value": "{0} وارد شده صحیح نمی باشد!".format(field.verbose_name),
                    "incorrect_type": "{0} وارد شده صحیح نمی باشد!".format(field.verbose_name),
                    "does_not_exist": "{0} وارد شده صحیح نمی باشد!".format(field.verbose_name),
                    "null": "{0} را وارد کنید!".format(field.verbose_name),
                    "empty": "{0} را وارد کنید!".format(field.verbose_name),
                    "unique": "این {0} قبلا ثبت شده است!".format(field.verbose_name),
                },
            }
            if field.attname.replace('_id', '') in required_fields:
                response[field.attname.replace('_id', '')]['required'] = True
                # response[field.attname.replace('_id', '')]['allow_blank'] = False
            if field.attname.replace('_id', '') in blank_fields:
                response[field.attname.replace('_id', '')]['required'] = False
                # response[field.attname.replace('_id', '')]['allow_blank'] = True
    if extra:
        response.update(extra)
    return response


def check_null_error(initial_data, field, error=''):
    res = initial_data.get(field)
    if res:
        return res
    else:
        raise CustomValidation(field, error)


def check_many2many(initial_data, field, error='', empty=False):
    res = initial_data.get(field)
    if res and type([]) == type(res):
        if len(res):
            return res
        else:
            raise CustomValidation(field, error)
    else:
        if not empty:
            raise CustomValidation(field, error)
        return 0


def set_many2many(initial_data, field, instance, model_many, key=None, many_key='title'):
    if key is None:
        key = field
    res = initial_data.get(field)
    allmany_object = []
    for val in res:
        many_object, was_created = model_many.objects.get_or_create(**{many_key + '': val})
        allmany_object.append(many_object.pk)
    instance.__getattribute__(key).set(allmany_object)
    instance.save()
