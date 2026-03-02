# backend/apps/communication/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MessageViewSet, ConversationViewSet, AnnouncementViewSet,
    NotificationViewSet, AttachmentViewSet, EmailTemplateViewSet
)

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'announcements', AnnouncementViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'email-templates', EmailTemplateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]