# backend/apps/assessment/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Count, Sum

from .models import AssessmentType, Assessment, GradeScale, Grade, StudentAssessment, Attendance, StudentAttendance, ReportCard
from .serializers import (
    AssessmentTypeSerializer, AssessmentSerializer, GradeScaleSerializer,
    GradeSerializer, StudentAssessmentSerializer, AttendanceSerializer,
    StudentAttendanceSerializer, ReportCardSerializer
)
from apps.core.permissions import SchoolPermission, HasPermission

class AssessmentTypeViewSet(viewsets.ModelViewSet):
    queryset = AssessmentType.objects.all()
    serializer_class = AssessmentTypeSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_assessment_types'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_assessments'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_subject', 'assessment_type', 'is_published']

class GradeScaleViewSet(viewsets.ModelViewSet):
    queryset = GradeScale.objects.all()
    serializer_class = GradeScaleSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_grade_scales'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active']

class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_grades'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['grade_scale']

class StudentAssessmentViewSet(viewsets.ModelViewSet):
    queryset = StudentAssessment.objects.all()
    serializer_class = StudentAssessmentSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_student_assessments'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assessment', 'student', 'is_absent']

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_attendance'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_subject', 'date']

class StudentAttendanceViewSet(viewsets.ModelViewSet):
    queryset = StudentAttendance.objects.all()
    serializer_class = StudentAttendanceSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_student_attendance'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['attendance', 'student', 'status']

class ReportCardViewSet(viewsets.ModelViewSet):
    queryset = ReportCard.objects.all()
    serializer_class = ReportCardSerializer
    permission_classes = [SchoolPermission, HasPermission(['assessment.manage_report_cards'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'academic_year', 'term', 'is_published']
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        report_card = self.get_object()
        report_card.is_published = True
        report_card.save()
        return Response({'status': 'report card published'})
    
    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        report_card = self.get_object()
        # Logique de génération PDF
        return Response({'status': 'PDF generated'})