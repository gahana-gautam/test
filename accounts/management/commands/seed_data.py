from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from teams.models import Department, Team, TeamMember, Skill, Repository, TeamDependency
from accounts.models import UserProfile
from messaging.models import Message
from schedule_app.models import Meeting
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Seed Nexora database with sample data from the Agile Project Module'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Nexora database...')

        # Create admin user
        admin, _ = User.objects.get_or_create(username='admin', defaults={
            'email': 'admin@nexora.com', 'first_name': 'System', 'last_name': 'Admin',
            'is_staff': True, 'is_superuser': True,
        })
        admin.set_password('admin123')
        admin.save()
        UserProfile.objects.get_or_create(user=admin)

        # Create departments from Agile Project Module
        dept_data = [
            {'name': 'xTV & Web', 'icon': 'fa-tv', 'color': '#2D6A4F', 'bg': '#D8F3DC', 'description': 'Responsible for xTV web platform delivery and all web-based broadcast services.'},
            {'name': 'Native TVs', 'icon': 'fa-desktop', 'color': '#3B82F6', 'bg': '#DBEAFE', 'description': 'Develops and maintains native TV applications across all major platforms.'},
            {'name': 'Mobile', 'icon': 'fa-mobile-alt', 'color': '#8B5CF6', 'bg': '#F3E8FF', 'description': 'Owns iOS and Android mobile app development and delivery.'},
            {'name': 'Reliability & Tools', 'icon': 'fa-wrench', 'color': '#F59E0B', 'bg': '#FEF3C7', 'description': 'Ensures platform reliability, tooling, and developer experience across all teams.'},
            {'name': 'Architecture & Programme', 'icon': 'fa-sitemap', 'color': '#EF4444', 'bg': '#FEE2E2', 'description': 'Provides technical architecture direction and programme management across the engineering division.'},
        ]

        depts = {}
        for dd in dept_data:
            dept, _ = Department.objects.get_or_create(name=dd['name'], defaults={
                'icon': dd['icon'], 'color': dd['color'], 'bg_color': dd['bg'],
                'description': dd['description'],
            })
            depts[dd['name']] = dept

        # Create department heads
        dept_heads = [
            ('sebastian.holt', 'Sebastian', 'Holt', 'sebastian.holt@broadcast.com', 'xTV & Web'),
            ('mason.briggs', 'Mason', 'Briggs', 'mason.briggs@broadcast.com', 'Native TVs'),
            ('violet.ramsey', 'Violet', 'Ramsey', 'violet.ramsey@broadcast.com', 'Mobile'),
            ('lucy.vaughn', 'Lucy', 'Vaughn', 'lucy.vaughn@broadcast.com', 'Reliability & Tools'),
            ('theodore.knox', 'Theodore', 'Knox', 'theodore.knox@broadcast.com', 'Architecture & Programme'),
        ]

        for uname, first, last, email, dept_name in dept_heads:
            u, _ = User.objects.get_or_create(username=uname, defaults={
                'email': email, 'first_name': first, 'last_name': last,
            })
            u.set_password('nexora123')
            u.save()
            UserProfile.objects.get_or_create(user=u)
            if dept_name in depts:
                depts[dept_name].head = u
                depts[dept_name].save()

        # Teams data from Agile Project Module
        teams_data = [
            # xTV & Web
            {'name': 'Code Warriors', 'dept': 'xTV & Web', 'color': '#2D6A4F',
             'mission': 'Infrastructure scalability and performance optimisation for xTV web platform.',
             'skills': ['AWS', 'Terraform', 'Kubernetes', 'Python', 'Go', 'CI/CD'],
             'repos': ['xtvweb-infra', 'scalability-toolkit', 'perf-monitor'],
             'email': 'code-warriors@broadcast.com', 'slack': '#code-warriors',
             'jira': 'CW', 'standup': '09:00 daily'},
            {'name': 'The Debuggers', 'dept': 'xTV & Web', 'color': '#40916C',
             'mission': 'Advanced debugging, root cause analysis, and technical debt resolution.',
             'skills': ['Python', 'JavaScript', 'Debugging', 'Performance Profiling', 'Selenium'],
             'repos': ['debug-toolkit', 'rca-framework', 'tech-debt-tracker'],
             'email': 'debuggers@broadcast.com', 'slack': '#debuggers',
             'jira': 'DBG', 'standup': '09:30 daily'},
            {'name': 'Bit Masters', 'dept': 'xTV & Web', 'color': '#52B788',
             'mission': 'Security compliance, encryption standards and vulnerability management.',
             'skills': ['OWASP', 'Encryption', 'AWS Security', 'Penetration Testing', 'GDPR'],
             'repos': ['security-scanner', 'encryption-lib', 'compliance-docs'],
             'email': 'bit-masters@broadcast.com', 'slack': '#bit-masters',
             'jira': 'BM', 'standup': '10:00 daily'},
            {'name': 'Agile Avengers', 'dept': 'xTV & Web', 'color': '#1B4332',
             'mission': 'Agile transformation, workflow optimisation and delivery excellence.',
             'skills': ['Scrum', 'Kanban', 'Jira', 'Confluence', 'Coaching'],
             'repos': ['agile-metrics', 'delivery-tracker'],
             'email': 'agile-avengers@broadcast.com', 'slack': '#agile-avengers',
             'jira': 'AA', 'standup': '09:15 daily'},
            {'name': 'Full Stack Ninjas', 'dept': 'xTV & Web', 'color': '#0D2818',
             'mission': 'Frontend and backend synchronisation for seamless xTV web experiences.',
             'skills': ['React', 'Node.js', 'TypeScript', 'GraphQL', 'PostgreSQL', 'Docker'],
             'repos': ['xtv-frontend', 'xtv-api', 'shared-components'],
             'email': 'fullstack-ninjas@broadcast.com', 'slack': '#fullstack-ninjas',
             'jira': 'FSN', 'standup': '09:00 daily'},
            {'name': 'Data Wranglers', 'dept': 'xTV & Web', 'color': '#2D6A4F',
             'mission': 'Big data engineering, streaming pipelines and analytics infrastructure.',
             'skills': ['Apache Kafka', 'Spark', 'Python', 'Airflow', 'dbt', 'Snowflake'],
             'repos': ['data-pipelines', 'streaming-infra', 'analytics-models'],
             'email': 'data-wranglers@broadcast.com', 'slack': '#data-wranglers',
             'jira': 'DW', 'standup': '09:30 daily'},
            # Native TVs
            {'name': 'TV Pioneers', 'dept': 'Native TVs', 'color': '#3B82F6',
             'mission': 'Next generation native TV app development for major broadcast platforms.',
             'skills': ['Swift', 'tvOS', 'Kotlin', 'Android TV', 'Fire TV', 'CI/CD'],
             'repos': ['tvos-app', 'android-tv-app', 'firetv-app'],
             'email': 'tv-pioneers@broadcast.com', 'slack': '#tv-pioneers',
             'jira': 'TVP', 'standup': '09:00 daily'},
            {'name': 'Screen Wizards', 'dept': 'Native TVs', 'color': '#1D4ED8',
             'mission': 'UI rendering optimisation and adaptive streaming for large-screen experiences.',
             'skills': ['SwiftUI', 'Compose', 'HLS', 'Video Encoding', 'CDN', 'WebRTC'],
             'repos': ['screen-renderer', 'adaptive-player', 'cdn-config'],
             'email': 'screen-wizards@broadcast.com', 'slack': '#screen-wizards',
             'jira': 'SW', 'standup': '09:15 daily'},
            {'name': 'Platform Guardians', 'dept': 'Native TVs', 'color': '#2563EB',
             'mission': 'Platform stability, testing and quality assurance for all native TV apps.',
             'skills': ['XCTest', 'Espresso', 'Appium', 'Jenkins', 'Fastlane', 'JIRA'],
             'repos': ['tv-test-suite', 'qa-automation', 'test-reports'],
             'email': 'platform-guardians@broadcast.com', 'slack': '#platform-guardians',
             'jira': 'PG', 'standup': '09:30 daily'},
            {'name': 'Stream Team', 'dept': 'Native TVs', 'color': '#1E40AF',
             'mission': 'Live streaming infrastructure and low-latency delivery for broadcast content.',
             'skills': ['FFmpeg', 'HLS', 'DASH', 'AWS MediaLive', 'WebSocket', 'Redis'],
             'repos': ['live-stream-infra', 'media-encoder', 'latency-monitor'],
             'email': 'stream-team@broadcast.com', 'slack': '#stream-team',
             'jira': 'ST', 'standup': '09:00 daily'},
            # Mobile
            {'name': 'App Architects', 'dept': 'Mobile', 'color': '#8B5CF6',
             'mission': 'Core mobile architecture, design system and shared mobile components.',
             'skills': ['Swift', 'Kotlin', 'React Native', 'Design Systems', 'SwiftUI', 'Compose'],
             'repos': ['mobile-design-system', 'shared-mobile-lib', 'app-core'],
             'email': 'app-architects@broadcast.com', 'slack': '#app-architects',
             'jira': 'AA2', 'standup': '09:00 daily'},
            {'name': 'Mobile Mavericks', 'dept': 'Mobile', 'color': '#7C3AED',
             'mission': 'Feature delivery and innovation for iOS and Android broadcast mobile apps.',
             'skills': ['Swift', 'Kotlin', 'Firebase', 'Push Notifications', 'Analytics', 'A/B Testing'],
             'repos': ['ios-broadcast-app', 'android-broadcast-app', 'feature-flags'],
             'email': 'mobile-mavericks@broadcast.com', 'slack': '#mobile-mavericks',
             'jira': 'MM', 'standup': '09:15 daily'},
            {'name': 'UX Unicorns', 'dept': 'Mobile', 'color': '#6D28D9',
             'mission': 'User experience research, design and accessibility across all mobile products.',
             'skills': ['Figma', 'User Research', 'Accessibility', 'Prototyping', 'Design Tokens'],
             'repos': ['ux-components', 'accessibility-toolkit', 'design-tokens'],
             'email': 'ux-unicorns@broadcast.com', 'slack': '#ux-unicorns',
             'jira': 'UX', 'standup': '10:00 daily'},
            # Reliability & Tools
            {'name': 'SRE Squad', 'dept': 'Reliability & Tools', 'color': '#F59E0B',
             'mission': 'Site reliability engineering, incident management and on-call operations.',
             'skills': ['Prometheus', 'Grafana', 'PagerDuty', 'Kubernetes', 'Python', 'Go'],
             'repos': ['sre-runbooks', 'monitoring-stack', 'incident-tracker'],
             'email': 'sre-squad@broadcast.com', 'slack': '#sre-squad',
             'jira': 'SRE', 'standup': '08:30 daily'},
            {'name': 'DevEx Team', 'dept': 'Reliability & Tools', 'color': '#D97706',
             'mission': 'Developer experience, tooling and productivity platforms for all engineering teams.',
             'skills': ['GitHub Actions', 'ArgoCD', 'Backstage', 'VS Code Extensions', 'CLI Tools'],
             'repos': ['devex-portal', 'internal-cli', 'cicd-templates'],
             'email': 'devex@broadcast.com', 'slack': '#devex',
             'jira': 'DEX', 'standup': '09:00 daily'},
            # Architecture & Programme
            {'name': 'Tech Council', 'dept': 'Architecture & Programme', 'color': '#EF4444',
             'mission': 'Technical strategy, architecture reviews and cross-team standards governance.',
             'skills': ['System Design', 'Architecture Review', 'RFC Process', 'Documentation', 'Mentoring'],
             'repos': ['architecture-decisions', 'tech-standards', 'rfcs'],
             'email': 'tech-council@broadcast.com', 'slack': '#tech-council',
             'jira': 'TC', 'standup': '10:00 weekly'},
            {'name': 'Programme Delivery', 'dept': 'Architecture & Programme', 'color': '#DC2626',
             'mission': 'Cross-team programme management, roadmap coordination and delivery tracking.',
             'skills': ['Programme Management', 'Roadmapping', 'OKRs', 'Stakeholder Management', 'Jira'],
             'repos': ['programme-tracker', 'roadmap-docs'],
             'email': 'programme@broadcast.com', 'slack': '#programme-delivery',
             'jira': 'PD', 'standup': '09:00 daily'},
            {'name': 'Platform Architecture', 'dept': 'Architecture & Programme', 'color': '#B91C1C',
             'mission': 'Platform-wide architecture patterns, reference implementations and capability roadmap.',
             'skills': ['Domain-Driven Design', 'Microservices', 'Event Sourcing', 'API Strategy', 'Cloud Native'],
             'repos': ['platform-arch', 'reference-services'],
             'email': 'platform-arch@broadcast.com', 'slack': '#platform-architecture',
             'jira': 'PA', 'standup': '09:30 daily'},
            # Reliability & Tools — extra team to satisfy 3-per-dept minimum
            {'name': 'Observability Crew', 'dept': 'Reliability & Tools', 'color': '#FB923C',
             'mission': 'Logging, metrics, tracing and incident response tooling across the platform.',
             'skills': ['Prometheus', 'Grafana', 'OpenTelemetry', 'Loki', 'Incident Response'],
             'repos': ['observability-stack', 'alert-rules', 'oncall-runbooks'],
             'email': 'observability@broadcast.com', 'slack': '#observability',
             'jira': 'OBS', 'standup': '09:15 daily'},
        ]

        # Create engineer users per team
        engineer_names = [
            ('alex.nguyen', 'Alex', 'Nguyen'), ('priya.gupta', 'Priya', 'Gupta'),
            ('sarah.chen', 'Sarah', 'Chen'), ('david.park', 'David', 'Park'),
            ('emma.wilson', 'Emma', 'Wilson'), ('mike.torres', 'Mike', 'Torres'),
            ('rachel.kim', 'Rachel', 'Kim'), ('james.mitchell', 'James', 'Mitchell'),
            ('nina.patel', 'Nina', 'Patel'), ('ryan.scott', 'Ryan', 'Scott'),
            ('jade.kim', 'Jade', 'Kim'), ('tom.harris', 'Tom', 'Harris'),
            ('omar.hassan', 'Omar', 'Hassan'), ('carlos.mendez', 'Carlos', 'Mendez'),
            ('yuki.tanaka', 'Yuki', 'Tanaka'), ('fatima.rashid', 'Fatima', 'Al-Rashid'),
            ('sam.taylor', 'Sam', 'Taylor'), ('mia.chen', 'Mia', 'Chen'),
            ('ben.ali', 'Ben', 'Ali'), ('olivia.park', 'Olivia', 'Park'),
            ('jake.miller', 'Jake', 'Miller'), ('lisa.park', 'Lisa', 'Park'),
            ('dan.brown', 'Dan', 'Brown'), ('sophie.wang', 'Sophie', 'Wang'),
            ('anna.lee', 'Anna', 'Lee'), ('mark.davis', 'Mark', 'Davis'),
            ('eva.green', 'Eva', 'Green'), ('phil.chang', 'Phil', 'Chang'),
            ('chen.wei', 'Chen', 'Wei'), ('amir.patel', 'Amir', 'Patel'),
            ('tina.ross', 'Tina', 'Ross'), ('li.wei', 'Li', 'Wei'),
        ]

        engineers = []
        for uname, first, last in engineer_names:
            u, _ = User.objects.get_or_create(username=uname, defaults={
                'email': f'{uname}@broadcast.com', 'first_name': first, 'last_name': last,
            })
            u.set_password('nexora123')
            u.save()
            UserProfile.objects.get_or_create(user=u)
            engineers.append(u)

        # Create demo user
        demo, _ = User.objects.get_or_create(username='john.doe', defaults={
            'email': 'john.doe@broadcast.com', 'first_name': 'John', 'last_name': 'Doe',
        })
        demo.set_password('demo123')
        demo.save()
        UserProfile.objects.get_or_create(user=demo)

        # Create teams
        created_teams = {}
        import random
        random.seed(42)
        for i, td in enumerate(teams_data):
            dept = depts.get(td['dept'])
            manager = engineers[i % len(engineers)]
            team, _ = Team.objects.get_or_create(name=td['name'], defaults={
                'department': dept, 'manager': manager,
                'manager_email': f"{manager.username}@broadcast.com",
                'mission': td['mission'], 'description': td['mission'],
                'status': 'Active', 'email': td['email'],
                'slack_channel': td['slack'], 'color': td['color'],
                'standup_time': td['standup'], 'jira_project': td['jira'],
            })
            created_teams[td['name']] = team
            # Add skills
            for skill_name in td['skills']:
                Skill.objects.get_or_create(team=team, name=skill_name)
            # Add repos
            for repo_name in td['repos']:
                Repository.objects.get_or_create(team=team, name=repo_name, defaults={'url': f'https://github.com/broadcast/{repo_name}'})
            # Add members (5-7 per team)
            roles = ['Team Lead', 'Senior Engineer', 'Engineer', 'Engineer', 'Engineer', 'DevOps', 'QA Engineer']
            member_pool = engineers[i*2:(i*2)+6] or engineers[:6]
            TeamMember.objects.get_or_create(team=team, user=manager, defaults={'role': 'Team Lead'})
            for j, eng in enumerate(member_pool[:5]):
                if eng != manager:
                    TeamMember.objects.get_or_create(team=team, user=eng, defaults={'role': roles[min(j+1, len(roles)-1)]})
            TeamMember.objects.get_or_create(team=team, user=demo, defaults={'role': 'Engineer'})

        # Spec: every team must have >= 5 engineers. Backfill any short teams.
        for team in Team.objects.all():
            while team.members.count() < 5:
                existing_ids = set(team.members.values_list('user_id', flat=True))
                candidate = next((e for e in engineers if e.pk not in existing_ids), None)
                if candidate is None:
                    break
                TeamMember.objects.create(team=team, user=candidate, role='Engineer')

        # Create dependencies between teams
        dep_pairs = [
            ('Code Warriors', 'Full Stack Ninjas', 'Infrastructure Support'),
            ('Full Stack Ninjas', 'The Debuggers', 'Bug Resolution'),
            ('Bit Masters', 'Code Warriors', 'Security Compliance'),
            ('Data Wranglers', 'Full Stack Ninjas', 'Data Feed'),
            ('SRE Squad', 'Code Warriors', 'Infrastructure Support'),
            ('SRE Squad', 'TV Pioneers', 'Infrastructure Support'),
            ('Stream Team', 'Screen Wizards', 'API Integration'),
            ('App Architects', 'Mobile Mavericks', 'Infrastructure Support'),
            ('Tech Council', 'Programme Delivery', 'General'),
            ('DevEx Team', 'Code Warriors', 'Deployment'),
        ]
        for from_name, to_name, dep_type in dep_pairs:
            from_t = created_teams.get(from_name)
            to_t = created_teams.get(to_name)
            if from_t and to_t:
                TeamDependency.objects.get_or_create(from_team=from_t, to_team=to_t, defaults={'dependency_type': dep_type})

        # Helper to fetch user by username
        def U(name):
            return User.objects.filter(username=name).first()

        sarah = U('sarah.chen'); david = U('david.park'); priya = U('priya.gupta')
        emma = U('emma.wilson'); mike = U('mike.torres'); rachel = U('rachel.kim')
        james = U('james.mitchell'); alex = U('alex.nguyen')

        # Inbox messages from various engineers (matches the dashboard screenshot)
        inbox_msgs = [
            (sarah, 'API Integration Query',
             "Hi John,\n\nI wanted to discuss the new API endpoints we need for the Platform Core integration. We've identified three key areas that need updates:\n\n1. User authentication endpoint — OAuth 2.0 support\n2. Team directory API — department filtering\n3. New dependency mapping query endpoint\n\nCould you review these requirements and let me know if your team can take this on in the next sprint?\n\nBest regards,\nSarah Chen\nPlatform Core Team Lead"),
            (david, 'Cloud Migration Timeline Update',
             "Hi John,\n\nThe migration schedule has been updated. Phase 2 will now begin next month due to the security audit requirements.\n\nKey changes:\n- Database migration pushed to next month\n- Service mesh deployment follows after\n\nDavid"),
            (priya, 'Could you grant our team access to the staging cluster?',
             "Hi John,\n\nWe need access to the staging cluster to validate the new API endpoints. Could you grant our team access by Thursday?\n\nThanks,\nPriya"),
            (emma, "I've completed the review of the new API spec",
             "Hi,\n\nI've completed the review of the new API spec. Overall it looks solid, just a few comments on the auth flow. Document attached.\n\nEmma"),
            (mike, 'QA Test Results — Sprint 12',
             "All regression tests passed for Sprint 12. Full report attached. Ready for release sign-off.\n\nMike"),
            (rachel, 'Re: Q2 infrastructure budget',
             "Forwarding the latest Q2 infra budget breakdown. Let me know if you have feedback.\n\nRachel"),
            (james, 'Welcome to the Engineering Portal',
             "Welcome aboard! I wanted to personally introduce myself and offer help with onboarding. Let me know if you need anything.\n\nJames"),
        ]
        from django.utils import timezone
        from datetime import timedelta as _td
        now_ts = timezone.now()
        # Offsets so inbox order matches screenshot: Sarah newest, James oldest
        offsets = [_td(hours=2), _td(days=1), _td(days=1, hours=2), _td(days=14), _td(days=15), _td(days=18), _td(days=19)]
        for (sender, subj, body), off in zip(inbox_msgs, offsets):
            if sender:
                m, created = Message.objects.get_or_create(
                    sender=sender, recipient=demo, subject=subj,
                    defaults={'body': body, 'status': 'inbox', 'is_read': False}
                )
                if created:
                    Message.objects.filter(pk=m.pk).update(created_at=now_ts - off)

        # Sent messages
        if alex:
            Message.objects.get_or_create(
                sender=demo, recipient=alex, subject='Re: Architecture Review Notes',
                defaults={'body': "Hi Alex,\n\nThanks for the review notes. I'll incorporate the feedback into the next revision.\n\nJohn", 'status': 'sent'}
            )

        # Draft
        Message.objects.get_or_create(
            sender=demo, recipient=None, subject='Team Restructuring Proposal',
            defaults={'body': 'Hi team,\n\nI would like to propose the following changes to our team structure...\n\n[TODO: Add details]', 'status': 'draft'}
        )

        # Sample meetings (spread across current month + upcoming)
        today_d = date.today()
        engineers = list(User.objects.exclude(username__in=['admin', 'john.doe'])[:8])
        meetings_data = [
            {'title': 'Sprint 13 Planning', 'd': today_d - timedelta(days=2), 's': time(10, 0), 'e': time(11, 0), 'p': 'teams'},
            {'title': 'API Integration Sync', 'd': today_d + timedelta(days=1), 's': time(13, 0), 'e': time(14, 0), 'p': 'zoom'},
            {'title': 'Cloud Migration Review', 'd': today_d + timedelta(days=3), 's': time(9, 0), 'e': time(10, 0), 'p': 'meet'},
            {'title': 'Frontend Component Demo', 'd': today_d + timedelta(days=5), 's': time(15, 0), 'e': time(16, 0), 'p': 'zoom'},
            {'title': 'QA Review - Sprint 12', 'd': today_d + timedelta(days=7), 's': time(11, 0), 'e': time(11, 30), 'p': 'teams'},
            {'title': 'Infrastructure Budget Sync', 'd': today_d + timedelta(days=8), 's': time(14, 0), 'e': time(15, 0), 'p': 'zoom'},
            {'title': 'API Spec Review', 'd': today_d, 's': time(10, 0), 'e': time(11, 30), 'p': 'teams'},
            {'title': 'Sprint 13 Planning', 'd': today_d + timedelta(days=10), 's': time(10, 0), 'e': time(11, 0), 'p': 'teams'},
            {'title': 'Dept Standup', 'd': today_d + timedelta(days=12), 's': time(8, 30), 'e': time(10, 0), 'p': 'slack'},
            {'title': 'Dependency Mapping Workshop', 'd': today_d + timedelta(days=12), 's': time(13, 0), 'e': time(15, 0), 'p': 'in_person'},
            {'title': 'Security Audit Prep', 'd': today_d + timedelta(days=14), 's': time(11, 0), 'e': time(13, 0), 'p': 'meet'},
            {'title': 'End of Month Retro', 'd': today_d + timedelta(days=17), 's': time(15, 0), 'e': time(16, 30), 'p': 'zoom'},
        ]
        for md in meetings_data:
            mt, created = Meeting.objects.get_or_create(
                creator=demo, title=md['title'], date=md['d'],
                defaults={'start_time': md['s'], 'end_time': md['e'], 'platform': md['p']}
            )
            if created and engineers:
                import random
                mt.participants.set(random.sample(engineers, min(3, len(engineers))))

        self.stdout.write(self.style.SUCCESS(f'''
Database seeded successfully!

LOGIN CREDENTIALS:
  Admin:    username=admin        password=admin123
  Demo:     username=john.doe     password=demo123
  Engineer: username=sarah.chen   password=nexora123

Teams created: {Team.objects.count()}
Departments:   {Department.objects.count()}
Members:       {TeamMember.objects.count()}
Messages:      {Message.objects.count()}
Meetings:      {Meeting.objects.count()}
        '''))
