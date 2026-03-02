# backend/apps/extensions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExtensionViewSet, APIIntegrationViewSet, WebhookViewSet

router = DefaultRouter()
router.register(r'extensions', ExtensionViewSet)
router.register(r'api-integrations', APIIntegrationViewSet)
router.register(r'webhooks', WebhookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]