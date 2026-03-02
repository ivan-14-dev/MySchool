# backend/apps/extensions/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import SchoolAwareModel

class Extension(SchoolAwareModel):
    """Extension/module additionnel"""
    EXTENSION_TYPES = (
        ('academic', _('Academic')),
        ('financial', _('Financial')),
        ('communication', _('Communication')),
        ('integration', _('Integration')),
        ('utility', _('Utility')),
    )
    
    STATUS = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('pending', _('Pending')),
        ('error', _('Error')),
    )
    
    name = models.CharField(_("name"), max_length=255)
    version = models.CharField(_("version"), max_length=20)
    extension_type = models.CharField(_("type"), max_length=20, choices=EXTENSION_TYPES)
    description = models.TextField(_("description"), blank=True)
    author = models.CharField(_("author"), max_length=255)
    website = models.URLField(_("website"), blank=True)
    is_enabled = models.BooleanField(_("enabled"), default=False)
    status = models.CharField(_("status"), max_length=20, choices=STATUS, default='inactive')
    settings = models.JSONField(_("settings"), default=dict)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True)
    
    class Meta:
        verbose_name = _("extension")
        verbose_name_plural = _("extensions")
        ordering = ['name']

class APIIntegration(SchoolAwareModel):
    """Intégration API externe"""
    SERVICE_TYPES = (
        ('sms', _('SMS Service')),
        ('email', _('Email Service')),
        ('payment', _('Payment Gateway')),
        ('storage', _('Cloud Storage')),
        ('ai', _('AI Service')),
        ('other', _('Other')),
    )
    
    name = models.CharField(_("name"), max_length=255)
    service_type = models.CharField(_("service type"), max_length=20, choices=SERVICE_TYPES)
    base_url = models.URLField(_("base URL"))
    api_key = models.CharField(_("API key"), max_length=255, blank=True)
    secret_key = models.CharField(_("secret key"), max_length=255, blank=True)
    is_active = models.BooleanField(_("active"), default=False)
    config = models.JSONField(_("configuration"), default=dict)
    webhook_url = models.URLField(_("webhook URL"), blank=True)
    webhook_secret = models.CharField(_("webhook secret"), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _("API integration")
        verbose_name_plural = _("API integrations")
        ordering = ['name']

class Webhook(SchoolAwareModel):
    """Webhook pour intégrations"""
    EVENT_TYPES = (
        ('student.created', _('Student Created')),
        ('student.updated', _('Student Updated')),
        ('invoice.created', _('Invoice Created')),
        ('invoice.paid', _('Invoice Paid')),
        ('attendance.created', _('Attendance Created')),
        ('grade.created', _('Grade Created')),
        ('custom', _('Custom Event')),
    )
    
    name = models.CharField(_("name"), max_length=255)
    event_type = models.CharField(_("event type"), max_length=50, choices=EVENT_TYPES)
    target_url = models.URLField(_("target URL"))
    is_active = models.BooleanField(_("active"), default=True)
    secret = models.CharField(_("secret"), max_length=255, blank=True)
    headers = models.JSONField(_("headers"), default=dict)
    retry_count = models.IntegerField(_("retry count"), default=3)
    timeout = models.IntegerField(_("timeout (seconds)"), default=30)
    
    class Meta:
        verbose_name = _("webhook")
        verbose_name_plural = _("webhooks")
        ordering = ['name']