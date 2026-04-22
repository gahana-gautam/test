from django.db import models
from django.contrib.auth.models import User


class Meeting(models.Model):
    PLATFORM_CHOICES = [
        ('zoom', 'Zoom'), ('teams', 'Microsoft Teams'),
        ('meet', 'Google Meet'), ('slack', 'Slack Huddle'),
        ('in_person', 'In-Person'),
    ]
    RECURRENCE_CHOICES = [
        ('none', 'None'), ('daily', 'Daily'), ('weekly', 'Weekly'),
        ('biweekly', 'Bi-weekly'), ('monthly', 'Monthly'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings')
    title = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='zoom')
    recurrence = models.CharField(max_length=20, choices=RECURRENCE_CHOICES, default='none')
    description = models.TextField(blank=True)
    participants = models.ManyToManyField(User, related_name='meetings', blank=True)
    team_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'start_time']

    def platform_display(self):
        return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)

    def platform_icon(self):
        icons = {
            'zoom': 'fa-video', 'teams': 'fa-video',
            'meet': 'fa-video', 'slack': 'fa-hashtag', 'in_person': 'fa-door-open'
        }
        return icons.get(self.platform, 'fa-calendar')

    def platform_badge_class(self):
        classes = {
            'zoom': 'nx-badge-blue', 'teams': 'nx-badge-teal',
            'meet': 'nx-badge-green', 'slack': 'nx-badge-yellow', 'in_person': 'nx-badge-gray'
        }
        return classes.get(self.platform, 'nx-badge-gray')

    def __str__(self):
        return f"{self.title} on {self.date}"
