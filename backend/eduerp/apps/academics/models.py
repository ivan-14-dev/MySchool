# backend/apps/academics/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class Subject(models.Model):
    school = models.ForeignKey('core.School', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(_("subject name"), max_length=255)
    code = models.CharField(_("subject code"), max_length=50)
    description = models.TextField(_("description"), blank=True, null=True)
    department = models.ForeignKey('core.Department', on_delete=models.SET_NULL, null=True, 
                                 related_name='subjects')
    is_active = models.BooleanField(_("active"), default=True)
    credits = models.IntegerField(_("credits"), default=0)
    color = models.CharField(_("color"), max_length=7, default='#3b82f6')  # Hex color
    
    class Meta:
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")
        ordering = ['name']
        unique_together = ['school', 'code']

    def __str__(self):
        return f"{self.name} ({self.code})"

class ClassRoom(models.Model):
    school = models.ForeignKey('core.School', on_delete=models.CASCADE, related_name='classrooms')
    name = models.CharField(_("room name"), max_length=100)
    code = models.CharField(_("room code"), max_length=50)
    capacity = models.IntegerField(_("capacity"))
    location = models.CharField(_("location"), max_length=255, blank=True, null=True)
    facilities = models.TextField(_("facilities"), blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    
    class Meta:
        verbose_name = _("classroom")
        verbose_name_plural = _("classrooms")
        ordering = ['name']
        unique_together = ['school', 'code']

    def __str__(self):
        return f"{self.name} ({self.code})"

class AcademicYear(models.Model):
    school = models.ForeignKey('core.School', on_delete=models.CASCADE, related_name='academic_years')
    name = models.CharField(_("academic year"), max_length=9)
    start_date = models.DateField(_("start date"))
    end_date = models.DateField(_("end date"))
    is_current = models.BooleanField(_("current year"), default=False)
    
    class Meta:
        verbose_name = _("academic year")
        verbose_name_plural = _("academic years")
        ordering = ['-start_date']
        unique_together = ['school', 'name']

    def __str__(self):
        return self.name

class ClassGroup(models.Model):
    school = models.ForeignKey('core.School', on_delete=models.CASCADE, related_name='class_groups')
    academic_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, 
                                    related_name='class_groups')
    name = models.CharField(_("class name"), max_length=100)
    code = models.CharField(_("class code"), max_length=50)
    level = models.CharField(_("level"), max_length=50)
    section = models.CharField(_("section"), max_length=50, blank=True, null=True)
    class_teacher = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                                    limit_choices_to={'user_type': 'teacher'},
                                    related_name='class_groups')
    capacity = models.IntegerField(_("capacity"), default=30)
    is_active = models.BooleanField(_("active"), default=True)
    
    class Meta:
        verbose_name = _("class group")
        verbose_name_plural = _("class groups")
        ordering = ['level', 'name']
        unique_together = ['school', 'academic_year', 'code']

    def __str__(self):
        return f"{self.name} - {self.academic_year.name}"

class ClassSubject(models.Model):
    class_group = models.ForeignKey('ClassGroup', on_delete=models.CASCADE, 
                                  related_name='subjects')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, 
                              related_name='class_subjects')
    teacher = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                              limit_choices_to={'user_type': 'teacher'})
    room = models.ForeignKey('ClassRoom', on_delete=models.SET_NULL, null=True, blank=True)
    credits = models.IntegerField(_("credits"), default=0)
    
    class Meta:
        verbose_name = _("class subject")
        verbose_name_plural = _("class subjects")
        unique_together = ['class_group', 'subject']

    def __str__(self):
        return f"{self.class_group.name} - {self.subject.name}"

class TimeTable(models.Model):
    class_subject = models.ForeignKey('ClassSubject', on_delete=models.CASCADE, 
                                    related_name='timetables')
    day_of_week = models.IntegerField(_("day of week"), 
                                    choices=[(0, _('Monday')), (1, _('Tuesday')), 
                                             (2, _('Wednesday')), (3, _('Thursday')), 
                                             (4, _('Friday')), (5, _('Saturday')), 
                                             (6, _('Sunday'))])
    start_time = models.TimeField(_("start time"))
    end_time = models.TimeField(_("end time"))
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    created_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, 
                                 related_name='timetable_created')
    updated_by = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, 
                                 related_name='timetable_updated')
    
    class Meta:
        verbose_name = _("timetable")
        verbose_name_plural = _("timetables")
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.class_subject} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"

class StudentEnrollment(models.Model):
    student = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                              limit_choices_to={'user_type': 'student'},
                              related_name='enrollments')
    class_group = models.ForeignKey('ClassGroup', on_delete=models.CASCADE, 
                                  related_name='enrollments')
    enrollment_date = models.DateField(_("enrollment date"))
    roll_number = models.IntegerField(_("roll number"))
    is_active = models.BooleanField(_("active"), default=True)
    
    class Meta:
        verbose_name = _("student enrollment")
        verbose_name_plural = _("student enrollments")
        unique_together = ['class_group', 'roll_number']
        ordering = ['class_group', 'roll_number']

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_group.name}"