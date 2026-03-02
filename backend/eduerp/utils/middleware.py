# backend/utils/middleware.py
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware pour logger les requêtes et réponses"""
    
    def process_request(self, request):
        request.start_time = time.time()
        return None

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Method: {request.method}, "
                f"Path: {request.path}, "
                f"Status: {response.status_code}, "
                f"Duration: {duration:.2f}s"
            )
        return response


class JWTAuthMiddleware(MiddlewareMixin):
    """Middleware pour gérer l'authentification JWT"""
    
    def process_request(self, request):
        # Vérification du token JWT dans les cookies
        jwt_token = request.COOKIES.get('access_token')
        if jwt_token and not request.user.is_authenticated:
            try:
                from rest_framework_simplejwt.tokens import AccessToken
                from django.contrib.auth import get_user_model
                
                User = get_user_model()
                access_token = AccessToken(jwt_token)
                user_id = access_token['user_id']
                user = User.objects.get(id=user_id)
                request.user = user
            except Exception as e:
                # Token invalide ou expiré
                pass
        return None