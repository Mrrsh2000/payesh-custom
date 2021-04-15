"""ماژول آخرین وضیعت

این ماژول جهت اضافه کردن، ویرایش کردن و حذف کردن
آخرین وضیعت ها استفاده میشود.

"""
from abresani.dynamic import *
from settings.models import City
from settings.views import *


class CityCreateView(SettingCreateView):
    model = City


class CityUpdateView(SettingUpdateView):
    model = City


class CityDatatableView(DynamicDatatableView):
    model = City


class CityDeleteView(DynamicDeleteView):
    model = City

