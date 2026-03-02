# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="EduERP API",
      default_version='v1',
      description="API documentation for EduERP School Management System",
      terms_of_service="https://www.eduerp.com/terms/",
      contact=openapi.Contact(email="contact@eduerp.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/academics/', include('apps.academics.urls')),
    path('api/assessment/', include('apps.assessment.urls')),
    path('api/finance/', include('apps.finance.urls')),
    path('api/communication/', include('apps.communication.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/extensions/', include('apps.extensions.urls')),
       # API Documentation
   path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('api/json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)