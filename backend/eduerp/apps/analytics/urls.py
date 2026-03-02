# backend/apps/analytics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentPerformanceViewSet, ClassStatisticsViewSet,
    SchoolReportViewSet, DashboardWidgetViewSet, AnalyticsViewSet
)

router = DefaultRouter()
router.register(r'student-performance', StudentPerformanceViewSet)
router.register(r'class-statistics', ClassStatisticsViewSet)
router.register(r'school-reports', SchoolReportViewSet)
router.register(r'dashboard-widgets', DashboardWidgetViewSet)
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
]