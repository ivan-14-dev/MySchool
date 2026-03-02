# backend/apps/communication/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import SchoolAwareModel, BaseModel
from apps.users.models import User

class Message(SchoolAwareModel):
    """Message entre utilisateurs"""
    MESSAGE_TYPES = (
        ('text', _('Text')),
        ('image', _('Image')),
        ('file', _('File')),
        ('system', _('System')),
    )
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    subject = models.CharField(_("subject"), max_length=255, blank=True)
    content = models.TextField(_("content"))
    message_type = models.CharField(_("message type"), max_length=20, choices=MESSAGE_TYPES, default='text')
    is_read = models.BooleanField(_("read"), default=False)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    attachments = models.ManyToManyField('Attachment', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

class Conversation(SchoolAwareModel):
    """Conversation entre utilisateurs"""
    participants = models.ManyToManyField(User, related_name='conversations')
    is_group = models.BooleanField(_("group conversation"), default=False)
    name = models.CharField(_("conversation name"), max_length=255, blank=True)
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("conversation")
        verbose_name_plural = _("conversations")
        ordering = ['-created_at']

    def __str__(self):
        if self.is_group:
            return self.name or f"Group conversation {self.id}"
        participants = self.participants.all()
        if participants.count() == 2:
            return f"Conversation between {participants[0]} and {participants[1]}"
        return f"Conversation {self.id}"

class Announcement(SchoolAwareModel):
    """Annonce générale"""
    ANNOUNCEMENT_TYPES = (
        ('info', _('Information')),
        ('warning', _('Warning')),
        ('urgent', _('Urgent')),
        ('event', _('Event')),
    )
    
    TARGET_AUDIENCE = (
        ('all', _('All Users')),
        ('students', _('Students Only')),
        ('teachers', _('Teachers Only')),
        ('parents', _('Parents Only')),
        ('staff', _('Staff Only')),
    )
    
    title = models.CharField(_("title"), max_length=255)
    content = models.TextField(_("content"))
    announcement_type = models.CharField(_("type"), max_length=20, choices=ANNOUNCEMENT_TYPES, default='info')
    target_audience = models.CharField(_("target audience"), max_length=20, choices=TARGET_AUDIENCE, default='all')
    is_published = models.BooleanField(_("published"), default=False)
    publish_date = models.DateTimeField(_("publish date"), null=True, blank=True)
    expiration_date = models.DateTimeField(_("expiration date"), null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("announcement")
        verbose_name_plural = _("announcements")
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

class Notification(SchoolAwareModel):
    """Notification utilisateur"""
    NOTIFICATION_TYPES = (
        ('info', _('Information')),
        ('success', _('Success')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('system', _('System')),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(_("title"), max_length=255)
    message = models.TextField(_("message"))
    notification_type = models.CharField(_("type"), max_length=20, choices=NOTIFICATION_TYPES, default='info')
    is_read = models.BooleanField(_("read"), default=False)
    read_at = models.DateTimeField(_("read at"), null=True, blank=True)
    action_url = models.URLField(_("action URL"), blank=True)
    related_object_type = models.CharField(_("related object type"), max_length=50, blank=True)
    related_object_id = models.PositiveIntegerField(_("related object ID"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user}: {self.title}"

class Attachment(SchoolAwareModel):
    """Fichier attaché"""
    file = models.FileField(_("file"), upload_to='attachments/%Y/%m/%d/')
    original_name = models.CharField(_("original name"), max_length=255)
    file_size = models.PositiveIntegerField(_("file size"))
    mime_type = models.CharField(_("MIME type"), max_length=100)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attachments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("attachment")
        verbose_name_plural = _("attachments")

    def __str__(self):
        return self.original_name

class EmailTemplate(SchoolAwareModel):
    """Template d'email"""
    TEMPLATE_TYPES = (
        ('welcome', _('Welcome Email')),
        ('password_reset', _('Password Reset')),
        ('invoice', _('Invoice Notification')),
        ('attendance', _('Attendance Alert')),
        ('grade', _('Grade Notification')),
        ('custom', _('Custom Template')),
    )
    
    name = models.CharField(_("name"), max_length=255)
    template_type = models.CharField(_("template type"), max_length=50, choices=TEMPLATE_TYPES)
    subject = models.CharField(_("subject"), max_length=255)
    body = models.TextField(_("body"))
    is_active = models.BooleanField(_("active"), default=True)
    variables = models.JSONField(_("variables"), default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("email template")
        verbose_name_plural = _("email templates")
        unique_together = ['school', 'template_type']

    def __str__(self):
        return self.name