# backend/apps/assessment/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssessmentTypeViewSet, AssessmentViewSet, GradeScaleViewSet,
    GradeViewSet, StudentAssessmentViewSet, AttendanceViewSet,
    StudentAttendanceViewSet, ReportCardViewSet
)

router = DefaultRouter()
router.register(r'assessment-types', AssessmentTypeViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'grade-scales', GradeScaleViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'student-assessments', StudentAssessmentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'student-attendance', StudentAttendanceViewSet)
router.register(r'report-cards', ReportCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]