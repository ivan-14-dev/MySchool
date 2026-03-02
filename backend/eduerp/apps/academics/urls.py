# backend/apps/academics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SubjectViewSet, ClassRoomViewSet, AcademicYearViewSet,
    ClassGroupViewSet, ClassSubjectViewSet, TimeTableViewSet,
    StudentEnrollmentViewSet
)

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'class-groups', ClassGroupViewSet)
router.register(r'class-subjects', ClassSubjectViewSet)
router.register(r'timetables', TimeTableViewSet)
router.register(r'enrollments', StudentEnrollmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]