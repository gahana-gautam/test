from django.db import migrations

ALLOWED_DOMAIN = "broadcast.com"


def deactivate_non_broadcast(apps, schema_editor):
    User = apps.get_model("auth", "User")
    for u in User.objects.filter(is_superuser=False):
        if not (u.email or "").lower().endswith("@" + ALLOWED_DOMAIN):
            if u.is_active:
                u.is_active = False
                u.save(update_fields=["is_active"])


def reactivate(apps, schema_editor):
    User = apps.get_model("auth", "User")
    User.objects.filter(is_active=False).update(is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_userprofile_avatar_userprofile_phone"),
    ]

    operations = [
        migrations.RunPython(deactivate_non_broadcast, reactivate),
    ]
