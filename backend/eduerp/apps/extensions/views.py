# backend/apps/extensions/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

from .models import Extension, APIIntegration, Webhook
from .serializers import ExtensionSerializer, APIIntegrationSerializer, WebhookSerializer
from apps.core.permissions import SchoolPermission, HasPermission

class ExtensionViewSet(viewsets.ModelViewSet):
    queryset = Extension.objects.all()
    serializer_class = ExtensionSerializer
    permission_classes = [SchoolPermission, HasPermission(['extensions.manage_extensions'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['extension_type', 'is_enabled', 'status']
    
    @action(detail=True, methods=['post'])
    def enable(self, request, pk=None):
        extension = self.get_object()
        extension.is_enabled = True
        extension.status = 'active'
        extension.save()
        return Response({'status': 'extension enabled'})
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk=None):
        extension = self.get_object()
        extension.is_enabled = False
        extension.status = 'inactive'
        extension.save()
        return Response({'status': 'extension disabled'})
    
    @action(detail=True, methods=['post'])
    def install(self, request, pk=None):
        extension = self.get_object()
        # Logique d'installation
        return Response({'status': 'extension installed'})

class APIIntegrationViewSet(viewsets.ModelViewSet):
    queryset = APIIntegration.objects.all()
    serializer_class = APIIntegrationSerializer
    permission_classes = [SchoolPermission, HasPermission(['extensions.manage_api_integrations'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service_type', 'is_active']
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        integration = self.get_object()
        # Logique de test de connexion
        return Response({'status': 'connection test completed'})
    
    @action(detail=True, methods=['post'])
    def sync_data(self, request, pk=None):
        integration = self.get_object()
        # Logique de synchronisation
        return Response({'status': 'data sync completed'})

class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    permission_classes = [SchoolPermission, HasPermission(['extensions.manage_webhooks'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event_type', 'is_active']
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        webhook = self.get_object()
        # Logique de test de webhook
        return Response({'status': 'webhook test completed'})
    
    @action(detail=True, methods=['post'])
    def trigger(self, request, pk=None):
        webhook = self.get_object()
        # Logique de déclenchement manuel
        return Response({'status': 'webhook triggered'})