from django.urls import path

from abresani.select2_views import *

urlpatterns = [
    path('city', CitySelect2.as_view(), name='city_select2'),
    path('part', PartSelect2.as_view(), name='part_select2'),
    path('town', TownSelect2.as_view(), name='town_select2'),
    path('village', VillageSelect2.as_view(), name='village_select2'),
    path('season', SeasonSelect2.as_view(), name='season_select2'),
    path('excel', ExcelFilterSelect2.as_view(), name='excel_select2'),
    path('replace_tanker_str', ReplaceTankerStrSelect2.as_view(), name='replace_tanker_str_select2'),
    path('custom_water_need_str', CustomWaterNeedStrSelect2.as_view(), name='custom_water_need_str_select2'),
    path('house_source_need_str', HouseSourceNeedStrSelect2.as_view(), name='house_source_need_str_select2'),
    path('water_network_need_str', WaterNetworkNeedStrSelect2.as_view(), name='water_network_need_str_select2'),
]
