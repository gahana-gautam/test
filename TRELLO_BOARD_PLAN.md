# Trello Board Plan

Use four Trello lists named exactly like the screenshot: `savya`, `gahana`, `shradha`, `pranaya`.

Do not invent completed evidence. Add real comments, screenshots, meeting links, Git branch links, and review notes to each card. The dates below are a planning structure for showing project management over the April 20 to May 6 work window.

## List: savya

| Card | Date Label | Checklist Items |
|---|---|---|
| Personal setup | Apr 20 - Apr 21 | install Python/Django; confirm app runs; join Git repo |
| Project Setup | Apr 20 - Apr 22 | create Django project shell; configure settings; wire root URLs |
| Admin Dashboard | Apr 22 - Apr 24 | custom admin site; admin grouping; admin index quick links |
| Base Template + Dashboard Shell | Apr 23 - Apr 26 | sidebar; topbar; notifications; staff-only nav |
| Organisation Backend | Apr 24 - Apr 27 | organisation URLs/views; departments query; dependencies query |
| Departments Front-end | Apr 27 - Apr 29 | department cards; department detail; search/empty state |
| Dependencies Front-end | Apr 29 - May 1 | dependency map; upstream/downstream matrix; relationship labels |
| Reports/Admin Integration | May 1 - May 3 | admin report links; reports menu visibility; staff flow review |
| Integration Review | May 4 - May 6 | merge review; run tests; record known issues |

## List: gahana

| Card | Date Label | Checklist Items |
|---|---|---|
| Personal setup | Apr 20 - Apr 21 | clone/extract project; run migrations; review database brief |
| Database Schema + Migrations | Apr 20 - Apr 23 | verify models; run migrate; document table relationships |
| Seed Data | Apr 22 - Apr 25 | users; departments; teams; skills; repos; dependencies; messages; meetings |
| Landing Page | Apr 23 - Apr 25 | public page; navigation; CTA buttons; responsive check |
| Dashboard + Search | Apr 25 - Apr 27 | stats from DB; global search; unread count |
| Messaging Models | Apr 26 - Apr 28 | message table; attachment table; admin registration |
| Inbox View | Apr 28 - Apr 30 | received messages; unread state; thread data |
| Sent + Drafts Views | Apr 30 - May 1 | sent messages; draft list; draft edit |
| Message Detail | May 1 - May 2 | thread render; mark-read endpoint; attachments |
| New Message Compose | May 2 - May 4 | direct/group compose; validation; save draft; reply/forward |
| Database QA | May 4 - May 5 | rebuild DB from migrations; seed data test; count records |
| Final DB Handoff | May 5 - May 6 | include SQLite artifact if required; document setup steps |

## List: shradha

| Card | Date Label | Checklist Items |
|---|---|---|
| Personal setup | Apr 20 - Apr 21 | run project locally; review auth/schedule scope |
| Sign-in Page | Apr 21 - Apr 23 | login form; email/username login; invalid credentials |
| Sign-up Page | Apr 22 - Apr 24 | register form; email domain check; password rules |
| Forgot Password + Profile | Apr 24 - Apr 26 | forgot password screen; profile page; avatar/profile edit |
| Account Settings | Apr 26 - Apr 27 | password change; notification toggles; validation messages |
| Schedule Model | Apr 27 - Apr 28 | meeting model; participants; migrations |
| Calendar Month View | Apr 28 - Apr 30 | month grid; meeting chips; today marker |
| Week + Upcoming Views | Apr 30 - May 1 | week grid; day timeline; upcoming list |
| New Meeting Form | May 1 - May 3 | date/time; platform; attendees; description |
| Meeting Detail | May 3 - May 4 | view modal; edit; cancel; permission checks |
| Email Notifications | May 4 - May 5 | console email backend; notification helper; attendee emails |
| Auth + Schedule Tests | May 5 - May 6 | unit tests; validation tests; demo checklist |

## List: pranaya

| Card | Date Label | Checklist Items |
|---|---|---|
| Personal setup | Apr 20 - Apr 21 | run project locally; inspect team requirements |
| Team Data Model Review | Apr 21 - Apr 23 | Team; TeamMember; Skill; Repository; TeamDependency |
| Teams List Page | Apr 23 - Apr 25 | grid cards; list rows; department/status display |
| Search + Filters | Apr 25 - Apr 26 | team name search; department filter; empty state |
| Team Detail JSON | Apr 26 - Apr 28 | endpoint; members; skills; repos; dependencies |
| Team Detail Modal | Apr 28 - Apr 30 | modal render; manager/contact; member list |
| Skills + Repositories Display | Apr 30 - May 1 | skills chips; GitHub repo links |
| Dependencies Display | May 1 - May 2 | upstream/downstream counts; dependency labels |
| Email Team Integration | May 2 - May 3 | link to messaging compose with team prefill |
| Schedule Team Integration | May 3 - May 4 | link to schedule page with team participants |
| Teams Test Cases | May 4 - May 5 | list view; search; JSON detail tests |
| JS Polish + Responsive | May 5 - May 6 | modal close; grid/list toggle; final demo review |

## Suggested Trello Evidence Comments

Add comments like these only when they match real work:

- "Pushed branch `<branch-name>` with `<feature>` implementation."
- "Reviewed by `<teammate>`; changed `<specific issue>` after feedback."
- "Tested with `python manage.py test <app>`; result: `<pass/fail summary>`."
- "Screenshot/video attached for demo evidence."
- "Integration issue found: `<issue>`; fixed in commit `<hash>`."
