from django.urls import path

from payesh.select2_views import *

urlpatterns = [
    path('city', CitySelect2.as_view(), name='city_select2'),
    path('part', PartSelect2.as_view(), name='part_select2'),
    path('town', TownSelect2.as_view(), name='town_select2'),
    path('village', VillageSelect2.as_view(), name='village_select2'),
    path('excel', ExcelFilterSelect2.as_view(), name='excel_select2'),
]
