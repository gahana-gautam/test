# Database Implementation - Gahana Ownership

Gahana owns the database implementation handoff for the final Nexora package.

## Database Scope

The project uses Django models and SQLite. The database work is not only the `nexora.db` file; it also includes the schema definitions, migrations, seed data, and relationships that allow the individual pages to integrate into one application.

## Files To Push Under Gahana

- `nexora.db` - coursework SQLite database artifact, if required by the tutor for runnable submission.
- `accounts/management/commands/seed_data.py` - sample departments, teams, users, team members, skills, repositories, dependencies, messages, and meetings.
- `accounts/migrations/`
- `teams/migrations/`
- `messaging/migrations/`
- `schedule_app/migrations/`
- `reports/migrations/`
- `accounts/models.py`
- `teams/models.py`
- `messaging/models.py`
- `schedule_app/models.py`
- `reports/models.py`

## Main Tables And Relationships

- `auth_user`: Django user accounts.
- `accounts_userprofile`: one profile per user.
- `teams_department`: departments and department heads.
- `teams_team`: teams linked to departments and managers.
- `teams_teammember`: many users assigned to teams.
- `teams_skill`: skills per team.
- `teams_repository`: code repositories per team.
- `teams_teamdependency`: upstream/downstream relationships between teams.
- `messaging_message`: internal messages, inbox/sent/draft state.
- `messaging_attachment`: uploaded message attachments.
- `schedule_app_meeting`: meetings created by users.
- `schedule_app_meeting_participants`: many-to-many attendees.
- `reports_auditlog`: audit trail for create/update/delete events.

## How To Rebuild The Database

```bash
python manage.py migrate
python manage.py seed_data
```

## How To Verify

```bash
python manage.py test
python manage.py shell -c "from teams.models import Team; print(Team.objects.count())"
```

## Notes For The Individual Template

Explain that the database was implemented through Django ORM models and migrations so every individual module can share the same source of data. Mention that seed data was added so the team directory, messaging, schedule, organisation, reports, and charts all demonstrate realistic records during marking.
