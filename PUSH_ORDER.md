# Push Order

Use this order when pushing branches to the shared Git remote.

1. `savya/admin-organisation`
   - Base project shell, admin dashboard, shared layout, organisation pages.
2. `gahana/database-landing-messaging`
   - SQLite database artifact if required, migrations, seed data, landing/dashboard/search, messaging.
3. `shradha/auth-schedule`
   - Login/signup/profile and schedule/calendar flows.
4. `pranaya/teams`
   - Teams directory, team detail modal, dependencies, email/schedule team actions.
5. `integration/final-nexora`
   - Merge all branches, run tests, fix conflicts, record final Trello review notes.

Each student should push to their own branch first. Do not have all students push directly to `main`.

The provided Bash scripts stage only the divided file list for that student:

- `git_push_scripts/filelists/savya.txt`
- `git_push_scripts/filelists/gahana.txt`
- `git_push_scripts/filelists/shradha.txt`
- `git_push_scripts/filelists/pranaya.txt`

Suggested commands:

```bash
git fetch origin
git checkout -b integration/final-nexora origin/main
git merge origin/savya/admin-organisation
git merge origin/gahana/database-landing-messaging
git merge origin/shradha/auth-schedule
git merge origin/pranaya/teams
python manage.py test
git push -u origin integration/final-nexora
```
