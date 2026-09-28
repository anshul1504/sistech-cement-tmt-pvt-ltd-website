from django.db import migrations

# Only "core" and "faq" have real models as of Phase 2. A follow-up data migration
# in Phase 3 re-syncs these groups' permissions once the remaining apps have models.
CONTENT_EDITOR_APPS = ["core", "products", "network", "programs", "company", "media_center", "careers", "faq"]


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    content_editor, _ = Group.objects.get_or_create(name="Content Editor")
    admin_group, _ = Group.objects.get_or_create(name="Admin")

    all_perms = Permission.objects.all()
    admin_group.permissions.set(all_perms)

    content_perms = Permission.objects.filter(content_type__app_label__in=CONTENT_EDITOR_APPS).exclude(
        content_type__app_label="core", content_type__model__in=["themesettings"]
    )
    content_editor.permissions.set(content_perms)


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Content Editor", "Admin"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("faq", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
