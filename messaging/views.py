from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import date, timedelta
import json

from .models import Message, Attachment


def _initials(u):
    if not u:
        return "??"
    f = u.first_name[:1].upper() if u.first_name else ""
    l = u.last_name[:1].upper() if u.last_name else ""
    return (f + l) or u.username[:2].upper()


def _user_team(u):
    try:
        from teams.models import TeamMember
        tm = TeamMember.objects.filter(user=u).select_related("team").first()
        return tm.team.name if tm else ""
    except Exception:
        return ""


def _time_label(when, now):
    when_local = timezone.localtime(when) if timezone.is_aware(when) else when
    now_local = timezone.localtime(now) if timezone.is_aware(now) else now
    today = now_local.date()
    msg_date = when_local.date()
    if msg_date == today:
        return when_local.strftime("%I:%M %p").lstrip("0")
    if msg_date == today - timedelta(days=1):
        return "Yesterday"
    return when_local.strftime("%d %b")


def _fmt_full(when):
    when_local = timezone.localtime(when) if timezone.is_aware(when) else when
    return when_local.strftime("%d %b, %I:%M %p").replace(" 0", " ")


@login_required
def messages_view(request):
    me = request.user
    me_initials = _initials(me)
    now = timezone.now()

    # ---- INBOX: dedupe by (sender, subject), keep newest per thread ----
    inbox_all = list(
        Message.objects.filter(recipient=me, status__in=["inbox", "sent"])
        .select_related("sender")
        .order_by("-created_at")
    )
    inbox_rows = []
    seen_inbox = set()
    for m in inbox_all:
        key = (m.sender_id, m.subject)
        if key in seen_inbox:
            continue
        seen_inbox.add(key)
        unread_count = sum(1 for x in inbox_all if x.sender_id == m.sender_id and x.subject == m.subject and not x.is_read)
        inbox_rows.append({"msg": m, "time_label": _time_label(m.created_at, now), "unread_count": unread_count})

    # ---- SENT: dedupe by (recipient/team, subject) ----
    sent_all = list(
        Message.objects.filter(sender=me, status="sent")
        .select_related("recipient")
        .order_by("-created_at")
    )
    sent_rows = []
    seen_sent = set()
    for m in sent_all:
        key = (m.recipient_id, m.recipient_team_name, m.subject)
        if key in seen_sent:
            continue
        seen_sent.add(key)
        sent_rows.append({"msg": m, "time_label": _time_label(m.created_at, now)})

    drafts = list(Message.objects.filter(sender=me, status="draft").select_related("recipient").order_by("-created_at"))

    unread_count = sum(1 for m in inbox_all if not m.is_read)
    all_users = User.objects.exclude(id=me.id).order_by("first_name", "last_name")

    # ---- Build messageData JS object ----
    message_data = {}

    def thread_for(other_user, subject):
        qs = Message.objects.filter(
            Q(sender=me, recipient=other_user) | Q(sender=other_user, recipient=me),
            subject=subject,
        ).order_by("created_at").prefetch_related("attachments")
        out = []
        for tm in qs:
            is_me = tm.sender_id == me.id
            atts = []
            for a in tm.attachments.all():
                atts.append({
                    "name": a.original_name,
                    "url": a.file.url if a.file else "",
                    "size": a.size,
                })
            out.append({
                "from": "You" if is_me else (tm.sender.get_full_name() or tm.sender.username),
                "initials": me_initials if is_me else _initials(tm.sender),
                "time": _fmt_full(tm.created_at),
                "text": tm.body,
                "me": is_me,
                "attachments": atts,
            })
        return out

    for idx, row in enumerate(inbox_rows):
        m = row["msg"]
        message_data[f"inbox-{idx}"] = {
            "kind": "inbox",
            "serverId": m.pk,
            "name": m.sender.get_full_name() or m.sender.username,
            "initials": _initials(m.sender),
            "email": m.sender.email or f"{m.sender.username}@nexora.com",
            "team": _user_team(m.sender),
            "subject": m.subject,
            "messages": thread_for(m.sender, m.subject),
        }

    for idx, row in enumerate(sent_rows):
        m = row["msg"]
        if m.recipient:
            other = m.recipient
            name = other.get_full_name() or other.username
            email = other.email or f"{other.username}@nexora.com"
            initials = _initials(other)
            team = _user_team(other)
            messages = thread_for(other, m.subject)
            is_group = m.is_group
        else:
            name = m.recipient_team_name or "Group"
            initials = (m.recipient_team_name[:2].upper() if m.recipient_team_name else "GR")
            email = ""
            team = "Group Message"
            messages = [{
                "from": "You", "initials": me_initials,
                "time": _fmt_full(m.created_at), "text": m.body, "me": True,
            }]
            is_group = True
        message_data[f"sent-{idx}"] = {
            "kind": "sent",
            "serverId": m.pk,
            "name": name,
            "initials": initials,
            "email": email,
            "team": team,
            "subject": m.subject,
            "isGroup": is_group,
            "messages": messages,
        }

    for idx, m in enumerate(drafts):
        recipient_name = (
            (m.recipient.get_full_name() or m.recipient.username) if m.recipient
            else (m.recipient_team_name or "(no recipient)")
        )
        recipient_initials = (_initials(m.recipient) if m.recipient
                              else (m.recipient_team_name[:2].upper() if m.recipient_team_name else "GR"))
        message_data[f"draft-{idx}"] = {
            "kind": "draft",
            "serverId": m.pk,
            "name": recipient_name,
            "initials": recipient_initials,
            "email": "",
            "team": "Draft" + (" — Group" if m.is_group else " — Direct"),
            "subject": m.subject,
            "isDraft": True,
            "isGroup": m.is_group,
            "messages": [{
                "from": "You", "initials": me_initials,
                "time": "Draft — " + timezone.localtime(m.created_at).strftime("%d %b"),
                "text": m.body, "me": True, "draft": True,
            }],
        }

    all_users_for_mention = [
        {"id": u.pk, "name": (u.get_full_name() or u.username),
         "username": u.username, "initials": _initials(u)}
        for u in all_users
    ]

    # Compose prefill: ?team=<id> auto-opens compose with team's manager + members as recipients
    prefill_team = None
    prefill_recipient_ids = []
    team_id = request.GET.get("team")
    if team_id:
        try:
            from teams.models import Team
            team = Team.objects.select_related("manager").prefetch_related("members__user").get(pk=team_id)
            prefill_team = {
                "id": team.pk, "name": team.name,
                "subject": f"Message to {team.name}",
            }
            ids = []
            if team.manager_id and team.manager_id != me.id:
                ids.append(team.manager_id)
            for tm in team.members.all():
                if tm.user_id != me.id and tm.user_id not in ids:
                    ids.append(tm.user_id)
            prefill_recipient_ids = ids
        except Exception:
            pass

    # Compose prefill: ?reply=<id> or ?forward=<id>
    prefill_mode = None
    prefill_subject = ""
    prefill_body = ""
    prefill_single_recipient = None
    rid = request.GET.get("reply") or request.GET.get("forward")
    if rid:
        try:
            parent = Message.objects.get(pk=rid)
            if parent.sender_id == me.id or parent.recipient_id == me.id:
                if request.GET.get("reply"):
                    prefill_mode = "reply"
                    prefill_subject = parent.subject if parent.subject.lower().startswith("re:") else f"Re: {parent.subject}"
                    prefill_single_recipient = parent.sender_id if parent.sender_id != me.id else parent.recipient_id
                else:
                    prefill_mode = "forward"
                    prefill_subject = parent.subject if parent.subject.lower().startswith("fwd:") else f"Fwd: {parent.subject}"
                quote = parent.body or ""
                prefill_body = f"\n\n--- Original message ---\nFrom: {parent.sender.get_full_name() or parent.sender.username}\nSubject: {parent.subject}\n\n{quote}"
        except Message.DoesNotExist:
            pass

    return render(request, "messaging/messages.html", {
        "inbox_rows": inbox_rows,
        "sent_rows": sent_rows,
        "drafts": drafts,
        "unread_count": unread_count,
        "all_users": all_users,
        "all_users_for_mention": json.dumps(all_users_for_mention),
        "me_initials": me_initials,
        "message_data_json": json.dumps(message_data),
        "page_title": "Messages",
        "active_nav": "messages",
        "prefill_team": json.dumps(prefill_team) if prefill_team else "null",
        "prefill_recipient_ids": json.dumps(prefill_recipient_ids),
        "prefill_mode": prefill_mode or "",
        "prefill_subject": prefill_subject,
        "prefill_body": prefill_body,
        "prefill_single_recipient": prefill_single_recipient or "",
    })


@login_required
@require_POST
def send_message(request):
    recipient_id = request.POST.get("recipient_id")
    recipient_name = request.POST.get("recipient_name", "")
    subject = request.POST.get("subject", "").strip()
    body = request.POST.get("body", "").strip()
    is_group = request.POST.get("is_group") == "1"
    save_draft = request.POST.get("save_draft") == "1"
    files = request.FILES.getlist("attachments")
    if not save_draft:
        if not recipient_id and not (is_group and recipient_name):
            return JsonResponse({"error": "Please select at least one recipient"}, status=400)
        if not subject:
            return JsonResponse({"error": "Subject is required"}, status=400)
    if not body and not files:
        return JsonResponse({"error": "Message body or attachment required"}, status=400)
    if save_draft and not subject:
        subject = "(Draft)"
    recipient = None
    if recipient_id:
        try:
            recipient = User.objects.get(pk=recipient_id)
        except User.DoesNotExist:
            pass
    status = "draft" if save_draft else "sent"
    draft_id = request.POST.get("draft_id")
    sent_msg = None
    if draft_id:
        try:
            sent_msg = Message.objects.get(pk=draft_id, sender=request.user, status="draft")
            sent_msg.recipient = recipient
            sent_msg.recipient_team_name = recipient_name if is_group else ""
            sent_msg.subject = subject
            sent_msg.body = body
            sent_msg.is_group = is_group
            sent_msg.status = status
            sent_msg.is_read = False
            sent_msg.save()
        except Message.DoesNotExist:
            sent_msg = None
    if sent_msg is None:
        sent_msg = Message.objects.create(
            sender=request.user, recipient=recipient,
            recipient_team_name=recipient_name if is_group else "",
            subject=subject, body=body, is_group=is_group, status=status,
            is_read=False,
        )
    for f in files:
        Attachment.objects.create(message=sent_msg, file=f, original_name=f.name, size=f.size)
    return JsonResponse({"success": True, "status": status, "id": sent_msg.pk})


@login_required
def get_message_detail(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.recipient_id == request.user.id and not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=["is_read"])
    return JsonResponse({"success": True})


@login_required
@require_POST
def reply_message(request, pk):
    parent = get_object_or_404(Message, pk=pk)
    body = request.POST.get("body", "").strip()
    subject = request.POST.get("subject", parent.subject).strip() or parent.subject
    files = request.FILES.getlist("attachments")
    if not body and not files:
        return JsonResponse({"error": "Reply body or attachment required"}, status=400)
    other = parent.recipient if parent.sender_id == request.user.id else parent.sender
    if other is None:
        return JsonResponse({"error": "No recipient on this thread"}, status=400)

    sent_msg = Message.objects.create(
        sender=request.user, recipient=other, subject=subject, body=body, status="sent",
        is_read=False,
    )
    attachments_payload = []
    for f in files:
        att = Attachment.objects.create(message=sent_msg, file=f, original_name=f.name, size=f.size)
        attachments_payload.append({"name": f.name, "url": att.file.url, "size": f.size})

    return JsonResponse({"success": True, "attachments": attachments_payload})


@login_required
@require_POST
def delete_message(request, pk):
    msg = get_object_or_404(Message, pk=pk)
    if msg.sender_id == request.user.id or msg.recipient_id == request.user.id:
        msg.delete()
    return JsonResponse({"success": True})
