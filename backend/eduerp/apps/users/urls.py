# backend/apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, StudentProfileViewSet, 
    TeacherProfileViewSet, ParentProfileViewSet,
    StudentParentViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'student-profiles', StudentProfileViewSet)
router.register(r'teacher-profiles', TeacherProfileViewSet)
router.register(r'parent-profiles', ParentProfileViewSet)
router.register(r'student-parents', StudentParentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]