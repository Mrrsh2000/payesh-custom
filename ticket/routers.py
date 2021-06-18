from user.student import StudentViewSet
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')
router.register('student', StudentViewSet, basename='student')
urlpatterns = router.urls
