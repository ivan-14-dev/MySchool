# backend/apps/academics/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Subject, ClassRoom, AcademicYear, ClassGroup, ClassSubject, TimeTable, StudentEnrollment

class SubjectSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ('school',)

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'
        read_only_fields = ('school',)

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'
        read_only_fields = ('school',)

class ClassGroupSerializer(serializers.ModelSerializer):
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    class_teacher_name = serializers.CharField(source='class_teacher.get_full_name', read_only=True)
    
    class Meta:
        model = ClassGroup
        fields = '__all__'
        read_only_fields = ('school',)

class ClassSubjectSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.get_full_name', read_only=True)
    room_name = serializers.CharField(source='room.name', read_only=True)
    
    class Meta:
        model = ClassSubject
        fields = '__all__'
        read_only_fields = ('school',)

class TimeTableSerializer(serializers.ModelSerializer):
    class_subject_info = serializers.CharField(source='class_subject.__str__', read_only=True)
    
    class Meta:
        model = TimeTable
        fields = '__all__'
        read_only_fields = ('school',)

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    class_group_name = serializers.CharField(source='class_group.name', read_only=True)
    
    class Meta:
        model = StudentEnrollment
        fields = '__all__'
        read_only_fields = ('school',)