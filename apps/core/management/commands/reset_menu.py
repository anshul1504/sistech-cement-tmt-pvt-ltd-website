from django.core.management.base import BaseCommand, CommandError

from apps.core.management.commands.seed_demo import build_menu
from apps.core.models import MenuItem, Page


class Command(BaseCommand):
    help = "Rebuilds the header/footer menu to the current 7-top-level + CTA structure, replacing whatever exists."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes", action="store_true",
            help="Required to confirm: this deletes all existing MenuItem rows and rebuilds them.",
        )

    def handle(self, *args, **options):
        if not options["yes"]:
            raise CommandError(
                "This will delete all existing menu items and rebuild the default structure. "
                "Re-run with --yes to confirm."
            )
        page_by_type = {p.page_type: p for p in Page.objects.all()}
        MenuItem.objects.all().delete()
        build_menu(page_by_type)
        self.stdout.write(self.style.SUCCESS("Menu rebuilt to the default 7-top-level + CTA structure."))
