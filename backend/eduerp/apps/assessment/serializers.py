# backend/apps/assessment/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import AssessmentType, Assessment, GradeScale, Grade, StudentAssessment, Attendance, StudentAttendance, ReportCard

class AssessmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentType
        fields = '__all__'
        read_only_fields = ('school',)

class AssessmentSerializer(serializers.ModelSerializer):
    class_subject_info = serializers.CharField(source='class_subject.__str__', read_only=True)
    assessment_type_name = serializers.CharField(source='assessment_type.name', read_only=True)
    
    class Meta:
        model = Assessment
        fields = '__all__'
        read_only_fields = ('school',)

class GradeScaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeScale
        fields = '__all__'
        read_only_fields = ('school',)

class GradeSerializer(serializers.ModelSerializer):
    grade_scale_name = serializers.CharField(source='grade_scale.name', read_only=True)
    
    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ('school',)

class StudentAssessmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    assessment_name = serializers.CharField(source='assessment.name', read_only=True)
    percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    
    class Meta:
        model = StudentAssessment
        fields = '__all__'
        read_only_fields = ('school',)

class AttendanceSerializer(serializers.ModelSerializer):
    class_subject_info = serializers.CharField(source='class_subject.__str__', read_only=True)
    taken_by_name = serializers.CharField(source='taken_by.get_full_name', read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'
        read_only_fields = ('school',)

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    attendance_info = serializers.CharField(source='attendance.__str__', read_only=True)
    
    class Meta:
        model = StudentAttendance
        fields = '__all__'
        read_only_fields = ('school',)

class ReportCardSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    class_group_name = serializers.CharField(source='class_group.name', read_only=True)
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    
    class Meta:
        model = ReportCard
        fields = '__all__'
        read_only_fields = ('school',)