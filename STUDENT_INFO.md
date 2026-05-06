# Gahana - Student 3 Contribution

## Main Responsibility

Gahana owns the landing page, database implementation handoff, and messages module.

## Coursework Mapping

Student 3 in the four-student allocation table is responsible for:
- Messages menu
- New Message
- Inbox
- Sent
- Draft
- Send new message

The group database task is also assigned to Gahana for this handoff.

## Files To Push

- `nexora.db`, if required for coursework submission
- `DATABASE_IMPLEMENTATION.md`
- `accounts/management/commands/seed_data.py`
- all app migration folders
- model files used to define the shared schema
- `core/`
- `templates/core/`
- `messaging/`
- `templates/messaging/`
- `COMMIT_SEQUENCE.md`

## Implemented Features

- Public landing page.
- Dashboard/search data integration.
- Shared SQLite schema through Django models and migrations.
- Seed data for users, departments, teams, skills, repositories, dependencies, messages, and meetings.
- Inbox, sent, and draft message views.
- Direct/group compose flow.
- Reply, forward, delete, draft edit, unread count, rich text, mentions, emoji, and attachments.

## Suggested Branch And Commits

Branch: `gahana/database-landing-messaging`

Suggested real commit sequence:
Use `COMMIT_SEQUENCE.md` in this ZIP for the full staged sequence and Trello date labels.

## Demo Checklist

- Open the landing page.
- Log in and show dashboard counts loaded from the database.
- Run `python manage.py seed_data` on a clean database.
- Open Messages.
- Show inbox, sent, and drafts.
- Compose and send a message.
- Save and reopen a draft.
- Upload an attachment.
