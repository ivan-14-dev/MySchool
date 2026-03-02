# backend/apps/analytics/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import StudentPerformance, ClassStatistics, SchoolReport, DashboardWidget

class StudentPerformanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    class_group_name = serializers.CharField(source='class_group.name', read_only=True)
    
    class Meta:
        model = StudentPerformance
        fields = '__all__'
        read_only_fields = ('school',)

class ClassStatisticsSerializer(serializers.ModelSerializer):
    class_group_name = serializers.CharField(source='class_group.name', read_only=True)
    
    class Meta:
        model = ClassStatistics
        fields = '__all__'
        read_only_fields = ('school',)

class SchoolReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)
    
    class Meta:
        model = SchoolReport
        fields = '__all__'
        read_only_fields = ('school',)

class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = '__all__'
        read_only_fields = ('school',)