from payesh.dynamic import DynamicListView
from payesh.dynamic_api import DynamicModelReadOnlyApi
from logs.models import Log


class LogListView(DynamicListView):
    """
    برای ایجاد یک کاربر جدید در سامانه از این کلاس استفاده میشود

    Arguments:
        form_class(UserCreateForm):
          فرمی که کلاس از آن استفاده میشود
        template_name(str):
           آردس تمپلت مورد استفاده در کلاس
        success_url(str):
           آدرس url که در صورت موفق بودن فرم، کاربر به آن هدایت خواهد شد
    """
    model = Log
    # datatable_cols = ['#', 'نام کاربری', 'نام', 'نام خانوادگی', 'مرحله', 'پوینت', 'شماره تماس', 'وضعیت']


class LogApi(DynamicModelReadOnlyApi):
    model = Log
    queryset = Log.objects.all()
    ordering_field = '-pk'
