from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from teams.models import Team, Department, TeamMember
from schedule_app.models import Meeting
from messaging.models import Message
from django.utils import timezone


def landing_view(request):
    return render(request, 'core/landing.html')


@login_required
def dashboard_view(request):
    teams = Team.objects.select_related('department', 'manager').all()
    departments = Department.objects.all()
    total_teams = teams.count()
    total_departments = departments.count()
    total_engineers = TeamMember.objects.count()
    from teams.models import Repository
    total_repos = Repository.objects.count()
    active_teams = teams.filter(status='Active')[:6]
    dept_list = departments[:3]
    from datetime import date as _date
    upcoming = Meeting.objects.filter(date__gte=_date.today()).order_by('date', 'start_time')[:3]
    total_meetings = Meeting.objects.count()
    unread_count = Message.objects.filter(recipient=request.user, is_read=False, status__in=['inbox','sent']).count()
    return render(request, 'core/dashboard.html', {
        'total_teams': total_teams,
        'total_departments': total_departments,
        'total_engineers': total_engineers,
        'total_repos': total_repos,
        'total_meetings': total_meetings,
        'active_teams': active_teams,
        'departments': dept_list,
        'upcoming_meetings': upcoming,
        'unread_count': unread_count,
        'page_title': 'Dashboard',
        'active_nav': 'dashboard',
    })


@login_required
def search_view(request):
    q = request.GET.get('q', '').strip()
    results = {'users': [], 'teams': [], 'departments': [], 'meetings': [], 'messages': []}
    if q:
        results['users'] = list(User.objects.filter(
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(username__icontains=q) | Q(email__icontains=q)
        )[:20])
        results['teams'] = list(Team.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q) | Q(mission__icontains=q)
        ).select_related('department')[:20])
        results['departments'] = list(Department.objects.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )[:20])
        results['meetings'] = list(Meeting.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q),
            creator=request.user,
        )[:20])
        results['messages'] = list(Message.objects.filter(
            Q(subject__icontains=q) | Q(body__icontains=q),
        ).filter(Q(sender=request.user) | Q(recipient=request.user))[:20])
    total = sum(len(v) for v in results.values())
    unread_count = Message.objects.filter(recipient=request.user, is_read=False, status__in=['inbox','sent']).count()
    return render(request, 'core/search.html', {
        'q': q, 'results': results, 'total': total,
        'unread_count': unread_count,
        'page_title': 'Search', 'active_nav': '',
    })
