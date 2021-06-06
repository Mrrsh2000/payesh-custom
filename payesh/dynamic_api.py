import json

from django.contrib.auth.models import Permission
from django.db.models import Q
from django.http import Http404
from django.utils.encoding import force_text
from django_datatables_view.base_datatable_view import BaseDatatableView
from django_datatables_view.mixins import LazyEncoder
from rest_framework import serializers, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from payesh.logging import log
from payesh.utils import custom_change_date


def replace_star(key, dictionary):
    if isinstance(dictionary, dict):
        for k, v in dictionary.items():
            if k == key:
                dictionary[key] = '*'
            elif isinstance(v, dict):
                v = replace_star(key, v)
            elif isinstance(v, list):
                for d in v:
                    if isinstance(d, dict):
                        d = replace_star(key, d)
    return dictionary


class DynamicModelApi(viewsets.ModelViewSet, BaseDatatableView):
    permission_classes = [permissions.IsAuthenticated]
    custom_perms = {}
    model = None
    columns = None
    order_columns = None
    permission_required = None
    disables_views = []
    ordering_field = None

    def ordering(self, qs):
        if self.ordering_field:
            qs.order_by(self.ordering_field)
        return super().ordering(qs)

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
        if '.' not in column:
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

    # @action(methods=['post'], detail=False, url_path='datatable/(?P<phone_pk>[^/.]+)')
    @action(methods=['post'], detail=False)
    def datatable(self, request, *args, **kwargs):
        if 'datatable' in self.disables_views:
            return Http404()
        response = None
        func_val = self.get_context_data(**kwargs)
        if not self.is_clean:
            assert isinstance(func_val, dict)
            response = dict(func_val)
            if 'error' not in response and 'sError' not in response:
                response['result'] = 'ok'
            else:
                response['result'] = 'error'
        else:
            response = func_val

        dump = json.dumps(response, cls=LazyEncoder)
        return self.render_to_response(dump)

    def check_permissions(self, request):
        if not self.request.user.is_authenticated:
            self.permission_denied(
                request, message=getattr('Login Required', 'message', None)
            )
        if self.custom_perms:
            if self.custom_perms.get(self.action):
                if self.request.user.role not in self.custom_perms.get(self.action):
                    self.permission_denied(request, message='شما دسترسی ندارید!')

    def create(self, request, *args, **kwargs):
        if 'create' in self.disables_views:
            return Http404()

        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        if 'retrieve' in self.disables_views:
            return Http404()
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if 'destroy' in self.disables_views or 'delete' in self.disables_views:
            return Http404()
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            user = request.user
            log(user, 1, 5, True, self.model, self.kwargs['pk'])
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            if e.args[1]:
                errorList = []
                for x in e.args[1]:
                    errorList.append(x._meta.verbose_name + '(' + str(x) + ')')
                return Response(' - '.join(errorList), status=500)

    def update(self, request, *args, **kwargs):
        if 'update' in self.disables_views:
            return Http404()
        return super().update(request, *args, **kwargs)


class DynamicModelReadOnlyApi(viewsets.ReadOnlyModelViewSet, BaseDatatableView):
    permission_classes = [permissions.IsAuthenticated]
    custom_perms = {}
    model = None
    columns = None
    order_columns = None
    permission_required = None
    disables_views = []
    ordering_field = None

    def ordering(self, qs):
        """ Get parameters from the request and prepare order by clause
                """

        # Number of columns that are used in sorting
        sorting_cols = 0
        if self.pre_camel_case_notation:
            try:
                sorting_cols = int(self._querydict.get('iSortingCols', 0))
            except ValueError:
                sorting_cols = 0
        else:
            sort_key = 'order[{0}][column]'.format(sorting_cols)
            while sort_key in self._querydict:
                sorting_cols += 1
                sort_key = 'order[{0}][column]'.format(sorting_cols)

        order = []
        order_columns = self.get_order_columns()

        for i in range(sorting_cols):
            # sorting column
            sort_dir = 'asc'
            try:
                if self.pre_camel_case_notation:
                    sort_col = int(self._querydict.get('iSortCol_{0}'.format(i)))
                    # sorting order
                    sort_dir = self._querydict.get('sSortDir_{0}'.format(i))
                else:
                    sort_col = int(self._querydict.get('order[{0}][column]'.format(i)))
                    # sorting order
                    sort_dir = self._querydict.get('order[{0}][dir]'.format(i))
            except ValueError:
                sort_col = 0

            sdir = '-' if sort_dir == 'desc' else ''
            sortcol = order_columns[sort_col]

            if isinstance(sortcol, list):
                for sc in sortcol:
                    order.append('{0}{1}'.format(sdir, sc.replace('.', '__')))
            else:
                order.append('{0}{1}'.format(sdir, sortcol.replace('.', '__')))

        if order:
            return qs.order_by(*order)
        elif self.ordering_field:
            return qs.order_by(self.ordering_field)
        return qs

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

    # @action(methods=['post'], detail=False, url_path='datatable/(?P<phone_pk>[^/.]+)')
    @action(methods=['post'], detail=False)
    def datatable(self, request, *args, **kwargs):
        if 'datatable' in self.disables_views:
            return Http404()
        response = None
        func_val = self.get_context_data(**kwargs)
        if not self.is_clean:
            assert isinstance(func_val, dict)
            response = dict(func_val)
            if 'error' not in response and 'sError' not in response:
                response['result'] = 'ok'
            else:
                response['result'] = 'error'
        else:
            response = func_val

        dump = json.dumps(response, cls=LazyEncoder)
        return self.render_to_response(dump)

    def check_permissions(self, request):
        super().check_permissions(request)
        if not self.request.user.is_authenticated:
            self.permission_denied(
                request, message=getattr('Login Required', 'message', None)
            )
        if self.custom_perms:
            if self.custom_perms.get(self.action):
                permissonObject = Permission.objects.filter(codename=self.custom_perms.get(self.action)).last()
                perm = str(self.model._meta).split('.')[0] + '.' + permissonObject.codename
                if not self.request.user.has_perm(perm):
                    self.permission_denied(request, message='شما دسترسی {0} را ندارید!'.format(permissonObject.name))

    def retrieve(self, request, *args, **kwargs):
        if 'retrieve' in self.disables_views:
            return Http404()
        return super().retrieve(request, *args, **kwargs)


class DynamicSerializer(serializers.ModelSerializer):
    remove_field_view = {}
    depth_zero = []
    default_depth_zero = True

    def get_fields(self):
        res = super().get_fields()
        if self.remove_field_view.get(self.context['view'].action):
            for field in self.remove_field_view.get(self.context['view'].action):
                if res.get(field):
                    del res[field]
                else:
                    print('ERROR in Get Field of {0}: No {1} Field in Model !!!'.format(self.context['view'].action,
                                                                                        field))
        return res

    def build_field(self, field_name, info, model_class, nested_depth):
        if self.default_depth_zero:
            if self.context['view'].action in ['create', 'update']:
                nested_depth = 0

        if self.context['view'].action in self.depth_zero:
            nested_depth = 0

        return super().build_field(field_name, info, model_class, nested_depth)


class CustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'مشکلی پیش آمده است.'

    def __init__(self, field, detail, status_code=None):
        if status_code is None:
            status_code = self.status_code
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: [force_text(detail)]}
        else:
            self.detail = {'detail': [force_text(self.default_detail)]}


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
                    "unique": "این {0} قبلا ثبت شده است!".format(field.verbose_name)
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


class MessageApiResponseMixin:
    success_message = 'You have successfully register'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # log(self.request.user, 1, 3, True,serializer)
        return Response({'messages': self.success_message}, status=status.HTTP_200_OK, headers={})

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'messages': self.success_message}, status=status.HTTP_200_OK, headers={})
