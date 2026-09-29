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
        from apps.media_center.models import BlogPost
        context["latest_posts"] = BlogPost.objects.filter(status=BlogPost.PUBLISHED).select_related("category")[:3]
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


def quality_assurance(request):
    return render(request, "pages/quality_assurance.html", {
        "page": get_page_or_none("quality_assurance"),
        "has_cta_section": True,
    })


def safety_sustainability(request):
    return render(request, "pages/safety_sustainability.html", {
        "page": get_page_or_none("safety_sustainability"),
        "has_cta_section": True,
    })


def corporate_responsibility(request):
    return render(request, "pages/csr.html", {
        "page": get_page_or_none("csr"),
        "has_cta_section": True,
    })


def privacy_terms(request):
    return render(request, "pages/privacy_terms.html", {
        "page": get_page_or_none("privacy_terms"),
        "has_cta_section": True,
    })


def rewards_recognition(request):
    return render(request, "pages/rewards_recognition.html", {
        "page": get_page_or_none("rewards_recognition"),
        "has_cta_section": True,
    })


def star_mason_contractor_scheme(request):
    return render(request, "pages/star_mason_contractor_scheme.html", {
        "page": get_page_or_none("star_mason_contractor_scheme"),
        "has_cta_section": True,
    })


def star_engineer_program(request):
    return render(request, "pages/star_engineer_program.html", {
        "page": get_page_or_none("star_engineer_program"),
        "has_cta_section": True,
    })


def star_dealer_program(request):
    return render(request, "pages/star_dealer_program.html", {
        "page": get_page_or_none("star_dealer_program"),
        "has_cta_section": True,
    })


def manufacturing_partners(request):
    return render(request, "pages/manufacturing_partners.html", {
        "page": get_page_or_none("manufacturing_partners"),
        "has_cta_section": True,
    })


def products(request):
    return render(request, "pages/products.html", {
        "page": get_page_or_none("products"),
        "has_cta_section": True,
    })


def about(request):
    return render(request, "pages/about.html", {
        "page": get_page_or_none("about"),
        "has_cta_section": True,
    })


def leadership(request):
    return render(request, "pages/leadership.html", {
        "page": get_page_or_none("leadership"),
        "has_cta_section": True,
    })


def roadmap(request):
    return render(request, "pages/roadmap.html", {
        "page": get_page_or_none("roadmap"),
        "has_cta_section": True,
    })
