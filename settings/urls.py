from settings.allviews.city import *
from settings.allviews.part import *
from settings.allviews.town import *
from settings.allviews.village import *
from .views import *

urls = multi_generator_url(model=City(), create=CityCreateView,
                           update=CityUpdateView) + \
       multi_generator_url(model=Part(), create=PartCreateView,
                           update=PartUpdateView) + \
       multi_generator_url(model=Town(), create=TownCreateView,
                           update=TownUpdateView) + \
       multi_generator_url(model=Village(), create=VillageCreateView,
                           update=VillageUpdateView)
urlpatterns = [
                  # path('village/create_default_villages', VillageCreateAllDefaultView.as_view(),
                  #      name='create_default_villages')
              ] + urls
