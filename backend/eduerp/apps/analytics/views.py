# backend/apps/analytics/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg, Count, Sum, Q
from datetime import datetime, timedelta

from .models import StudentPerformance, ClassStatistics, SchoolReport, DashboardWidget
from .serializers import (
    StudentPerformanceSerializer, ClassStatisticsSerializer,
    SchoolReportSerializer, DashboardWidgetSerializer
)
from apps.core.permissions import SchoolPermission, HasPermission
from apps.assessment.models import Assessment, StudentAssessment, Attendance, StudentAttendance
from apps.academics.models import ClassGroup, StudentEnrollment
from apps.users.models import User

class StudentPerformanceViewSet(viewsets.ModelViewSet):
    queryset = StudentPerformance.objects.all()
    serializer_class = StudentPerformanceSerializer
    permission_classes = [SchoolPermission, HasPermission(['analytics.view_performance'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['academic_year', 'class_group', 'subject']

class ClassStatisticsViewSet(viewsets.ModelViewSet):
    queryset = ClassStatistics.objects.all()
    serializer_class = ClassStatisticsSerializer
    permission_classes = [SchoolPermission, HasPermission(['analytics.view_statistics'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['academic_year']

class SchoolReportViewSet(viewsets.ModelViewSet):
    queryset = SchoolReport.objects.all()
    serializer_class = SchoolReportSerializer
    permission_classes = [SchoolPermission, HasPermission(['analytics.manage_reports'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['report_type', 'period', 'is_published']

class DashboardWidgetViewSet(viewsets.ModelViewSet):
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [SchoolPermission, HasPermission(['analytics.manage_dashboard'])]
    
    @action(detail=False, methods=['get'])
    def user_widgets(self, request):
        widgets = self.queryset.filter(is_visible=True).order_by('position')
        serializer = self.get_serializer(widgets, many=True)
        return Response(serializer.data)

class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [SchoolPermission, HasPermission(['analytics.view_dashboard'])]
    
    @action(detail=False, methods=['get'])
    def dashboard_stats(self, request):
        # Statistiques globales
        total_students = User.objects.filter(user_type='student', is_active=True).count()
        total_teachers = User.objects.filter(user_type='teacher', is_active=True).count()
        total_classes = ClassGroup.objects.filter(is_active=True).count()
        
        # Performances récentes
        recent_assessments = Assessment.objects.filter(date__gte=datetime.now() - timedelta(days=30))
        avg_performance = StudentAssessment.objects.filter(
            assessment__in=recent_assessments
        ).aggregate(avg=Avg('marks_obtained'))['avg'] or 0
        
        # Taux de présence
        attendance_rate = Attendance.objects.aggregate(
            rate=Avg(
                Case(
                    When(student_attendances__status='present', then=1),
                    When(student_attendances__status='absent', then=0),
                    default=0,
                    output_field=FloatField()
                )
            )
        )['rate'] or 0
        
        return Response({
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_classes': total_classes,
            'avg_performance': round(avg_performance, 2),
            'attendance_rate': round(attendance_rate * 100, 2)
        })
    
    @action(detail=False, methods=['get'])
    def student_progress(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        student = User.objects.filter(id=student_id, user_type='student').first()
        if not student:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculer la progression de l'étudiant
        performances = StudentPerformance.objects.filter(student=student)
        progress_data = []
        
        for performance in performances:
            progress_data.append({
                'subject': performance.subject.name,
                'average_score': performance.average_score,
                'trend': performance.trend,
                'completed_assessments': performance.completed_assessments,
                'total_assessments': performance.total_assessments
            })
        
        return Response(progress_data)