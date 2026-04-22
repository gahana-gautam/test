from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')
    head_title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fa-building')
    color = models.CharField(max_length=20, default='#2D6A4F')
    bg_color = models.CharField(max_length=20, default='#D8F3DC')
    created_at = models.DateTimeField(auto_now_add=True)

    def team_count(self):
        return self.teams.count()

    def engineer_count(self):
        return sum(t.members.count() for t in self.teams.all())

    def __str__(self):
        return self.name


class Team(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Restructuring', 'Restructuring'), ('Disbanded', 'Disbanded')]

    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='teams')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_teams')
    manager_email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    email = models.EmailField(blank=True)
    slack_channel = models.CharField(max_length=100, blank=True)
    teams_channel = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, default='#2D6A4F')
    standup_time = models.CharField(max_length=50, blank=True)
    jira_project = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def member_count(self):
        return self.members.count()

    def get_initials(self):
        words = self.name.split()
        return ''.join(w[0].upper() for w in words[:2])

    def manager_initials(self):
        if self.manager:
            f = self.manager.first_name[:1].upper() if self.manager.first_name else ''
            l = self.manager.last_name[:1].upper() if self.manager.last_name else ''
            return f + l or self.manager.username[:2].upper()
        return 'N/A'

    def manager_display(self):
        if self.manager:
            return self.manager.get_full_name() or self.manager.username
        return 'N/A'

    def __str__(self):
        return self.name


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('Team Lead', 'Team Lead'), ('Senior Engineer', 'Senior Engineer'),
        ('Engineer', 'Engineer'), ('Junior Engineer', 'Junior Engineer'),
        ('DevOps', 'DevOps'), ('QA Engineer', 'QA Engineer'),
        ('Data Scientist', 'Data Scientist'), ('Architect', 'Architect'),
    ]
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Engineer')
    joined_at = models.DateTimeField(auto_now_add=True)

    def get_initials(self):
        f = self.user.first_name[:1].upper() if self.user.first_name else ''
        l = self.user.last_name[:1].upper() if self.user.last_name else ''
        return f + l or self.user.username[:2].upper()

    def full_name(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"


class Skill(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.team.name})"


class Repository(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='repositories')
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class TeamDependency(models.Model):
    DEP_TYPE_CHOICES = [
        ('Infrastructure Support', 'Infrastructure Support'),
        ('Bug Resolution', 'Bug Resolution'),
        ('API Integration', 'API Integration'),
        ('Data Feed', 'Data Feed'),
        ('Security Compliance', 'Security Compliance'),
        ('Deployment', 'Deployment'),
        ('General', 'General'),
    ]
    from_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='upstream_deps')
    to_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='downstream_deps')
    dependency_type = models.CharField(max_length=50, choices=DEP_TYPE_CHOICES, default='General')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('from_team', 'to_team')

    def __str__(self):
        return f"{self.from_team.name} → {self.to_team.name}"
