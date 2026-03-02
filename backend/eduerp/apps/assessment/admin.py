# backend/apps/assessment/admin.py
from django.contrib import admin
from .models import AssessmentType, Assessment, GradeScale, Grade, StudentAssessment, Attendance, StudentAttendance, ReportCard

@admin.register(AssessmentType)
class AssessmentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'weight', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_subject', 'assessment_type', 'date', 'maximum_marks', 'is_published')
    list_filter = ('assessment_type', 'is_published', 'date')
    search_fields = ('name', 'class_subject__class_group__name')
    raw_id_fields = ('class_subject',)

@admin.register(GradeScale)
class GradeScaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade_scale', 'name', 'minimum_percentage', 'maximum_percentage', 'points')
    list_filter = ('grade_scale',)
    search_fields = ('name',)

@admin.register(StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'student', 'marks_obtained', 'is_absent')
    list_filter = ('assessment__date', 'is_absent')
    search_fields = ('student__first_name', 'student__last_name', 'assessment__name')
    raw_id_fields = ('assessment', 'student')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('class_subject', 'date', 'period', 'taken_by')
    list_filter = ('date', 'class_subject__class_group__academic_year')
    search_fields = ('class_subject__class_group__name', 'class_subject__subject__name')
    raw_id_fields = ('class_subject', 'taken_by')

@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance', 'student', 'status')
    list_filter = ('status', 'attendance__date')
    search_fields = ('student__first_name', 'student__last_name')
    raw_id_fields = ('attendance', 'student')

@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'term', 'percentage', 'grade', 'is_published')
    list_filter = ('academic_year', 'term', 'is_published')
    search_fields = ('student__first_name', 'student__last_name')
    raw_id_fields = ('student', 'grade')