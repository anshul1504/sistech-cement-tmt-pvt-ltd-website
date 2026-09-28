import re

from django.core.cache import cache
from django.core.management import call_command
from django.test import Client, RequestFactory, TestCase
from django.test.utils import CaptureQueriesContext
from django.db import connection

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
    and that all 20 published pages are reachable from header or footer."""

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

        expected_paths = {p.get_absolute_url() for p in Page.objects.filter(is_published=True)} - {"/"}
        self.assertTrue(expected_paths.issubset(links), expected_paths - links)
