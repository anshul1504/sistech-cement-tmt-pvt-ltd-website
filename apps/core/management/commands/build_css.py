import re

from django.conf import settings
from django.core.management.base import BaseCommand


def minify(css: str) -> str:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,])\s*", r"\1", css)
    css = re.sub(r";}", "}", css)
    return css.strip()


class Command(BaseCommand):
    help = (
        "Concatenates and minifies the CSS layers listed in static/css/manifest.txt into "
        "static/dist/main.css (pure Python, no Node). base.html reads the same manifest for dev mode."
    )

    def handle(self, *args, **options):
        static_dir = settings.BASE_DIR / "static"
        manifest_path = static_dir / "css" / "manifest.txt"
        dist_path = static_dir / "dist" / "main.css"
        dist_path.parent.mkdir(parents=True, exist_ok=True)

        layers = [
            line.strip() for line in manifest_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

        chunks = []
        for relative_path in layers:
            file_path = static_dir / relative_path
            if not file_path.exists():
                self.stderr.write(self.style.WARNING(f"Missing CSS layer: {relative_path}"))
                continue
            chunks.append(file_path.read_text(encoding="utf-8"))

        combined = "\n".join(chunks)
        dist_path.write_text(minify(combined), encoding="utf-8")

        self.stdout.write(self.style.SUCCESS(f"Built {dist_path} ({len(layers)} layers from manifest.txt)."))
