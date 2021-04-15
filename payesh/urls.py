"""abresani URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework import permissions
from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from abresani import settings
# from user.views import ChangePasswordViewTemplateView
from .views import *
from django.contrib import admin
from django.urls import path, include


schema_view = get_schema_view(
    openapi.Info(
        title="Opp Market API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
handler404 = 'abresani.views.my_custom_page_not_found_view'

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # BASE URLS

    path('login/', UserLoginView.as_view(), name='custom_login'),
    path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/signup/', SignUp.as_view(), name='sign_up_api'),
    path('admin/', admin.site.urls),
    path('404', NotFound404.as_view(), name="404"),

    path('logout/', UserLogout.as_view(), name='user_logout'),
    # API URLS
    path('api/v1/', include('user.routers')),
    path('api/v1/', include('data.routers')),
    path('api/v1/select2/', include('abresani.select2_urls')),
    # Modules URLS
    path('', index, name='index'),
    path('user/', include('user.urls')),
    path('logs/', include('logs.urls')),
    path('settings/', include('settings.urls')),
    path('data/', include('data.urls')),
    path('api/v1/', include('settings.routers')),
    path('api/v1/', include('logs.routers')),
    # API URLS
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
