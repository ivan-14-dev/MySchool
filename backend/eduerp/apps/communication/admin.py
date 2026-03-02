# backend/apps/communication/admin.py
from django.contrib import admin
from .models import Message, Conversation, Announcement, Notification, Attachment, EmailTemplate

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'message_type', 'created_at')
    search_fields = ('subject', 'content', 'sender__email', 'recipient__email')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_group', 'created_at')
    filter_horizontal = ('participants',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'announcement_type', 'target_audience', 'is_published', 'publish_date')
    list_filter = ('announcement_type', 'target_audience', 'is_published')
    search_fields = ('title', 'content')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('title', 'message', 'user__email')

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'template_type', 'is_active')
    list_filter = ('template_type', 'is_active')