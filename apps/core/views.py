from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from apps.core.models import Page


def get_page_or_none(page_type):
    return Page.objects.filter(page_type=page_type, is_published=True).first()


class HomeView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = get_page_or_none("home")
        context["page"] = page
        context["has_cta_section"] = bool(
            page and page.sections.filter(is_visible=True, section_type="cta_band").exists()
        )
        return context


class GenericPageView(TemplateView):
    """Renders any Page by its page_type through the section builder."""

    template_name = "pages/generic_page.html"
    page_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = get_page_or_none(self.page_type)
        context["page"] = page
        if page:
            sections = list(
                page.sections.filter(is_visible=True).prefetch_related(
                    "feature_cards", "stats", "timeline_items", "steps",
                    "faq_links__faq_item", "gallery_images", "downloads",
                )
            )
        else:
            sections = []
        context["sections"] = sections
        context["has_cta_section"] = any(s.section_type == "cta_band" for s in sections)
        return context


def robots_txt(request):
    from apps.core.models import SiteSettings

    site = SiteSettings.load()
    return HttpResponse(site.robots_txt or "User-agent: *\nAllow: /\n", content_type="text/plain")
