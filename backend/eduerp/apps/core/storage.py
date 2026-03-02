# backend/apps/core/storage.py
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):
    """
    Storage personnalisé pour overwrite les fichiers existants
    """
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def user_directory_path(instance, filename):
    """
    Fonction pour déterminer le chemin de stockage des fichiers utilisateur
    """
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


def school_directory_path(instance, filename):
    """
    Fonction pour déterminer le chemin de stockage des fichiers d'établissement
    """
    # file will be uploaded to MEDIA_ROOT/school_<id>/<filename>
    return f'school_{instance.school.id}/{filename}'