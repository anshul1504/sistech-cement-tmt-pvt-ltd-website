from django.urls import path

from apps.core import views

app_name = "core"

# Pages rendered through the generic Page/PageSection builder until a
# dedicated app/view/template replaces them (Products, Network, Careers, etc.
# get their own apps in a later phase; the slug stays the same when that happens).
GENERIC_PAGES = [
    ("about/", "about", "about"),
    ("leadership/", "leadership", "leadership"),
    ("products/", "products", "products"),
    ("manufacturing-partners/", "manufacturing_partners", "manufacturing_partners"),
    ("distribution-network/", "distribution_network", "distribution_network"),
    ("star-dealer-program/", "star_dealer_program", "star_dealer_program"),
    ("star-engineer-program/", "star_engineer_program", "star_engineer_program"),
    ("star-mason-contractor-scheme/", "star_mason_contractor_scheme", "star_mason_contractor_scheme"),
    ("rewards-recognition/", "rewards_recognition", "rewards_recognition"),
    ("quality-assurance/", "quality_assurance", "quality_assurance"),
    ("safety-sustainability/", "safety_sustainability", "safety_sustainability"),
    ("csr/", "csr", "csr"),
    ("roadmap/", "roadmap", "roadmap"),
    ("gallery/", "gallery", "gallery"),
    ("careers/", "careers", "careers"),
    ("blog/", "blog", "blog"),
    ("faq/", "faq", "faq"),
    ("contact/", "contact", "contact"),
    ("privacy-terms/", "privacy_terms", "privacy_terms"),
]

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
] + [
    path(slug, views.GenericPageView.as_view(page_type=page_type), name=name)
    for slug, page_type, name in GENERIC_PAGES
]
