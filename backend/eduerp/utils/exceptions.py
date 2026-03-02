# backend/utils/exceptions.py
from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Handler d'exception personnalisé pour l'API
    """
    # Appel du handler par défaut
    response = exception_handler(exc, context)
    
    if response is not None:
        # Log de l'erreur
        logger.error(f"API Error: {exc}", exc_info=True)
        
        # Personnalisation de la réponse
        custom_response = {
            'error': {
                'status_code': response.status_code,
                'message': response.data.get('detail', 'An error occurred'),
                'details': response.data
            }
        }
        response.data = custom_response
    
    return response


class EduERPException(Exception):
    """Exception de base pour EduERP"""
    def __init__(self, message, code=status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationError(EduERPException):
    """Exception pour les erreurs de validation"""
    pass


class PermissionDeniedError(EduERPException):
    """Exception pour les permissions refusées"""
    def __init__(self, message="Permission denied", code=status.HTTP_403_FORBIDDEN):
        super().__init__(message, code)


class NotFoundError(EduERPException):
    """Exception pour les ressources non trouvées"""
    def __init__(self, message="Resource not found", code=status.HTTP_404_NOT_FOUND):
        super().__init__(message, code)