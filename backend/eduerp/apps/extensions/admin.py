# backend/apps/extensions/admin.py
from django.contrib import admin
from .models import Extension, APIIntegration, Webhook

@admin.register(Extension)
class ExtensionAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'extension_type', 'is_enabled', 'status')
    list_filter = ('extension_type', 'is_enabled', 'status')
    filter_horizontal = ('dependencies',)

@admin.register(APIIntegration)
class APIIntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'is_active')
    list_filter = ('service_type', 'is_active')
    readonly_fields = ('api_key', 'secret_key')

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'target_url', 'is_active')
    list_filter = ('event_type', 'is_active')
    readonly_fields = ('secret',)