from django.core.management.base import BaseCommand

from apps.core.models import ThemeSettings


class Command(BaseCommand):
    help = "Resets ThemeSettings to their default values."

    def handle(self, *args, **options):
        theme = ThemeSettings.load()
        for field in ThemeSettings._meta.fields:
            if field.name == "id":
                continue
            if field.default is not None:
                setattr(theme, field.name, field.default)
        theme.save()
        self.stdout.write(self.style.SUCCESS("Theme reset to defaults."))
