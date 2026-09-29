from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

FONT_STACKS = {
    "system": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    "poppins": "'Poppins', sans-serif",
    "montserrat": "'Montserrat', sans-serif",
    "roboto": "'Roboto', sans-serif",
    "inter": "'Inter', sans-serif",
    "open_sans": "'Open Sans', sans-serif",
    "barlow": "'Barlow', sans-serif",
}

RADIUS_VALUES = {
    "sharp": "0px",
    "soft": "8px",
    "round": "16px",
}


@register.filter
def font_stack(value):
    return mark_safe(FONT_STACKS.get(value, FONT_STACKS["system"]))


@register.filter
def radius_value(value):
    return RADIUS_VALUES.get(value, RADIUS_VALUES["soft"])


@register.filter
def india_phone(value):
    """Display Indian phone numbers consistently with the +91 country code."""
    raw = str(value or "").strip()
    digits = "".join(character for character in raw if character.isdigit())
    if len(digits) == 10:
        return f"+91 {digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+91 {digits[2:]}"
    return raw


@register.simple_tag
def render_section(section):
    """Returns the template path for a given PageSection type."""
    return f"sections/{section.section_type}.html"


@register.simple_tag(takes_context=True)
def menu_is_active(context, item):
    """True if the current request path matches this item's URL (or, for a
    parent, if any of its children match). Never marks '/' active for other pages."""
    request = context.get("request")
    if request is None:
        return False
    path = request.path

    def matches(url):
        if not url or url == "#":
            return False
        if url == "/":
            return path == "/"
        return path == url or path.startswith(url)

    if matches(item.get_url()):
        return True
    children = getattr(item, "active_children", None)
    if children is None:
        children = item.children.filter(is_active=True)
    for child in children:
        if matches(child.get_url()):
            return True
    return False


@register.simple_tag
def css_manifest():
    """Reads static/css/manifest.txt so base.html and build_css.py share one ordered list."""
    manifest_path = settings.BASE_DIR / "static" / "css" / "manifest.txt"
    return [
        line.strip() for line in manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


@register.simple_tag
def icon(name, css_class=""):
    attrs = f' class="icon {css_class}"'.rstrip() if css_class else ' class="icon"'
    return mark_safe(
        f'<svg{attrs} aria-hidden="true" focusable="false"><use href="#icon-{name}"></use></svg>'
    )
