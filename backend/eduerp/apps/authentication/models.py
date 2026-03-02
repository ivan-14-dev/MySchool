# backend/apps/authentication/models.py
from django.db import models
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from apps.core.models import SchoolAwareModel

class AuthConfig(SchoolAwareModel):
    """Configuration d'authentification par école en cas de plusieurs écoles
    Permet de définir des politiques de mot de passe, des paramètres de session, etc.
    """
    PASSWORD_POLICY = (
        ('low', _('Low - 6 characters')),
        ('medium', _('Medium - 8 characters with numbers')),
        ('high', _('High - 10 characters with numbers and special characters')),
    )
    
    password_policy = models.CharField(_("password policy"), max_length=20, choices=PASSWORD_POLICY, default='medium')
    max_login_attempts = models.IntegerField(_("max login attempts"), default=5)
    lockout_time = models.IntegerField(_("lockout time (minutes)"), default=30)
    session_timeout = models.IntegerField(_("session timeout (minutes)"), default=120)
    two_factor_auth = models.BooleanField(_("two-factor authentication"), default=False)
    social_auth_enabled = models.BooleanField(_("social authentication"), default=False)
    
    class Meta:
        verbose_name = _("authentication configuration")
        verbose_name_plural = _("authentication configurations")

class LoginHistory(SchoolAwareModel):
    """Historique de connexion"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(_("IP address"))
    user_agent = models.TextField(_("user agent"))
    success = models.BooleanField(_("success"))
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("login history")
        verbose_name_plural = _("login history")
        ordering = ['-timestamp']

class SecurityToken(SchoolAwareModel):
    """Token de sécurité pour réinitialisation de mot de passe, etc."""
    TOKEN_TYPES = (
        ('password_reset', _('Password Reset')),
        ('email_verification', _('Email Verification')),
        ('two_factor', _('Two-Factor Authentication')),
    )
    
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='security_tokens')
    token_type = models.CharField(_("token type"), max_length=20, choices=TOKEN_TYPES)
    token = models.CharField(_("token"), max_length=255)
    expires_at = models.DateTimeField(_("expires at"))
    used = models.BooleanField(_("used"), default=False)
    used_at = models.DateTimeField(_("used at"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("security token")
        verbose_name_plural = _("security tokens")
        indexes = [
            models.Index(fields=['token', 'token_type']),
        ]