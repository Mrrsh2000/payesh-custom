"""ماژول آخرین وضیعت

این ماژول جهت اضافه کردن، ویرایش کردن و حذف کردن
آخرین وضیعت ها استفاده میشود.

"""
from abresani.dynamic import *
from settings.models import Town
from settings.views import *


class TownCreateView(SettingCreateView):
    model = Town
    template_name = None


class TownUpdateView(SettingUpdateView):
    model = Town
    template_name = None

    def get_extra_context(self, context):
        context['city'] = self.get_object().father.father
        return super().get_extra_context(context)


class TownDatatableView(DynamicDatatableView):
    model = Town


class TownDeleteView(DynamicDeleteView):
    model = Town

