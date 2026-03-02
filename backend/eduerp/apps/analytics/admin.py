# backend/apps/analytics/admin.py
from django.contrib import admin
from .models import StudentPerformance, ClassStatistics, SchoolReport, DashboardWidget

@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'academic_year', 'average_score', 'trend')
    list_filter = ('academic_year', 'subject', 'trend')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')

@admin.register(ClassStatistics)
class ClassStatisticsAdmin(admin.ModelAdmin):
    list_display = ('class_group', 'academic_year', 'average_performance', 'attendance_rate')
    list_filter = ('academic_year',)
    search_fields = ('class_group__name',)

@admin.register(SchoolReport)
class SchoolReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'period', 'start_date', 'is_published')
    list_filter = ('report_type', 'period', 'is_published')
    search_fields = ('title',)

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'widget_type', 'position', 'is_visible')
    list_filter = ('widget_type', 'is_visible')
    ordering = ('position',)