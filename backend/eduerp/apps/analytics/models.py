# backend/apps/analytics/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import SchoolAwareModel
from apps.users.models import User
from apps.academics.models import ClassGroup, Subject
from apps.assessment.models import Assessment
from apps import academics

class StudentPerformance(SchoolAwareModel):
    """Performance de l'étudiant"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                               limit_choices_to={'user_type': 'student'})
    academic_year = models.CharField(_("academic year"), max_length=9)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_assessments = models.IntegerField(_("total assessments"))
    completed_assessments = models.IntegerField(_("completed assessments"))
    average_score = models.DecimalField(_("average score"), max_digits=5, decimal_places=2)
    max_score = models.DecimalField(_("max score"), max_digits=5, decimal_places=2)
    min_score = models.DecimalField(_("min score"), max_digits=5, decimal_places=2)
    trend = models.CharField(_("trend"), max_length=20, choices=(
        ('improving', _('Improving')),
        ('declining', _('Declining')),
        ('stable', _('Stable')),
    ))
    
    class Meta:
        verbose_name = _("student performance")
        verbose_name_plural = _("student performances")
        unique_together = ['student', 'academic_year', 'subject']

class ClassStatistics(SchoolAwareModel):
    """Statistiques de classe"""
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE)
    academic_year = models.CharField(_("academic year"), max_length=9)
    total_students = models.IntegerField(_("total students"))
    average_performance = models.DecimalField(_("average performance"), max_digits=5, decimal_places=2)
    attendance_rate = models.DecimalField(_("attendance rate"), max_digits=5, decimal_places=2)
    completion_rate = models.DecimalField(_("completion rate"), max_digits=5, decimal_places=2)
    
    class Meta:
        verbose_name = _("class statistics")
        verbose_name_plural = _("class statistics")
        unique_together = ['class_group', 'academic_year']

class SchoolReport(SchoolAwareModel):
    """Rapport d'école"""
    REPORT_TYPES = (
        ('academic', _('Academic Performance')),
        ('financial', _('Financial Report')),
        ('attendance', _('Attendance Report')),
        ('behavior', _('Behavior Report')),
        ('custom', _('Custom Report')),
    )
    
    PERIODS = (
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('yearly', _('Yearly')),
    )
    
    title = models.CharField(_("title"), max_length=255)
    report_type = models.CharField(_("report type"), max_length=20, choices=REPORT_TYPES)
    period = models.CharField(_("period"), max_length=20, choices=PERIODS)
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"))
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField(_("report data"), default=dict)
    is_published = models.BooleanField(_("published"), default=False)
    
    class Meta:
        verbose_name = _("school report")
        verbose_name_plural = _("school reports")
        ordering = ['-start_date']

class DashboardWidget(SchoolAwareModel):
    """Widget de tableau de bord"""
    WIDGET_TYPES = (
        ('chart', _('Chart')),
        ('table', _('Table')),
        ('metric', _('Metric')),
        ('list', _('List')),
    )
    
    name = models.CharField(_("name"), max_length=255)
    widget_type = models.CharField(_("widget type"), max_length=20, choices=WIDGET_TYPES)
    data_source = models.CharField(_("data source"), max_length=255)
    config = models.JSONField(_("configuration"), default=dict)
    position = models.IntegerField(_("position"), default=0)
    is_visible = models.BooleanField(_("visible"), default=True)
    
    class Meta:
        verbose_name = _("dashboard widget")
        verbose_name_plural = _("dashboard widgets")
        ordering = ['position']