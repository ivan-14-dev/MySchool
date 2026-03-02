# backend/apps/extensions/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Extension, APIIntegration, Webhook

class ExtensionSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_extension_type_display', read_only=True)
    
    class Meta:
        model = Extension
        fields = '__all__'
        read_only_fields = ('school', 'status')

class APIIntegrationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    
    class Meta:
        model = APIIntegration
        fields = '__all__'
        read_only_fields = ('school',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Masquer les clés sensibles
        for field in ['api_key', 'secret_key', 'webhook_secret']:
            if field in representation and representation[field]:
                representation[field] = '••••••••' + representation[field][-4:]
        return representation

class WebhookSerializer(serializers.ModelSerializer):
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = Webhook
        fields = '__all__'
        read_only_fields = ('school',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Masquer le secret
        if 'secret' in representation and representation['secret']:
            representation['secret'] = '••••••••' + representation['secret'][-4:]
        return representation