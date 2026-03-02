# backend/apps/core/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Utiliser get_user_model() pour éviter les imports circulaires
User = get_user_model()

class School(models.Model):
    name = models.CharField(_("school name"), max_length=255)
    code = models.CharField(_("school code"), max_length=50, unique=True)
    address = models.TextField(_("address"))
    city = models.CharField(_("city"), max_length=100)
    country = models.CharField(_("country"), max_length=100, default="France")
    postal_code = models.CharField(_("postal code"), max_length=20)
    phone = models.CharField(_("phone"), max_length=20)
    email = models.EmailField(_("email"))
    website = models.URLField(_("website"), blank=True, null=True)
    logo = models.ImageField(_("logo"), upload_to='schools/logos/', blank=True, null=True)
    academic_year = models.CharField(_("academic year"), max_length=9, help_text="Format: YYYY-YYYY")
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("school")
        verbose_name_plural = _("schools")
        ordering = ['name']

    def __str__(self):
        return self.name

class Department(models.Model):
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(_("department name"), max_length=255)
    code = models.CharField(_("department code"), max_length=50)
    description = models.TextField(_("description"), blank=True, null=True)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                           related_name='headed_departments')
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("department")
        verbose_name_plural = _("departments")
        ordering = ['name']
        unique_together = ['school', 'code']

    def __str__(self):
        return f"{self.name} - {self.school.name}"

class BaseModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='%(class)s_created')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                                 related_name='%(class)s_updated')

    class Meta:
        abstract = True

class SchoolAwareModel(models.Model):
    """Modèle de base pour tous les modèles liés à une école"""
    school = models.ForeignKey('core.School', on_delete=models.CASCADE, related_name='%(class)s')
    
    class Meta:
        abstract = True