# backend/apps/assessment/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from apps.academics.models import ClassSubject, AcademicYear
from apps.users.models import User

class AssessmentType(models.Model):
    name = models.CharField(_("assessment type"), max_length=100)
    code = models.CharField(_("code"), max_length=50)
    description = models.TextField(_("description"), blank=True, null=True)
    weight = models.DecimalField(_("weight"), max_digits=5, decimal_places=2, 
                               help_text="Weight in percentage")
    is_active = models.BooleanField(_("active"), default=True)
    
    class Meta:
        verbose_name = _("assessment type")
        verbose_name_plural = _("assessment types")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.weight}%)"


class Assessment(BaseModel):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, 
                                    related_name='assessments')
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE, 
                                      related_name='assessments')
    name = models.CharField(_("assessment name"), max_length=255)
    description = models.TextField(_("description"), blank=True, null=True)
    maximum_marks = models.DecimalField(_("maximum marks"), max_digits=6, decimal_places=2)
    date = models.DateField(_("date"))
    is_published = models.BooleanField(_("published"), default=False)
    
    class Meta:
        verbose_name = _("assessment")
        verbose_name_plural = _("assessments")
        ordering = ['-date']

    def __str__(self):
        return f"{self.class_subject} - {self.name}"


class GradeScale(models.Model):
    name = models.CharField(_("grade scale"), max_length=100)
    description = models.TextField(_("description"), blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    
    class Meta:
        verbose_name = _("grade scale")
        verbose_name_plural = _("grade scales")
        ordering = ['name']

    def __str__(self):
        return self.name


class Grade(models.Model):
    grade_scale = models.ForeignKey(GradeScale, on_delete=models.CASCADE, 
                                  related_name='grades')
    name = models.CharField(_("grade"), max_length=10)
    minimum_percentage = models.DecimalField(_("minimum percentage"), max_digits=5, decimal_places=2)
    maximum_percentage = models.DecimalField(_("maximum percentage"), max_digits=5, decimal_places=2)
    points = models.DecimalField(_("points"), max_digits=4, decimal_places=2)
    description = models.CharField(_("description"), max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = _("grade")
        verbose_name_plural = _("grades")
        ordering = ['minimum_percentage']

    def __str__(self):
        return f"{self.name} ({self.minimum_percentage}-{self.maximum_percentage}%)"


class StudentAssessment(BaseModel):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, 
                                 related_name='student_assessments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                              limit_choices_to={'user_type': 'student'},
                              related_name='assessments')
    marks_obtained = models.DecimalField(_("marks obtained"), max_digits=6, decimal_places=2)
    comments = models.TextField(_("comments"), blank=True, null=True)
    is_absent = models.BooleanField(_("absent"), default=False)
    
    class Meta:
        verbose_name = _("student assessment")
        verbose_name_plural = _("student assessments")
        unique_together = ['assessment', 'student']
        ordering = ['assessment', 'student']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assessment.name}"

    @property
    def percentage(self):
        if self.assessment.maximum_marks > 0:
            return (self.marks_obtained / self.assessment.maximum_marks) * 100
        return 0


class Attendance(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE, 
                                    related_name='attendances')
    date = models.DateField(_("date"))
    period = models.CharField(_("period"), max_length=50, blank=True, null=True)
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               limit_choices_to={'user_type': 'teacher'})
    
    class Meta:
        verbose_name = _("attendance")
        verbose_name_plural = _("attendances")
        unique_together = ['class_subject', 'date', 'period']
        ordering = ['-date']

    def __str__(self):
        return f"{self.class_subject} - {self.date}"


class StudentAttendance(models.Model):
    ATTENDANCE_CHOICES = (
        ('present', _('Present')),
        ('absent', _('Absent')),
        ('late', _('Late')),
        ('excused', _('Excused')),
    )
    
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, 
                                 related_name='student_attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                              limit_choices_to={'user_type': 'student'})
    status = models.CharField(_("status"), max_length=10, choices=ATTENDANCE_CHOICES)
    remarks = models.CharField(_("remarks"), max_length=255, blank=True, null=True)
    
    class Meta:
        verbose_name = _("student attendance")
        verbose_name_plural = _("student attendances")
        unique_together = ['attendance', 'student']
        ordering = ['attendance', 'student']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.attendance.date} - {self.status}"


class ReportCard(BaseModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, 
                              limit_choices_to={'user_type': 'student'},
                              related_name='report_cards')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, 
                                    related_name='report_cards')
    class_group = models.ForeignKey('academics.ClassGroup', on_delete=models.CASCADE, 
                                  related_name='report_cards')
    term = models.CharField(_("term"), max_length=50)
    total_marks = models.DecimalField(_("total marks"), max_digits=8, decimal_places=2)
    marks_obtained = models.DecimalField(_("marks obtained"), max_digits=8, decimal_places=2)
    percentage = models.DecimalField(_("percentage"), max_digits=5, decimal_places=2)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    rank = models.IntegerField(_("rank"), null=True, blank=True)
    remarks = models.TextField(_("remarks"), blank=True, null=True)
    is_published = models.BooleanField(_("published"), default=False)
    
    class Meta:
        verbose_name = _("report card")
        verbose_name_plural = _("report cards")
        unique_together = ['student', 'academic_year', 'term']
        ordering = ['-academic_year', 'term', 'student']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.academic_year} - {self.term}"