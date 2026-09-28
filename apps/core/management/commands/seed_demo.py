from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.core.models import (
    HeroSlide,
    MenuItem,
    Page,
    PageSection,
    SectionFeatureCard,
    SectionStep,
    SectionTimelineItem,
    SiteSettings,
    ThemeSettings,
)

SAMPLE_TAG = "[SAMPLE CONTENT — replace before launch]"

PAGES = [
    ("Home", "home", "home"),
    ("About Us", "about", "about"),
    ("Board of Directors / Leadership", "leadership", "leadership"),
    ("Products", "products", "products"),
    ("Manufacturing Partners", "manufacturing-partners", "manufacturing_partners"),
    ("Distribution Network", "distribution-network", "distribution_network"),
    ("Star Dealer Program", "star-dealer-program", "star_dealer_program"),
    ("Star Engineer Program", "star-engineer-program", "star_engineer_program"),
    ("Star Mason & Contractor Scheme", "star-mason-contractor-scheme", "star_mason_contractor_scheme"),
    ("Rewards & Recognition", "rewards-recognition", "rewards_recognition"),
    ("Quality Assurance", "quality-assurance", "quality_assurance"),
    ("Safety & Sustainability", "safety-sustainability", "safety_sustainability"),
    ("Corporate Responsibility (CSR)", "csr", "csr"),
    ("Future Expansion / Roadmap", "roadmap", "roadmap"),
    ("Gallery", "gallery", "gallery"),
    ("Careers", "careers", "careers"),
    ("Blog / News", "blog", "blog"),
    ("FAQ", "faq", "faq"),
    ("Contact Us", "contact", "contact"),
    ("Privacy Policy & Terms", "privacy-terms", "privacy_terms"),
]

# Top-level header structure: max 7 items + 1 CTA button.
# Each top-level entry is (label, page_type_or_None, footer_column, children)
# children: list of (label, page_type, description, footer_column)
HEADER_MENU = [
    ("Home", "home", "none", []),
    ("About", None, "none", [
        ("About Us", "about", "Our story, mission and values.", "1"),
        ("Board of Directors / Leadership", "leadership", "Meet the leadership team.", "1"),
        ("Future Expansion / Roadmap", "roadmap", "Our growth strategy.", "1"),
    ]),
    ("Products", "products", "2", []),
    ("Network", None, "none", [
        ("Manufacturing Partners", "manufacturing_partners", "Our cement & TMT manufacturing tie-ups.", "2"),
        ("Distribution Network", "distribution_network", "Dealers and distributors across India.", "2"),
    ]),
    ("Programs", None, "none", [
        ("Star Dealer Program", "star_dealer_program", "Rewards for top-performing dealers.", "2"),
        ("Star Engineer Program", "star_engineer_program", "Recognition for engineers.", "none"),
        ("Star Mason & Contractor Scheme", "star_mason_contractor_scheme", "Rewards for masons & contractors.", "none"),
        ("Rewards & Recognition", "rewards_recognition", "Annual awards program.", "none"),
    ]),
    ("Responsibility", None, "none", [
        ("Quality Assurance", "quality_assurance", "Our quality commitment.", "3"),
        ("Safety & Sustainability", "safety_sustainability", "Building responsibly.", "none"),
        ("Corporate Responsibility (CSR)", "csr", "Our commitment beyond business.", "1"),
    ]),
    ("Media", None, "none", [
        ("Gallery", "gallery", "Photos and videos.", "3"),
        ("Blog / News", "blog", "Latest updates from SISTECH.", "none"),
    ]),
    ("Careers", "careers", "3", []),
    ("Contact Us", "contact", "3", []),
]

# Footer-only links (not in header nav): assigned straight to a footer column.
# Privacy Policy & Terms lives only in the bottom legal bar (footer.html), not in
# this column list too, to avoid showing the same link twice.
FOOTER_ONLY_LINKS = [
    ("FAQ", "faq", "3"),
    ("Privacy Policy & Terms", "privacy_terms", "none"),
]

HERO_SUBTITLE = {
    "about": "SISTECH Cement & TMT Pvt. Ltd. is an Indian construction materials company committed to providing high-quality cement and TMT steel products through strategic manufacturing partnerships and a strong distribution network.",
    "leadership": "The Board is committed to transparent governance, ethical business practices, sustainable growth, and delivering long-term value to customers, partners, and stakeholders.",
    "products": "OPC, PPC and PSC cement, and high-strength TMT bars, built for residential, commercial, industrial and infrastructure projects.",
    "manufacturing_partners": "Strategic manufacturing partnerships enable SISTECH to maintain a dependable supply chain, consistent product availability, and reliable service across multiple regions.",
    "distribution_network": "SISTECH Cement & TMT Pvt. Ltd. is continuously strengthening its distribution network to ensure timely availability of products across key markets.",
    "star_dealer_program": "Grow Together. Win Together. SISTECH recognizes and rewards its dealer partners for their outstanding contribution to business growth.",
    "star_engineer_program": "Engineering Excellence Deserves Recognition. SISTECH appreciates engineers who contribute to the successful use of quality construction materials.",
    "star_mason_contractor_scheme": "Building Excellence Together. Masons and Contractors are the backbone of every successful construction project.",
    "rewards_recognition": "Celebrating Excellence — every year, SISTECH organizes a special recognition program to honour its highest-performing business partners.",
    "quality_assurance": "At SISTECH, quality is the foundation of every product we supply.",
    "safety_sustainability": "SISTECH encourages responsible business practices throughout its operations.",
    "csr": "We believe that business growth should create value for society.",
    "roadmap": "SISTECH Cement & TMT Pvt. Ltd. is committed to sustainable growth through strategic expansion, stronger partnerships, and customer-focused operations.",
    "contact": "Let's Build Together.",
    "privacy_terms": "",
}

BOARD_MEMBERS = [
    ("Ajay Kumar Ratnakar", "Managing Director"),
    ("Pooja Singh Gaharwar", "Director"),
    ("Aditya Paswan", "Director"),
    ("B K Namdev", "Director"),
]

CORE_VALUES = [
    "Quality First", "Customer Satisfaction", "Integrity & Transparency", "Strong Partnerships",
    "Innovation", "Timely Delivery", "Safety", "Sustainable Growth",
]

WHY_CHOOSE_SISTECH = [
    ("Premium Quality Products", "Consistent, quality-checked cement and TMT bars."),
    ("Reliable Manufacturing Partners", "A network of established cement and TMT manufacturing partners."),
    ("Strong Distribution Network", "A growing dealer network across Madhya Pradesh, Uttar Pradesh, Chhattisgarh and Bihar."),
    ("Timely Delivery", "Planned logistics and dispatch to keep projects on schedule."),
    ("Customer-Centric Service", "Dedicated support for dealers, engineers, masons and contractors."),
    ("Experienced Leadership", "A board committed to transparent governance and long-term partnerships."),
]

CEMENT_RANGE = [
    ("OPC Cement", "Ordinary Portland Cement."),
    ("PPC Cement", "Portland Pozzolana Cement."),
    ("PSC Cement", "Portland Slag Cement."),
]

TMT_FEATURES = [
    ("High Strength TMT Bars", ""),
    ("Earthquake Resistant", ""),
    ("Corrosion Resistant", ""),
    ("Superior Weldability", ""),
    ("Uniform Rib Design", ""),
]

APPLICATIONS = ["Residential Buildings", "Commercial Projects", "Industrial Construction", "Roads & Bridges", "Government Infrastructure"]

MANUFACTURING_PARTNERS = [
    ("Abhiraj Cement", "Simga, Raipur (Chhattisgarh) — Capacity 2.5 MTPA, Clinker Type PPC/OPC, Modern Dry Process."),
    ("Central Cement Industries", "Simga, Raipur (Chhattisgarh) — Capacity 2.0 MTPA, Clinker Type PPC/OPC, Modern Dry Process."),
    ("Rajat Cement", "Sardarpur, Dhar (Madhya Pradesh) — Capacity 0.72 MTPA, Clinker Type PPC/OPC, Modern Dry Process."),
    ("Himalaya Height Cement", "Kaimur, Bhabhua (Bihar) — Capacity 5.4 MTPA, Clinker Type PPC/OPC, Modern Dry Process."),
    ("Pioneer Industries", "Ghursal, Jeerabad, Dhar (Madhya Pradesh) — Capacity 3.24 MTPA, Clinker Type PPC/OPC, Modern Dry Process."),
    ("SISTECH TMT — Raigarh Ispat", "Raigarh (Chhattisgarh) — Capacity 300,000 TPA, TMT Bars, Induction Based."),
]

FOCUS_STATES = [
    ("Madhya Pradesh", ""), ("Uttar Pradesh", ""), ("Chhattisgarh", ""), ("Bihar", ""),
]

DISTRIBUTION_HIGHLIGHTS = [
    ("Well-planned dealer network", ""), ("Efficient dispatch system", ""),
    ("Timely product availability", ""), ("Dedicated sales support", ""), ("Expansion into new districts", ""),
]

STAR_DEALER_ELIGIBILITY = ["Registered SISTECH Dealers", "Performance during the annual scheme period", "Compliance with company policies"]
STAR_DEALER_REWARDS = [
    ("District Level", "Domestic Couple Trip"), ("State Level", "International Couple Trip"),
    ("National Level", "Grand Champion Award, Trophy & Certificate"),
]
STAR_DEALER_BENEFITS = [
    ("Recognition", "Recognition as a Star Dealer"), ("Premium Travel", "Premium travel experiences"),
    ("Business Networking", "Business networking opportunities"), ("Annual Appreciation", "Annual appreciation by the company"),
]

STAR_ENGINEER_ELIGIBILITY = ["Registered Engineers associated with SISTECH", "Annual performance and project engagement", "Compliance with company guidelines"]
STAR_ENGINEER_REWARDS = [
    ("Domestic Couple Trip", ""), ("International Couple Trip", ""),
    ("Trophy & Certificate", ""), ("Recognition at the Annual Awards Ceremony", ""),
]

STAR_MASON_ELIGIBILITY = ["Registered Masons & Contractors", "Annual performance", "Consistent use of SISTECH products", "Compliance with company policies"]
STAR_MASON_RECOGNITION = [
    ("Domestic Couple Trip", ""), ("International Couple Trip", ""),
    ("Annual Champion Awards", ""), ("Trophy & Certificate of Excellence", ""),
]

AWARD_CATEGORIES = [("Star Dealer", ""), ("Star Engineer", ""), ("Star Mason", ""), ("Star Contractor", "")]
GRAND_RECOGNITION = ["International Couple Tour", "Luxury Accommodation", "Award Ceremony", "Trophy & Certificate", "Special Recognition by the Management"]

QUALITY_FOCUS = [
    "Consistent product quality through manufacturing partners", "Raw material quality monitoring",
    "Compliance with applicable quality standards", "Reliable packaging and dispatch", "Customer feedback-driven improvement",
]

SAFETY_FOCUS = [
    ("Product quality and consistency", "Delivering high-quality cement and TMT products you can rely on."),
    ("Responsible sourcing through manufacturing partners", "Partnering with reliable manufacturers who share our values."),
    ("Efficient transportation and logistics", "Timely delivery through well-planned transportation and logistics."),
    ("Safe handling and storage practices", "Ensuring safe unloading, handling and storage at every stage."),
    ("Continuous improvement in business processes", "Adopting better methods every day for a stronger tomorrow."),
]

CSR_FOCUS = [
    ("Promoting safe construction practices", "We support awareness and adoption of safe and standard construction methods."),
    ("Supporting skill development for masons and contractors", "We encourage training and upskilling to build a stronger, more skilled workforce."),
    ("Encouraging ethical business practices", "We believe in honesty, transparency and fair business conduct in everything we do."),
    ("Building long-term relationships with channel partners", "We grow together by creating trust, respect and mutual success."),
    ("Contributing to community development initiatives where possible", "We care for communities and contribute towards building a better and stronger tomorrow."),
]

SEED_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "seed_assets"

ROADMAP_PHASES = [
    ("Phase 1", "Strengthen Operations", "Strengthening operations in Madhya Pradesh, Uttar Pradesh, Chhattisgarh and Bihar."),
    ("Phase 2", "Expand into Additional States", "Increasing dealer and distributor presence; enhancing technical support for engineers and contractors."),
    ("Phase 3", "Build a Strong National Network", "Building a strong national distribution network, expanding the product portfolio, and strengthening long-term strategic partnerships."),
]


def build_menu(page_by_type):
    """Builds the 7-top-level-item + CTA header menu, shared by seed_demo and reset_menu."""
    for order, (label, page_type, footer_col, children) in enumerate(HEADER_MENU):
        page = page_by_type.get(page_type) if page_type else None
        item = MenuItem.objects.create(
            label=label, page=page, order=order, show_in_header=True,
            show_in_footer=False, footer_column=footer_col,
        )
        for child_order, (child_label, child_type, description, child_footer_col) in enumerate(children):
            MenuItem.objects.create(
                label=child_label, page=page_by_type.get(child_type), parent=item,
                order=child_order, description=description,
                show_in_header=True, show_in_footer=False, footer_column=child_footer_col,
            )

    for order, (label, page_type, footer_col) in enumerate(FOOTER_ONLY_LINKS):
        MenuItem.objects.create(
            label=label, page=page_by_type.get(page_type), order=100 + order,
            show_in_header=False, show_in_footer=True, footer_column=footer_col,
        )

    MenuItem.objects.create(
        label="Join as Dealer", url="/distribution-network/", order=99,
        is_button=True, show_in_header=True, show_in_footer=False,
    )


class Command(BaseCommand):
    help = "Seeds all 20 pages, default menu, theme and real SISTECH corporate content so every page renders on first run."

    def handle(self, *args, **options):
        ThemeSettings.load()
        self._seed_site_settings()

        page_by_type = {}
        for title, slug, page_type in PAGES:
            page, created = Page.objects.get_or_create(
                page_type=page_type,
                defaults=dict(
                    title=title,
                    slug=slug or "home",
                    hero_title=title if page_type != "home" else "",
                    hero_subtitle=HERO_SUBTITLE.get(page_type, ""),
                    meta_title=title,
                    meta_description=(HERO_SUBTITLE.get(page_type) or title)[:170],
                ),
            )
            page_by_type[page_type] = page
            if created:
                self.stdout.write(f"Created page: {title}")

            if not page.sections.exists():
                self._seed_sections(page_type, page)

        self._seed_hero_slides()
        self._seed_menu(page_by_type)

        self.stdout.write(self.style.SUCCESS("seed_demo complete: 20 pages ready with real SISTECH content."))

    # -- helpers -----------------------------------------------------

    def _seed_site_settings(self):
        site = SiteSettings.load()
        if site.address:
            return
        site.legal_name = "SISTECH Cement & TMT Private Limited"
        site.address = "Ho. No. 186/C, Scheme No. 134, Near Advance Academy, Indore, Madhya Pradesh"
        site.phone_primary = "8319416402"
        site.whatsapp_number = "918319416402"
        site.email_contact = "sistechcement@gmail.com"
        site.gst_number = "23ABICS4693M1ZQ"
        site.cin_number = "U26940MP2022PTC060788"
        site.footer_about = "SISTECH Cement & TMT Pvt. Ltd. — Solid Foundation, Strong Future. An Indian construction materials company delivering quality cement and TMT bars through trusted manufacturing partnerships and a strong distribution network."
        site.copyright_text = "© SISTECH Cement & TMT Pvt. Ltd. All rights reserved."

        asset_map = {
            "logo_header.png": ("logo_header", "sistech-logo-header.png"),
            "logo_header_compact.png": ("logo_header_compact", "sistech-logo-header-compact.png"),
            "logo_footer.png": ("logo_footer", "sistech-logo-footer.png"),
            "favicon.png": ("favicon", "sistech-favicon.png"),
            "apple_touch_icon.png": ("apple_touch_icon", "sistech-apple-touch-icon.png"),
        }
        for filename, (field_name, save_as) in asset_map.items():
            src = SEED_ASSETS_DIR / filename
            if src.exists():
                with open(src, "rb") as f:
                    getattr(site, field_name).save(save_as, File(f), save=False)

        site.save()
        self.stdout.write("Seeded Site Settings with real company details and logo assets.")

    def _add_feature_cards(self, page, heading, items, subheading="", background="white", order=0):
        section = PageSection.objects.create(
            page=page, section_type="feature_cards", order=order,
            heading=heading, subheading=subheading, background_style=background,
        )
        for i, (title, text) in enumerate(items):
            SectionFeatureCard.objects.create(section=section, title=title, text=text, order=i)
        return section

    def _add_steps(self, page, heading, items, background="alt", order=0):
        section = PageSection.objects.create(page=page, section_type="steps", order=order, heading=heading, background_style=background)
        for i, title in enumerate(items):
            SectionStep.objects.create(section=section, title=title, order=i)
        return section

    def _add_richtext(self, page, heading, html, background="white", order=0):
        return PageSection.objects.create(
            page=page, section_type="richtext", order=order, heading=heading,
            richtext_body=html, background_style=background,
        )

    def _add_testimonial(self, page, quote, author, role, order=0):
        return PageSection.objects.create(
            page=page, section_type="testimonial", order=order,
            testimonial_quote=quote, testimonial_author=author, testimonial_role=role, background_style="navy",
        )

    def _add_timeline(self, page, heading, items, order=0):
        section = PageSection.objects.create(page=page, section_type="timeline", order=order, heading=heading)
        for i, (label, title, text) in enumerate(items):
            SectionTimelineItem.objects.create(section=section, year_or_label=label, title=title, text=text, order=i)
        return section

    def _seed_sections(self, page_type, page):
        if page_type == "home":
            self._add_feature_cards(page, "Why Choose SISTECH", WHY_CHOOSE_SISTECH, order=0)
            self._add_richtext(
                page, "Who We Are",
                "<p>SISTECH Cement & TMT Private Limited is an Indian construction materials company "
                "committed to providing high-quality cement and TMT steel products through strategic "
                "manufacturing partnerships and a strong distribution network. The company serves "
                "infrastructure, residential, commercial and industrial construction projects with a "
                "focus on quality, reliability and timely supply.</p>",
                background="alt", order=1,
            )
        elif page_type == "about":
            self._add_richtext(
                page, "Who We Are",
                "<p>SISTECH Cement & TMT Private Limited is an Indian construction materials company "
                "committed to providing high-quality cement and TMT steel products through strategic "
                "manufacturing partnerships and a strong distribution network.</p>"
                "<p>The company serves infrastructure, residential, commercial, and industrial construction "
                "projects with a focus on quality, reliability, and timely supply.</p>"
                "<p>Through its network of manufacturing partners and distributors, SISTECH aims to deliver "
                "products that meet customer expectations while supporting sustainable business growth.</p>",
                order=0,
            )
            self._add_richtext(
                page, "Our Mission",
                "<p>To deliver quality cement and TMT products through trusted manufacturing partnerships, "
                "an efficient distribution network, and customer-focused service.</p>",
                background="alt", order=1,
            )
            self._add_richtext(
                page, "Our Vision",
                "<p>To become one of India's most trusted construction material companies by building "
                "long-term relationships with customers, dealers, contractors, engineers, and manufacturing "
                "partners.</p>",
                order=2,
            )
            self._add_feature_cards(page, "Core Values", [(v, "") for v in CORE_VALUES], background="alt", order=3)
            self._add_testimonial(
                page,
                "At SISTECH Cement & TMT Pvt. Ltd., we believe that every strong structure begins with "
                "quality materials and trusted relationships. Our goal is to create a reliable supply "
                "network, maintain consistent product quality through our manufacturing partners, and "
                "build long-term partnerships with our dealers, engineers, contractors, and customers. "
                "We are committed to expanding across India while maintaining the highest standards of "
                "integrity, service, and customer satisfaction.",
                "Ajay Kumar Ratnakar", "Managing Director", order=4,
            )
        elif page_type == "leadership":
            self._add_feature_cards(page, "Leadership Team", [(n, d) for n, d in BOARD_MEMBERS], order=0)
            self._add_richtext(
                page, "Leadership Philosophy",
                "<p>The Board is committed to transparent governance, ethical business practices, "
                "sustainable growth, and delivering long-term value to customers, partners, and "
                "stakeholders.</p>",
                background="alt", order=1,
            )
        elif page_type == "products":
            self._add_feature_cards(page, "SISTECH Cement Range", CEMENT_RANGE, order=0)
            self._add_feature_cards(page, "SISTECH TMT Bars", TMT_FEATURES, background="alt", order=1)
            self._add_feature_cards(page, "Applications", [(a, "") for a in APPLICATIONS], order=2)
        elif page_type == "manufacturing_partners":
            self._add_feature_cards(page, "Manufacturing Tie-Up Network", MANUFACTURING_PARTNERS, order=0)
            self._add_richtext(
                page, "Our Strength",
                "<p>Strategic manufacturing partnerships enable SISTECH to maintain a dependable supply "
                "chain, consistent product availability, and reliable service across multiple regions.</p>",
                background="navy", order=1,
            )
        elif page_type == "distribution_network":
            self._add_feature_cards(page, "Current Focus States", FOCUS_STATES, order=0)
            self._add_feature_cards(page, "Distribution Highlights", DISTRIBUTION_HIGHLIGHTS, background="alt", order=1)
            self._add_richtext(
                page, "Vision",
                "<p>To build one of the most reliable construction material distribution networks in "
                "India.</p>",
                order=2,
            )
        elif page_type == "star_dealer_program":
            self._add_steps(page, "Eligibility", STAR_DEALER_ELIGIBILITY, order=0)
            self._add_feature_cards(page, "Rewards", STAR_DEALER_REWARDS, background="alt", order=1)
            self._add_feature_cards(page, "Benefits", STAR_DEALER_BENEFITS, order=2)
        elif page_type == "star_engineer_program":
            self._add_steps(page, "Eligibility", STAR_ENGINEER_ELIGIBILITY, order=0)
            self._add_feature_cards(page, "Rewards", STAR_ENGINEER_REWARDS, background="alt", order=1)
        elif page_type == "star_mason_contractor_scheme":
            self._add_steps(page, "Eligibility", STAR_MASON_ELIGIBILITY, order=0)
            self._add_feature_cards(page, "Recognition", STAR_MASON_RECOGNITION, background="alt", order=1)
        elif page_type == "rewards_recognition":
            self._add_feature_cards(page, "Award Categories", AWARD_CATEGORIES, order=0)
            self._add_steps(page, "Grand Recognition", GRAND_RECOGNITION, order=1)
        elif page_type == "quality_assurance":
            self._add_steps(page, "Quality Focus", QUALITY_FOCUS, order=0)
            self._add_testimonial(
                page,
                "Every bag of cement and every TMT bar supplied through SISTECH reflects our commitment "
                "to reliability and customer satisfaction.",
                "SISTECH Cement & TMT Pvt. Ltd.", "Our Promise", order=1,
            )
        elif page_type == "safety_sustainability":
            self._add_feature_cards(page, "Our Focus", SAFETY_FOCUS, order=0)
            self._add_richtext(
                page, "Commitment",
                "<p>To grow responsibly while maintaining customer trust and business integrity.</p>",
                background="navy", order=1,
            )
        elif page_type == "csr":
            self._add_feature_cards(page, "Focus Areas", CSR_FOCUS, order=0)
            self._add_richtext(
                page, "A Better Tomorrow, Together",
                "<p>Stronger Business. Stronger Society. We believe that business growth should create "
                "value for society.</p>",
                background="navy", order=1,
            )
        elif page_type == "roadmap":
            self._add_timeline(page, "Business Roadmap — Growth Strategy", ROADMAP_PHASES, order=0)
        elif page_type == "contact":
            self._add_richtext(
                page, "Get in Touch",
                "<p>We respond to your inquiries promptly, with expert support and a dedicated team "
                "building long-term relationships through trust and transparency.</p>",
                order=0,
            )
        else:
            # gallery, careers, blog, faq, privacy_terms: dedicated apps/templates land in later phases
            PageSection.objects.create(
                page=page, section_type="richtext", order=0, heading=page.title,
                richtext_body=f"<p>{SAMPLE_TAG} Content for the {page.title} page will appear here once its "
                f"dedicated app is built. Edit this section in Django admin under Pages &rarr; {page.title} "
                f"&rarr; Sections.</p>",
            )

    def _seed_hero_slides(self):
        if HeroSlide.objects.exists():
            return
        HeroSlide.objects.create(
            heading="Building Strength. Delivering Trust.",
            subheading="SISTECH Cement & TMT Pvt. Ltd. — Solid Foundation, Strong Future. Indore, Madhya Pradesh.",
            cta_1_label="Explore Our Products",
            cta_1_url="/products/",
            cta_2_label="Join as Dealer",
            cta_2_url="/distribution-network/",
            order=0,
        )
        self.stdout.write("Created hero slide (add a background image in admin).")

    def _seed_menu(self, page_by_type):
        if MenuItem.objects.exists():
            return
        build_menu(page_by_type)
        self.stdout.write("Created default menu (7 top-level items + CTA).")
