# backend/apps/core/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from .models import School

class MultiSchoolMiddleware(MiddlewareMixin):
    """Middleware pour gérer les multi-écoles"""
    
    def process_request(self, request):
        # Déterminer l'école basée sur le domaine ou le header
        domain = request.get_host().split(':')[0]
        
        try:
            school = School.objects.get(domain=domain, is_active=True)
            request.school = school
        except School.DoesNotExist:
            # Fallback à l'école par défaut ou erreur
            try:
                school = School.objects.get(is_default=True, is_active=True)
                request.school = school
            except School.DoesNotExist:
                raise Http404("Aucun établissement configuré")