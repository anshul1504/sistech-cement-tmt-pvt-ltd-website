from django.urls import path

from apps.core import views
from apps.enquiries.views import contact
from apps.network.views import dealer_application

app_name = "core"

# Pages rendered through the generic Page/PageSection builder until a
# dedicated app/view/template replaces them (Products, Network, Careers, etc.
# get their own apps in a later phase; the slug stays the same when that happens).
GENERIC_PAGES = [
    ("faq/", "faq", "faq"),
]

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("leadership/", views.leadership, name="leadership"),
    path("roadmap/", views.roadmap, name="roadmap"),
    path("contact/", contact, name="contact"),
    path("contact/thank-you/", contact, {"submitted": True}, name="contact_success"),
    path("distribution-network/", dealer_application, name="distribution_network"),
    path("distribution-network/thank-you/", dealer_application, {"submitted": True}, name="dealer_success"),
    path("quality-assurance/", views.quality_assurance, name="quality_assurance"),
    path("safety-sustainability/", views.safety_sustainability, name="safety_sustainability"),
    path("csr/", views.corporate_responsibility, name="csr"),
    path("rewards-recognition/", views.rewards_recognition, name="rewards_recognition"),
    path("star-mason-contractor-scheme/", views.star_mason_contractor_scheme, name="star_mason_contractor_scheme"),
    path("star-engineer-program/", views.star_engineer_program, name="star_engineer_program"),
    path("star-dealer-program/", views.star_dealer_program, name="star_dealer_program"),
    path("manufacturing-partners/", views.manufacturing_partners, name="manufacturing_partners"),
    path("products/", views.products, name="products"),
    path("privacy-terms/", views.privacy_terms, name="privacy_terms"),
] + [
    path(slug, views.GenericPageView.as_view(page_type=page_type), name=name)
    for slug, page_type, name in GENERIC_PAGES
]
