from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch

from apps.core.models import HeroSlide, MenuItem, SiteSettings, ThemeSettings

MENU_CACHE_KEY = "menu_items_all_v2"

# Bump this whenever CSS/JS changes ship, so browsers can't serve a stale
# cached header/footer from before the update (Django's dev server doesn't
# set strong cache-busting headers on its own).
STATIC_ASSET_VERSION = "20260928-14"


def _load_menu_items():
    children_qs = (
        MenuItem.objects.filter(is_active=True)
        .select_related("page")
        .order_by("order")
    )
    parents_qs = (
        MenuItem.objects.filter(is_active=True, parent__isnull=True)
        .select_related("page")
        .prefetch_related(Prefetch("children", queryset=children_qs, to_attr="active_children"))
        .order_by("order")
    )
    return list(parents_qs)


def site_and_theme(request):
    site = SiteSettings.load()
    theme = ThemeSettings.load()

    menu_items = cache.get(MENU_CACHE_KEY)
    if menu_items is None:
        menu_items = _load_menu_items()
        cache.set(MENU_CACHE_KEY, menu_items, 300)

    header_menu = [m for m in menu_items if m.show_in_header]

    footer_columns = {"1": [], "2": [], "3": []}
    for m in menu_items:
        if m.footer_column in footer_columns:
            footer_columns[m.footer_column].append(m)
        for c in m.active_children:
            if c.footer_column in footer_columns:
                footer_columns[c.footer_column].append(c)

    hero_slides = HeroSlide.objects.filter(is_active=True).order_by("order")[:5]

    return {
        "site": site,
        "theme": theme,
        "header_menu": header_menu,
        "footer_columns": footer_columns,
        "hero_slides": hero_slides,
        "use_built_css": settings.USE_BUILT_CSS,
        "asset_v": STATIC_ASSET_VERSION,
    }
