# backend/apps/authentication/admin.py
from django.contrib import admin
from .models import AuthConfig, LoginHistory, SecurityToken

@admin.register(AuthConfig)
class AuthConfigAdmin(admin.ModelAdmin):
    list_display = ('school', 'password_policy', 'max_login_attempts', 'two_factor_auth')
    list_filter = ('password_policy', 'two_factor_auth')

@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'success', 'timestamp')
    list_filter = ('success', 'timestamp')
    search_fields = ('user__email', 'ip_address')
    readonly_fields = ('timestamp',)

@admin.register(SecurityToken)
class SecurityTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_type', 'expires_at', 'used')
    list_filter = ('token_type', 'used', 'expires_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('expires_at',)