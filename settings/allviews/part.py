"""ماژول آخرین وضیعت

این ماژول جهت اضافه کردن، ویرایش کردن و حذف کردن
آخرین وضیعت ها استفاده میشود.

"""
from payesh.dynamic import *
from settings.models import Part
from settings.views import *


class PartCreateView(SettingCreateView):
    model = Part


class PartUpdateView(SettingUpdateView):
    model = Part


class PartDatatableView(DynamicDatatableView):
    model = Part


class PartDeleteView(DynamicDeleteView):
    model = Part

