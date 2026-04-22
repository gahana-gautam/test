from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    STATUS_CHOICES = [('inbox', 'Inbox'), ('sent', 'Sent'), ('draft', 'Draft')]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_messages')
    recipient_team_name = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=300)
    body = models.TextField()
    is_group = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def sender_initials(self):
        f = self.sender.first_name[:1].upper() if self.sender.first_name else ''
        l = self.sender.last_name[:1].upper() if self.sender.last_name else ''
        return f + l or self.sender.username[:2].upper()

    def recipient_initials(self):
        if self.recipient:
            f = self.recipient.first_name[:1].upper() if self.recipient.first_name else ''
            l = self.recipient.last_name[:1].upper() if self.recipient.last_name else ''
            return f + l or self.recipient.username[:2].upper()
        return self.recipient_team_name[:2].upper() if self.recipient_team_name else 'GR'

    def __str__(self):
        return f"{self.subject} from {self.sender.username}"


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='message_attachments/%Y/%m/')
    original_name = models.CharField(max_length=255)
    size = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_name
