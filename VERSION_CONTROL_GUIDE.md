# Nexora Version Control Guide

This guide matches the 5COSC021W CWK2 requirement to discuss version control, integration, compatibility, and individual contribution evidence.

Important integrity rule: do not fabricate commit history or backdate commits. Git evidence should show real commits, real authors, and real work. If work was originally completed outside Git, explain that honestly and use this handoff to create clean branches and traceable final commits from each student.

## How This Handoff Is Divided

Each ZIP contains the full runnable Django project so the marker can open and run it, but each student push is divided by file ownership. The Bash scripts in `C:\Users\voidb\Downloads\nexora_handoff\git_push_scripts` do not run `git add .`; they stage only the files listed in `git_push_scripts/filelists/<student>.txt`.

The scripts use `git push --force-with-lease` for the student branches. This is a force push, but it avoids overwriting newer remote work that your local Git has not fetched.

Each ZIP also contains a student-specific `COMMIT_SEQUENCE.md`. That file shows the staged checkpoint format, date labels for Trello, commit-message examples, and files to stage for that student.

## Coursework Requirements Read From The Brief

- The project must be a Django web application using SQLite.
- CWK2 requires all code and database files needed to run the Django project.
- The individual template must discuss the code implemented, integration between individual parts, version control, test-plan output, UI/UX principles, security risks, legal/ethical constraints, and peer feedback.
- Trello must be used regularly for meeting notes, agreements, online discussion, research links, and evidence of time/project management.
- The four-student allocation table assigns:
  - Student 1: Teams menu.
  - Student 2: Organisation, departments, dependencies.
  - Student 3: Messages.
  - Student 4: Schedule.
- Group tasks include database handling, user authentication, admin panel, form handling, integration, and review.

## Agreed Team Ownership

| Student | Main Ownership | Additional Ownership |
|---|---|---|
| Pranaya | Teams list, team search, team detail modal, skills, upstream/downstream dependency display | Team actions that open messaging and schedule flows |
| Savya | Admin dashboard, Django admin grouping, organisation, departments, dependencies | Reports/admin navigation, shared base layout, final integration review |
| Gahana | Landing page, database implementation, seed data, migrations, data relationships | Messages module as Student 3 allocation |
| Shradha | Sign-in/sign-up pages, authentication/profile flows | Schedule/calendar module as Student 4 allocation |

## What Each Student Should Push

Push each contribution on a separate branch. Do not push generated cache files such as `__pycache__/`, `.pyc`, `.coverage`, `local_tools/`, or local helper scripts.

### Savya Branch: `savya/admin-organisation`

Push:
- `manage.py`, `requirements.txt`
- `nexora_project/`
- `templates/base.html`
- `templates/admin/`
- `organisation/`
- `templates/organisation/`
- `reports/`
- `templates/reports/`
- `static/css/style.css`
- `STUDENT_INFO.md`, `COMMIT_SEQUENCE.md`, `VERSION_CONTROL_GUIDE.md`, `TRELLO_BOARD_PLAN.md`, `PUSH_ORDER.md`

Run from the extracted `nexora_savya` folder:

```bash
/c/Users/voidb/Downloads/nexora_handoff/git_push_scripts/push_savya.sh <remote-url>
```

### Gahana Branch: `gahana/database-landing-messaging`

Push:
- `nexora.db` if the tutor requires the SQLite database artifact in version control
- all app models and migrations that define the database schema
- `accounts/management/commands/seed_data.py`
- `core/`
- `templates/core/`
- `messaging/`
- `templates/messaging/`
- `DATABASE_IMPLEMENTATION.md`
- `STUDENT_INFO.md`, `COMMIT_SEQUENCE.md`, `VERSION_CONTROL_GUIDE.md`, `TRELLO_BOARD_PLAN.md`, `PUSH_ORDER.md`

Run from the extracted `nexora_gahana` folder:

```bash
/c/Users/voidb/Downloads/nexora_handoff/git_push_scripts/push_gahana.sh <remote-url>
```

### Shradha Branch: `shradha/auth-schedule`

Push:
- `accounts/admin.py`, `accounts/apps.py`, `accounts/forms.py`, `accounts/tests.py`, `accounts/urls.py`, `accounts/views.py`, `accounts/__init__.py`
- `templates/accounts/`
- `schedule_app/admin.py`, `schedule_app/apps.py`, `schedule_app/tests.py`, `schedule_app/urls.py`, `schedule_app/utils.py`, `schedule_app/views.py`, `schedule_app/__init__.py`
- `templates/schedule_app/`
- `STUDENT_INFO.md`, `COMMIT_SEQUENCE.md`, `VERSION_CONTROL_GUIDE.md`, `TRELLO_BOARD_PLAN.md`, `PUSH_ORDER.md`

Run from the extracted `nexora_shradha` folder:

```bash
/c/Users/voidb/Downloads/nexora_handoff/git_push_scripts/push_shradha.sh <remote-url>
```

### Pranaya Branch: `pranaya/teams`

Push:
- `teams/admin.py`, `teams/apps.py`, `teams/tests.py`, `teams/urls.py`, `teams/views.py`, `teams/__init__.py`
- `templates/teams/`
- `STUDENT_INFO.md`, `COMMIT_SEQUENCE.md`, `VERSION_CONTROL_GUIDE.md`, `TRELLO_BOARD_PLAN.md`, `PUSH_ORDER.md`

Run from the extracted `nexora_pranaya` folder:

```bash
/c/Users/voidb/Downloads/nexora_handoff/git_push_scripts/push_pranaya.sh <remote-url>
```

## Push Order

1. Savya pushes `savya/admin-organisation` first because it contains the project shell, admin dashboard, shared base template, and navigation.
2. Gahana pushes `gahana/database-landing-messaging` next because the database schema, seed data, landing page, and messaging depend on the project shell.
3. Shradha pushes `shradha/auth-schedule` next because login/signup and schedule flows rely on the shared base and database.
4. Pranaya pushes `pranaya/teams` next because teams link into messaging and schedule.
5. Savya or the group lead creates `integration/final-nexora`, merges the four branches, resolves conflicts, runs tests, and records final Trello review notes.

## Optional Local Python Helper

The local helper is:

`C:\Users\voidb\Downloads\nexora_handoff\local_tools\make_real_student_commits.py`

It is intentionally outside the ZIP Git content and should not be committed. It creates real current-date checkpoint commits using the same divided sequence as the `COMMIT_SEQUENCE.md` files.

Example from an extracted student folder:

```bash
python /c/Users/voidb/Downloads/nexora_handoff/local_tools/make_real_student_commits.py gahana --remote <remote-url>
```

## Evidence To Keep

- `git log --stat --author="<student name>"`
- screenshots of Trello cards with comments, due dates, checklists, and review notes
- test output from `python manage.py test`
- screenshots/video showing each student feature working
- notes on peer feedback and what changed after review

## Files Not To Push

- `build_git_history.py` or any script that fabricates/backdates commits
- `local_tools/`
- `git_push_scripts/`
- `commit_sequences/`
- `__pycache__/`
- `*.pyc`
- `.coverage`
- local virtual environments
- editor folders such as `.vscode/`, unless the team intentionally agrees
