# backend/apps/communication/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import Message, Conversation, Announcement, Notification, Attachment, EmailTemplate
from .serializers import (
    MessageSerializer, ConversationSerializer, AnnouncementSerializer,
    NotificationSerializer, AttachmentSerializer, EmailTemplateSerializer
)
from apps.core.permissions import SchoolPermission, HasPermission

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [SchoolPermission, HasPermission(['communication.manage_messages'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['sender', 'recipient', 'is_read', 'message_type']
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        ).select_related('sender', 'recipient').prefetch_related('attachments')
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        message = self.get_object()
        if message.recipient == request.user:
            message.is_read = True
            message.save()
            return Response({'status': 'message marked as read'})
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [SchoolPermission, HasPermission(['communication.manage_conversations'])]
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).prefetch_related('participants', 'last_message')
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        participant_id = request.data.get('participant_id')
        # Logique d'ajout de participant
        return Response({'status': 'participant added'})

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [SchoolPermission, HasPermission(['communication.manage_announcements'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['announcement_type', 'target_audience', 'is_published']
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        announcement = self.get_object()
        announcement.is_published = True
        announcement.save()
        return Response({'status': 'announcement published'})

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [SchoolPermission, HasPermission(['communication.manage_notifications'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['notification_type', 'is_read']
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all notifications marked as read'})

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [SchoolPermission, HasPermission(['communication.manage_attachments'])]

class EmailTemplateViewSet(viewsets.ModelViewSet):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [SchoolPermission, HasPermission(['communication.manage_email_templates'])]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['template_type', 'is_active']
    
    @action(detail=True, methods=['post'])
    def test(self, request, pk=None):
        template = self.get_object()
        # Logique de test d'email
        return Response({'status': 'test email sent'})