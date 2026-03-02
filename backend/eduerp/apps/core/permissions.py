# backend/apps/core/permissions.py
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _


PERMISSIONS_MAP = {
    'academics': {
        'manage_subjects': 'Can manage subjects',
        'manage_classrooms': 'Can manage classrooms',
        'manage_academic_years': 'Can manage academic years',
        'manage_class_groups': 'Can manage class groups',
        'manage_class_subjects': 'Can manage class subjects',
        'manage_timetable': 'Can manage timetable',
        'manage_enrollments': 'Can manage student enrollments',
    },
    'assessment': {
        'manage_assessment_types': 'Can manage assessment types',
        'manage_assessments': 'Can manage assessments',
        'manage_grade_scales': 'Can manage grade scales',
        'manage_grades': 'Can manage grades',
        'manage_student_assessments': 'Can manage student assessments',
        'manage_attendance': 'Can manage attendance',
        'manage_student_attendance': 'Can manage student attendance',
        'manage_report_cards': 'Can manage report cards',
    },
    'finance': {
        'manage_fees': 'Can manage fees',
        'manage_invoices': 'Can manage invoices',
        'manage_payments': 'Can manage payments',
        'manage_gateways': 'Can manage payment gateways',
    },
    'communication': {
        'manage_messages': 'Can manage messages',
        'manage_conversations': 'Can manage conversations',
        'manage_announcements': 'Can manage announcements',
        'manage_notifications': 'Can manage notifications',
        'manage_attachments': 'Can manage attachments',
        'manage_email_templates': 'Can manage email templates',
    },
    'analytics': {
        'view_performance': 'Can view student performance',
        'view_statistics': 'Can view class statistics',
        'manage_reports': 'Can manage school reports',
        'manage_dashboard': 'Can manage dashboard widgets',
        'view_dashboard': 'Can view dashboard',
    },
    'extensions': {
        'manage_extensions': 'Can manage extensions',
        'manage_api_integrations': 'Can manage API integrations',
        'manage_webhooks': 'Can manage webhooks',
    }
}

class SchoolPermission(permissions.BasePermission):
    """
    Permission personnalisée basée sur le school et les rôles
    """
    def has_permission(self, request, view):
        # Les superutilisateurs ont tous les droits
        if request.user.is_superuser:
            return True
        
        # Vérifier si l'utilisateur a une école
        if not request.user.school:
            return False
        
        # Vérifier les permissions spécifiques
        required_permissions = getattr(view, 'required_permissions', [])
        if required_permissions:
            return request.user.has_perms(required_permissions)
        
        return True

    def has_object_permission(self, request, view, obj):
        # Les superutilisateurs ont tous les droits
        if request.user.is_superuser:
            return True
        
        # Vérifier l'accès à l'objet basé sur l'école
        if hasattr(obj, 'school'):
            return obj.school == request.user.school
        
        if hasattr(obj, 'user'):
            return obj.user.school == request.user.school
        
        return False


class IsSchoolAdmin(permissions.BasePermission):
    """Permission pour les administrateurs d'établissement"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                (request.user.is_staff or request.user.user_type == 'admin'))


class IsTeacher(permissions.BasePermission):
    """Permission pour les enseignants"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.user_type == 'teacher')


class IsStudent(permissions.BasePermission):
    """Permission pour les étudiants"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.user_type == 'student')


class IsParent(permissions.BasePermission):
    """Permission pour les parents"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated and 
                request.user.user_type == 'parent')


class HasPermission(permissions.BasePermission):
    """Permission basée sur des permissions spécifiques"""
    def __init__(self, permissions):
        self.permissions = permissions

    def has_permission(self, request, view):
        return request.user.has_perms(self.permissions)