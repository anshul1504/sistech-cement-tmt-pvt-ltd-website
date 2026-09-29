import re

from django.core.cache import cache
from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.urls import reverse

from apps.core.context_processors import site_and_theme
from apps.core.models import MenuItem, Page
from apps.core.templatetags.core_extras import menu_is_active

LINK_RE = re.compile(r'href="(/[a-z0-9\-/]*/)"')


class SeedDataMixin:
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        call_command("seed_demo")


class MenuContextProcessorTests(SeedDataMixin, TestCase):
    def test_inactive_children_excluded(self):
        parent = MenuItem.objects.filter(parent__isnull=True, label="Programs").first()
        self.assertIsNotNone(parent)
        child = parent.children.first()
        child.is_active = False
        child.save()
        cache.clear()

        request = RequestFactory().get("/")
        context = site_and_theme(request)
        programs = next(m for m in context["header_menu"] if m.label == "Programs")
        self.assertNotIn(child.pk, [c.pk for c in programs.active_children])

    def test_no_n_plus_one_queries(self):
        cache.clear()
        request = RequestFactory().get("/")
        with CaptureQueriesContext(connection) as ctx:
            site_and_theme(request)
        # two queries: parents, then a single batched prefetch for all children
        # (plus the two singleton loads and hero slides, all constant regardless of menu size)
        self.assertLessEqual(len(ctx.captured_queries), 6, ctx.captured_queries)

    def test_footer_columns_populated(self):
        # Column 3 is intentionally link-free: it holds only contact details
        # (rendered directly from SiteSettings in footer.html), not MenuItems.
        request = RequestFactory().get("/")
        context = site_and_theme(request)
        self.assertTrue(context["footer_columns"]["1"])
        self.assertTrue(context["footer_columns"]["2"])


class MenuIsActiveTagTests(SeedDataMixin, TestCase):
    def test_home_not_active_elsewhere(self):
        home = MenuItem.objects.get(label="Home")
        request = RequestFactory().get("/about/")
        context = {"request": request}
        self.assertFalse(menu_is_active(context, home))

    def test_home_active_on_home(self):
        home = MenuItem.objects.get(label="Home")
        request = RequestFactory().get("/")
        context = {"request": request}
        self.assertTrue(menu_is_active(context, home))

    def test_parent_active_when_child_active(self):
        parent = MenuItem.objects.get(label="About", parent__isnull=True)
        about_us_url = Page.objects.get(page_type="about").get_absolute_url()
        request = RequestFactory().get(about_us_url)
        context = {"request": request}
        self.assertTrue(menu_is_active(context, parent))


class SiteCrawlTests(SeedDataMixin, TestCase):
    """Crawls every header/footer link and asserts it resolves to a real page,
    and that all published navigation pages are reachable from the home page."""

    def test_every_page_reachable_and_returns_200(self):
        client = Client()
        home = client.get("/")
        self.assertEqual(home.status_code, 200)

        links = set(LINK_RE.findall(home.content.decode()))
        self.assertGreater(len(links), 5)

        for link in links:
            with self.subTest(link=link):
                resp = client.get(link)
                self.assertIn(resp.status_code, (200, 302), f"{link} returned {resp.status_code}")

        # FAQ is intentionally not present in the global navigation/top bar.
        expected_paths = {p.get_absolute_url() for p in Page.objects.filter(is_published=True)} - {"/", "/faq/"}
        self.assertTrue(expected_paths.issubset(links), expected_paths - links)

    def test_every_page_has_unique_search_metadata(self):
        pages = list(Page.objects.filter(is_published=True))
        titles = [page.meta_title for page in pages]
        self.assertTrue(all(titles))
        self.assertEqual(len(titles), len(set(titles)))
        self.assertTrue(all(len(title) <= 70 for title in titles))
        self.assertTrue(all(80 <= len(page.meta_description) <= 170 for page in pages))


class QualityAssurancePageTests(SeedDataMixin, TestCase):
    def test_dedicated_quality_page_renders_complete_system(self):
        response = self.client.get(reverse("core:quality_assurance"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/quality_assurance.html")
        self.assertContains(response, "How We Approach Quality")
        self.assertContains(response, "From Source to Site")
        self.assertContains(response, "Reliable Packaging & Dispatch")


class SafetySustainabilityPageTests(SeedDataMixin, TestCase):
    def test_dedicated_safety_page_renders_complete_framework(self):
        response = self.client.get(reverse("core:safety_sustainability"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/safety_sustainability.html")
        self.assertContains(response, "Our Safety &amp; Sustainability Framework", html=True)
        self.assertContains(response, "Practical Controls Across Operations")
        self.assertContains(response, "A Simple Improvement Cycle")


class CorporateResponsibilityPageTests(SeedDataMixin, TestCase):
    def test_dedicated_csr_page_renders_complete_framework(self):
        response = self.client.get(reverse("core:csr"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/csr.html")
        self.assertContains(response, "Where We Aim to Make a Difference")
        self.assertContains(response, "Knowledge Creates Lasting Impact")
        self.assertContains(response, "Responsibility Through Relationships")


class RewardsRecognitionPageTests(SeedDataMixin, TestCase):
    def test_dedicated_rewards_page_uses_brochure_programme_content(self):
        response = self.client.get(reverse("core:rewards_recognition"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/rewards_recognition.html")
        self.assertContains(response, "Star Dealer")
        self.assertContains(response, "International Couple Tour")
        self.assertContains(response, "Special appreciation from SISTECH management")


class StarMasonContractorSchemePageTests(SeedDataMixin, TestCase):
    def test_dedicated_scheme_page_uses_brochure_content(self):
        response = self.client.get(reverse("core:star_mason_contractor_scheme"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/star_mason_contractor_scheme.html")
        self.assertContains(response, "Registered Mason or Contractor")
        self.assertContains(response, "Domestic Couple Trip")
        self.assertContains(response, "Annual Champion Awards")


class StarEngineerProgramPageTests(SeedDataMixin, TestCase):
    def test_dedicated_engineer_page_uses_brochure_content(self):
        response = self.client.get(reverse("core:star_engineer_program"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/star_engineer_program.html")
        self.assertContains(response, "Registered Engineers")
        self.assertContains(response, "International Couple Trip")
        self.assertContains(response, "Annual Awards Ceremony")


class StarDealerProgramPageTests(SeedDataMixin, TestCase):
    def test_dedicated_dealer_program_uses_brochure_content(self):
        response = self.client.get(reverse("core:star_dealer_program"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/star_dealer_program.html")
        self.assertContains(response, "Registered SISTECH Dealers")
        self.assertContains(response, "Domestic Couple Trip")
        self.assertContains(response, "Grand Champion Award")


class ManufacturingPartnersPageTests(SeedDataMixin, TestCase):
    def test_dedicated_manufacturing_page_uses_brochure_network(self):
        response = self.client.get(reverse("core:manufacturing_partners"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/manufacturing_partners.html")
        self.assertContains(response, "Abhiraj Cement")
        self.assertContains(response, "Pioneer Industries")
        self.assertContains(response, "300,000 TPA")


class ProductsPageTests(SeedDataMixin, TestCase):
    def test_dedicated_products_page_uses_brochure_portfolio(self):
        response = self.client.get(reverse("core:products"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/products.html")
        self.assertContains(response, "Ordinary Portland Cement")
        self.assertContains(response, "Portland Pozzolana Cement")
        self.assertContains(response, "Uniform Rib Design")
        self.assertContains(response, "How to Identify Quality TMT Bars")
        self.assertContains(response, "Certification &amp; Traceability", html=True)
        self.assertContains(response, "SISTECH TMT 550D")
