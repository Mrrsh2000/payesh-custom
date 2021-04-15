from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register('city', CityViewSet, basename='city')
router.register('town', TownViewSet, basename='town')
router.register('part', PartViewSet, basename='part')
router.register('village', VillageViewSet, basename='village')
urlpatterns = router.urls
