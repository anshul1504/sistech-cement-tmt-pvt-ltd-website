from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field


class SingletonModel(models.Model):
    """Base for models that must only ever have one row (pk=1)."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        self.clear_cache()

    def delete(self, *args, **kwargs):
        pass  # singleton rows are never deleted through the admin

    def clear_cache(self):
        cache.delete(self.cache_key())

    @classmethod
    def cache_key(cls):
        return f"singleton:{cls.__name__}"

    @classmethod
    def load(cls):
        cached = cache.get(cls.cache_key())
        if cached is not None:
            return cached
        obj, _ = cls.objects.get_or_create(pk=1)
        cache.set(cls.cache_key(), obj, 300)
        return obj


FONT_CHOICES = [
    ("system", "System default"),
    ("poppins", "Poppins"),
    ("montserrat", "Montserrat"),
    ("roboto", "Roboto"),
    ("inter", "Inter"),
    ("open_sans", "Open Sans"),
    ("barlow", "Barlow"),
]

RADIUS_CHOICES = [
    ("sharp", "Sharp"),
    ("soft", "Soft"),
    ("round", "Round"),
]

BUTTON_STYLE_CHOICES = [
    ("solid", "Solid"),
    ("outline", "Outline"),
    ("pill", "Pill"),
]


class ThemeSettings(SingletonModel):
    color_primary = models.CharField(max_length=7, default="#14337F")
    color_primary_dark = models.CharField(max_length=7, default="#0C2259")
    color_accent = models.CharField(max_length=7, default="#F2B705")
    color_text = models.CharField(max_length=7, default="#1F2937")
    color_muted = models.CharField(max_length=7, default="#6B7280")
    color_background = models.CharField(max_length=7, default="#FFFFFF")
    color_alt_background = models.CharField(max_length=7, default="#F5F7FA")
    color_border = models.CharField(max_length=7, default="#E5E7EB")
    color_header_bg = models.CharField(max_length=7, default="#FFFFFF")
    color_footer_bg = models.CharField(max_length=7, default="#0C2259")

    heading_font = models.CharField(max_length=20, choices=FONT_CHOICES, default="poppins")
    body_font = models.CharField(max_length=20, choices=FONT_CHOICES, default="poppins")
    base_font_size = models.PositiveIntegerField(default=16, help_text="Base font size in pixels.")
    border_radius = models.CharField(max_length=10, choices=RADIUS_CHOICES, default="soft")
    container_width = models.PositiveIntegerField(default=1200, help_text="Max content width in pixels.")
    button_style = models.CharField(max_length=10, choices=BUTTON_STYLE_CHOICES, default="solid")

    sticky_header = models.BooleanField(default=True)
    top_bar_enabled = models.BooleanField(default=True)
    whatsapp_button_enabled = models.BooleanField(default=True)
    back_to_top_enabled = models.BooleanField(default=True)
    scroll_animations_enabled = models.BooleanField(default=True)
    dark_footer = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Theme Settings"
        verbose_name_plural = "Theme Settings"

    def __str__(self):
        return "Theme Settings"


class SiteSettings(SingletonModel):
    company_name = models.CharField(max_length=200, default="SISTECH Cement & TMT Pvt. Ltd.")
    legal_name = models.CharField(max_length=200, blank=True)
    tagline = models.CharField(max_length=200, default="Solid Foundation, Strong Future.")

    logo_header = models.ImageField(upload_to="site/", blank=True, null=True)
    logo_header_compact = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="Logo without the tagline line, used when the header is scrolled/collapsed and on mobile.",
    )
    logo_footer = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(upload_to="site/", blank=True, null=True)
    apple_touch_icon = models.ImageField(upload_to="site/", blank=True, null=True)
    default_share_image = models.ImageField(upload_to="site/", blank=True, null=True)

    phone_primary = models.CharField(max_length=20, blank=True)
    phone_secondary = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text="With country code, digits only, e.g. 919876543210")
    whatsapp_message = models.CharField(max_length=300, blank=True, default="Hello, I would like to know more about SISTECH products.")

    email_contact = models.EmailField(blank=True)
    email_career = models.EmailField(blank=True)
    email_support = models.EmailField(blank=True)

    address = models.TextField(blank=True)
    map_lat = models.DecimalField(max_digits=9, decimal_places=6, default=22.7196)
    map_lng = models.DecimalField(max_digits=9, decimal_places=6, default=75.8577)
    map_zoom = models.PositiveIntegerField(default=14)
    business_hours = models.CharField(max_length=200, blank=True)

    gst_number = models.CharField(max_length=20, blank=True)
    cin_number = models.CharField(max_length=30, blank=True)

    footer_col1_title = models.CharField(max_length=50, blank=True, default="Company")
    footer_col2_title = models.CharField(max_length=50, blank=True, default="Products & Programs")
    footer_col3_title = models.CharField(max_length=50, blank=True, default="Contact")
    credit_text = models.CharField(max_length=100, blank=True, default="Designed & Developed by The Webfix")
    credit_url = models.URLField(blank=True, default="https://thewebfix.in")

    social_facebook = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_youtube = models.URLField(blank=True)
    social_x = models.URLField(blank=True)
    social_indiamart = models.URLField(blank=True)

    footer_about = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True, default="© SISTECH Cement & TMT Pvt. Ltd. All rights reserved.")

    ga_id = models.CharField(max_length=30, blank=True, verbose_name="Google Analytics ID")
    head_scripts = models.TextField(blank=True, help_text="Staff-only. Raw HTML/JS injected before </head>.")
    footer_scripts = models.TextField(blank=True, help_text="Staff-only. Raw HTML/JS injected before </body>.")

    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(
        blank=True, default="We're performing scheduled maintenance. Please check back soon."
    )
    robots_txt = models.TextField(
        blank=True,
        default="User-agent: *\nAllow: /\n",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"


class HeroSlide(models.Model):
    heading = models.CharField(max_length=200)
    subheading = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="hero_slides/")
    cta_1_label = models.CharField(max_length=50, blank=True)
    cta_1_url = models.CharField(max_length=300, blank=True)
    cta_2_label = models.CharField(max_length=50, blank=True)
    cta_2_url = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Hero Slide"

    def __str__(self):
        return self.heading


class MenuItem(models.Model):
    label = models.CharField(max_length=100)
    url = models.CharField(max_length=300, blank=True, help_text="Used if no page is linked below.")
    page = models.ForeignKey("core.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="menu_items")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    description = models.CharField(
        max_length=150, blank=True, help_text="Optional short text shown under this link inside a dropdown panel."
    )
    order = models.PositiveIntegerField(default=0)
    new_tab = models.BooleanField(default=False)
    show_in_header = models.BooleanField(default=True)
    show_in_footer = models.BooleanField(default=False)
    footer_column = models.CharField(
        max_length=10,
        choices=[("none", "Not in footer"), ("1", "Footer column 1"), ("2", "Footer column 2"), ("3", "Footer column 3")],
        default="none",
        help_text="Which footer column this link appears in (independent of 'show in footer').",
    )
    is_active = models.BooleanField(default=True)
    is_button = models.BooleanField(default=False, help_text="Highlight this item as a button, e.g. Become a Dealer.")

    class Meta:
        ordering = ["order"]
        verbose_name = "Menu Item"

    def __str__(self):
        return self.label

    def get_url(self):
        if self.page_id:
            return self.page.get_absolute_url()
        return self.url or "#"


PAGE_TYPE_CHOICES = [
    ("home", "Home"),
    ("about", "About Us"),
    ("leadership", "Board of Directors / Leadership"),
    ("products", "Products"),
    ("manufacturing_partners", "Manufacturing Partners"),
    ("distribution_network", "Distribution Network"),
    ("star_dealer_program", "Star Dealer Program"),
    ("star_engineer_program", "Star Engineer Program"),
    ("star_mason_contractor_scheme", "Star Mason & Contractor Scheme"),
    ("rewards_recognition", "Rewards & Recognition"),
    ("quality_assurance", "Quality Assurance"),
    ("safety_sustainability", "Safety & Sustainability"),
    ("csr", "Corporate Responsibility (CSR)"),
    ("roadmap", "Future Expansion / Roadmap"),
    ("gallery", "Gallery"),
    ("careers", "Careers"),
    ("blog", "Blog / News"),
    ("faq", "FAQ"),
    ("contact", "Contact Us"),
    ("privacy_terms", "Privacy Policy & Terms"),
]

PAGE_SLUG_MAP = {
    "home": "",
    "about": "about",
    "leadership": "leadership",
    "products": "products",
    "manufacturing_partners": "manufacturing-partners",
    "distribution_network": "distribution-network",
    "star_dealer_program": "star-dealer-program",
    "star_engineer_program": "star-engineer-program",
    "star_mason_contractor_scheme": "star-mason-contractor-scheme",
    "rewards_recognition": "rewards-recognition",
    "quality_assurance": "quality-assurance",
    "safety_sustainability": "safety-sustainability",
    "csr": "csr",
    "roadmap": "roadmap",
    "gallery": "gallery",
    "careers": "careers",
    "blog": "blog",
    "faq": "faq",
    "contact": "contact",
    "privacy_terms": "privacy-terms",
}


class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    page_type = models.CharField(max_length=40, choices=PAGE_TYPE_CHOICES, unique=True)
    is_published = models.BooleanField(default=True)

    hero_title = models.CharField(max_length=200, blank=True)
    hero_subtitle = models.CharField(max_length=300, blank=True)
    hero_bg_image = models.ImageField(upload_to="page_heroes/", blank=True, null=True)
    hero_overlay_opacity = models.PositiveIntegerField(default=50, help_text="0-100")
    hero_cta_label = models.CharField(max_length=50, blank=True)
    hero_cta_url = models.CharField(max_length=300, blank=True)
    hero_cta_2_label = models.CharField(max_length=50, blank=True)
    hero_cta_2_url = models.CharField(max_length=300, blank=True)

    show_breadcrumb = models.BooleanField(default=True)

    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=170, blank=True)
    share_image = models.ImageField(upload_to="page_shares/", blank=True, null=True)
    noindex = models.BooleanField(default=False)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        slug = PAGE_SLUG_MAP.get(self.page_type, self.slug)
        if slug == "":
            return reverse("core:home")
        return f"/{slug}/"


SECTION_TYPE_CHOICES = [
    ("richtext", "Rich text"),
    ("image_text", "Image + text"),
    ("feature_cards", "Feature cards"),
    ("stats", "Stats / counters"),
    ("timeline", "Timeline"),
    ("steps", "Steps / process"),
    ("faq_accordion", "FAQ accordion"),
    ("gallery_strip", "Gallery strip"),
    ("cta_band", "CTA band"),
    ("testimonial", "Testimonial / quote"),
    ("downloads", "Downloads list"),
    ("map_embed", "Embedded map"),
    ("custom_html", "Custom HTML (staff-only)"),
]

BACKGROUND_STYLE_CHOICES = [
    ("white", "White"),
    ("alt", "Alt background"),
    ("navy", "Navy"),
    ("gold", "Gold"),
    ("image", "Image"),
]

ALIGNMENT_CHOICES = [("left", "Left"), ("center", "Center"), ("right", "Right")]
PADDING_CHOICES = [("sm", "Small"), ("md", "Medium"), ("lg", "Large")]


class PageSection(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="sections")
    section_type = models.CharField(max_length=30, choices=SECTION_TYPE_CHOICES)
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    heading = models.CharField(max_length=200, blank=True)
    subheading = models.CharField(max_length=300, blank=True)
    background_style = models.CharField(max_length=10, choices=BACKGROUND_STYLE_CHOICES, default="white")
    background_image = models.ImageField(upload_to="section_backgrounds/", blank=True, null=True)
    alignment = models.CharField(max_length=10, choices=ALIGNMENT_CHOICES, default="left")
    padding_size = models.CharField(max_length=5, choices=PADDING_CHOICES, default="md")

    richtext_body = CKEditor5Field(blank=True, config_name="default")

    image_text_image = models.ImageField(upload_to="section_images/", blank=True, null=True)
    image_text_position = models.CharField(
        max_length=5, choices=[("left", "Image left"), ("right", "Image right")], default="left"
    )
    image_text_body = CKEditor5Field(blank=True, config_name="default")

    cta_band_button_label = models.CharField(max_length=50, blank=True)
    cta_band_button_url = models.CharField(max_length=300, blank=True)

    testimonial_quote = models.TextField(blank=True)
    testimonial_author = models.CharField(max_length=150, blank=True)
    testimonial_role = models.CharField(max_length=150, blank=True)

    map_embed_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_embed_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    map_embed_zoom = models.PositiveIntegerField(default=14)

    custom_html = models.TextField(blank=True, help_text="Staff-only. Rendered unescaped.")

    class Meta:
        ordering = ["order"]
        verbose_name = "Page Section"

    def __str__(self):
        return f"{self.page.title} — {self.get_section_type_display()}"


class SectionFeatureCard(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="feature_cards")
    icon = models.CharField(max_length=50, blank=True, help_text="Icon keyword/class name.")
    title = models.CharField(max_length=150)
    text = models.TextField(blank=True)
    link = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class SectionStat(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="stats")
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=30)
    suffix = models.CharField(max_length=10, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class SectionTimelineItem(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="timeline_items")
    year_or_label = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class SectionStep(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="steps")
    title = models.CharField(max_length=200)
    text = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class SectionFAQLink(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="faq_links")
    faq_item = models.ForeignKey("faq.FAQItem", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class SectionGalleryImage(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="section_gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]


class SectionDownload(models.Model):
    section = models.ForeignKey(PageSection, on_delete=models.CASCADE, related_name="downloads")
    label = models.CharField(max_length=200)
    file = models.FileField(upload_to="section_downloads/")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
