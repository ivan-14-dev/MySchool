# backend/apps/academics/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

from .models import Subject, ClassRoom, AcademicYear, ClassGroup, ClassSubject, TimeTable, StudentEnrollment
from .serializers import (
    SubjectSerializer, ClassRoomSerializer, AcademicYearSerializer,
    ClassGroupSerializer, ClassSubjectSerializer, TimeTableSerializer,
    StudentEnrollmentSerializer
)
from apps.core.permissions import SchoolPermission, HasPermission

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [SchoolPermission, HasPermission(['academics.manage_subjects'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'is_active']

class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [SchoolPermission, HasPermission(['academics.manage_classrooms'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [SchoolPermission, HasPermission(['academics.manage_academic_years'])]
    
    @action(detail=True, methods=['post'])
    def set_current(self, request, pk=None):
        academic_year = self.get_object()
        # Désactiver tous les autres années académiques courantes
        AcademicYear.objects.filter(is_current=True).update(is_current=False)
        # Activer cette année académique
        academic_year.is_current = True
        academic_year.save()
        return Response({'status': 'academic year set as current'})

class ClassGroupViewSet(viewsets.ModelViewSet):
    queryset = ClassGroup.objects.all()
    serializer_class = ClassGroupSerializer
    permission_classes = [SchoolPermission, HasPermission(['academics.manage_class_groups'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['academic_year', 'level', 'is_active']

class ClassSubjectViewSet(viewsets.ModelViewSet):
    queryset = ClassSubject.objects.all()
    serializer_class = ClassSubjectSerializer
    permission_classes = [SchoolPermission, HasPermission(['academics.manage_class_subjects'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_group', 'subject']

class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [SchoolPermission, HasPermission(['academics.manage_timetable'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_subject', 'day_of_week', 'is_active']

class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    permission_classes = [SchoolPermission, HasPermission(['academics.manage_enrollments'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_group', 'is_active']
    
    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')
        if student_id:
            enrollments = self.queryset.filter(student_id=student_id, is_active=True)
            serializer = self.get_serializer(enrollments, many=True)
            return Response(serializer.data)
        return Response([], status=status.HTTP_400_BAD_REQUEST)