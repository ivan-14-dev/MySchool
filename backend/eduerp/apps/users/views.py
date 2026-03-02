# backend/apps/users/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

from .models import User, StudentProfile, TeacherProfile, ParentProfile, StudentParent
from .serializers import (
    UserSerializer, StudentProfileSerializer, 
    TeacherProfileSerializer, ParentProfileSerializer,
    StudentParentSerializer
)
from .permissions import IsAdminOrSelf, IsAdminTeacherOrParent

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_type', 'is_active', 'school']
    
    def get_permissions(self):
        if self.action in ['create', 'destroy', 'list']:
            permission_classes = [IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsAdminOrSelf]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user activated'})
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminTeacherOrParent]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['class_level', 'section']


class TeacherProfileViewSet(viewsets.ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['department', 'is_class_teacher']


class ParentProfileViewSet(viewsets.ModelViewSet):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer
    permission_classes = [IsAuthenticated]


class StudentParentViewSet(viewsets.ModelViewSet):
    queryset = StudentParent.objects.all()
    serializer_class = StudentParentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'parent', 'is_primary']