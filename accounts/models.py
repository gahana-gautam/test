from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    email_notifications = models.BooleanField(default=True)
    meeting_reminders = models.BooleanField(default=True)
    avatar_initials = models.CharField(max_length=3, blank=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        if not self.avatar_initials:
            first = self.user.first_name[:1].upper() if self.user.first_name else ''
            last = self.user.last_name[:1].upper() if self.user.last_name else ''
            self.avatar_initials = (first + last) or self.user.username[:2].upper()
        super().save(*args, **kwargs)

    def get_initials(self):
        first = self.user.first_name[:1].upper() if self.user.first_name else ''
        last = self.user.last_name[:1].upper() if self.user.last_name else ''
        return (first + last) or self.user.username[:2].upper()

    def __str__(self):
        return f"{self.user.username} profile"
