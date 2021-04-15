from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('logs', LogApi, basename='log')
urlpatterns = router.urls