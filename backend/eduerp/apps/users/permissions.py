# backend/apps/users/permissions.py
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _

class IsAdminOrSelf(permissions.BasePermission):
    """
    Permission pour permettre aux admins ou à l'utilisateur lui-même d'accéder à l'objet
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        return obj == request.user


class IsAdminTeacherOrParent(permissions.BasePermission):
    """
    Permission pour permettre aux admins, enseignants ou parents concernés d'accéder aux données
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'teacher_profile'):
            return True
        
        if hasattr(request.user, 'parent_profile'):
            # Vérifier si le parent a un lien avec l'étudiant
            # Utiliser une importation locale pour éviter les circular imports
            from .models import StudentParent
            if hasattr(obj, 'student'):
                return StudentParent.objects.filter(
                    parent=request.user, 
                    student=obj.student
                ).exists()
        
        return False


class IsSchoolAdmin(permissions.BasePermission):
    """
    Permission pour les administrateurs d'établissement
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.is_staff or request.user.user_type == 'admin'))


class IsTeacher(permissions.BasePermission):
    """
    Permission pour les enseignants
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.user_type == 'teacher')


class IsStudent(permissions.BasePermission):
    """
    Permission pour les étudiants
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.user_type == 'student')


class IsParent(permissions.BasePermission):
    """
    Permission pour les parents
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.user_type == 'parent')