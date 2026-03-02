# backend/apps/communication/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Message, Conversation, Announcement, Notification, Attachment, EmailTemplate

class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = ('school', 'uploaded_by', 'file_size', 'mime_type')

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('school', 'sender', 'read_at')

class ConversationSerializer(serializers.ModelSerializer):
    participants_info = serializers.SerializerMethodField()
    last_message_preview = serializers.CharField(source='last_message.content', read_only=True)
    last_message_time = serializers.DateTimeField(source='last_message.created_at', read_only=True)
    
    class Meta:
        model = Conversation
        fields = '__all__'
        read_only_fields = ('school', 'last_message')
    
    def get_participants_info(self, obj):
        return [{
            'id': user.id,
            'name': user.get_full_name(),
            'email': user.email,
            'user_type': user.user_type
        } for user in obj.participants.all()]

class AnnouncementSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ('school', 'author')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ('school', 'read_at')

class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = '__all__'
        read_only_fields = ('school',)