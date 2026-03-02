# backend/apps/academics/admin.py
from django.contrib import admin
from .models import Subject, ClassRoom, AcademicYear, ClassGroup, ClassSubject, TimeTable, StudentEnrollment

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'credits', 'is_active')
    list_filter = ('department', 'is_active')
    search_fields = ('name', 'code')
    list_editable = ('is_active',)

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'capacity', 'location', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'location')

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    search_fields = ('name',)

@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'academic_year', 'level', 'class_teacher', 'is_active')
    list_filter = ('academic_year', 'level', 'is_active')
    search_fields = ('name', 'code')
    raw_id_fields = ('class_teacher',)

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('class_group', 'subject', 'teacher', 'room')
    list_filter = ('class_group__academic_year', 'class_group__level')
    search_fields = ('class_group__name', 'subject__name')
    raw_id_fields = ('teacher', 'room')

@admin.register(TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('class_subject', 'day_of_week', 'start_time', 'end_time', 'is_active')
    list_filter = ('day_of_week', 'is_active')
    search_fields = ('class_subject__class_group__name', 'class_subject__subject__name')

@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_group', 'enrollment_date', 'roll_number', 'is_active')
    list_filter = ('class_group__academic_year', 'class_group__level', 'is_active')
    search_fields = ('student__first_name', 'student__last_name', 'class_group__name')
    raw_id_fields = ('student', 'class_group')