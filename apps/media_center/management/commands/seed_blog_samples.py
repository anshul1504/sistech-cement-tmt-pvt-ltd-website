from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.media_center.models import BlogCategory, BlogPost


POSTS = [
    {
        "category": ("TMT & Engineering", "tmt-engineering", 1), "title": "How to Choose Quality TMT Bars for Safer Construction", "slug": "how-to-choose-quality-tmt-bars",
        "image": "tmt-quality-guide.png", "alt": "Engineer checking TMT bar quality at an Indian construction site", "featured": True,
        "excerpt": "A practical guide to understanding TMT grades, strength, ductility, bend performance and the checks that support safer reinforced-concrete construction.",
        "meta": "Learn how to evaluate TMT steel grades, strength, ductility, certification and on-site quality for safer reinforced-concrete construction.",
        "content": """<p>TMT reinforcement is one of the most important structural inputs in reinforced-concrete construction. The right bar must provide strength, ductility and dependable bonding with concrete—not simply look heavy or rigid.</p><h2>Start with the structural design</h2><p>Bar diameter, spacing and grade should follow drawings prepared by a qualified structural engineer. Substituting a grade or diameter without approval can change how a structural member performs under load.</p><h2>Check grade and traceability</h2><p>Confirm the specified grade, manufacturer identification and batch documentation. A reliable supply partner should be able to provide invoices and relevant quality certificates for traceability.</p><h2>Strength must work with ductility</h2><p>High yield strength is valuable, but a good TMT bar must also deform safely before failure. Ductility is especially important where structures may face dynamic or seismic forces.</p><blockquote>Quality steel is not selected by appearance alone; specification, certification and correct placement must work together.</blockquote><h2>Inspect material at delivery</h2><ul><li>Verify diameter, quantity and grade against the purchase order.</li><li>Look for excessive rust, oil, paint or surface contamination.</li><li>Store bars above ground and separate different diameters clearly.</li><li>Do not accept visibly damaged, deeply pitted or mixed unidentified material.</li></ul><h2>Protect quality during fabrication</h2><p>Correct cutting, bending, lap length, cover blocks and bar spacing are as important as the steel itself. Use approved bar-bending schedules and avoid uncontrolled heating during bending.</p><h2>A coordinated approach</h2><p>Builders, engineers, fabricators and suppliers should review specifications before dispatch and again before concreting. This simple coordination reduces mistakes and supports a stronger, more dependable structure.</p>""",
    },
    {
        "category": ("Cement & Concrete", "cement-concrete", 2), "title": "Building a Strong Foundation: Cement and Concrete Essentials", "slug": "cement-concrete-essentials-strong-foundation",
        "image": "cement-foundation-guide.png", "alt": "Concrete being poured for a modern residential foundation in India", "featured": False,
        "excerpt": "From cement selection and water control to placement and curing, understand the essentials that influence concrete strength and foundation durability.",
        "meta": "Understand cement selection, concrete proportioning, water control, compaction and curing for strong, durable building foundations.",
        "content": """<p>A foundation transfers the building load safely to the ground. Its performance depends on sound design, suitable materials and disciplined execution at every stage of concreting.</p><h2>Use the specified cement and mix</h2><p>Cement type and concrete grade must match the engineer’s specification. Avoid changing mix proportions at site without technical approval, because small adjustments can affect strength, workability and durability.</p><h2>Control the water-cement ratio</h2><p>Adding excess water may make concrete easier to place, but it can increase porosity and reduce final strength. Measure water carefully and account for moisture already present in aggregates.</p><h2>Prepare before the pour</h2><ul><li>Confirm excavation level, formwork and reinforcement.</li><li>Remove standing water, loose soil and debris.</li><li>Check cover blocks and service openings.</li><li>Plan access, labour, equipment and uninterrupted material supply.</li></ul><h2>Place and compact correctly</h2><p>Concrete should be placed near its final position and compacted systematically to remove trapped air. Improper vibration can cause honeycombing, while excessive vibration may lead to segregation.</p><blockquote>A strong mix still requires correct placement and curing to achieve its intended performance.</blockquote><h2>Curing is not optional</h2><p>Concrete needs adequate moisture for cement hydration. Begin curing at the appropriate time and maintain it for the specified duration, protecting fresh concrete from rapid drying, vibration and early loading.</p><h2>Document quality</h2><p>Maintain pour records, material details and test results. Good documentation enables the project team to identify issues early and creates accountability throughout construction.</p>""",
    },
    {
        "category": ("Dealer Growth", "dealer-growth", 3), "title": "Five Practices That Help Building-Material Dealers Grow", "slug": "building-material-dealer-growth-practices",
        "image": "dealer-growth-guide.png", "alt": "Indian building-material dealer planning inventory with a sales professional", "featured": False,
        "excerpt": "Practical ways for cement and TMT dealers to improve inventory planning, contractor relationships, service quality and sustainable market growth.",
        "meta": "Explore five practical strategies for cement and TMT dealers to improve inventory, customer service, contractor relationships and growth.",
        "content": """<p>Building-material retail is a relationship-driven business, but consistent growth also depends on inventory discipline, market knowledge and dependable customer service.</p><h2>1. Plan inventory around local demand</h2><p>Review fast-moving grades, pack types, seasonal construction cycles and active project categories. A focused inventory plan improves availability without locking unnecessary capital in slow-moving stock.</p><h2>2. Build a reliable fulfilment process</h2><p>Give customers clear commitments on stock, delivery timing and documentation. Coordinate dispatch early for large orders and maintain accurate order records to reduce last-minute confusion.</p><h2>3. Support contractors and engineers</h2><p>Product information, technical sessions and responsive issue handling help professionals make informed choices. Long-term loyalty is earned through useful support, not only price negotiation.</p><h2>4. Use simple digital tools</h2><ul><li>Track enquiries and follow-ups.</li><li>Maintain customer and project records.</li><li>Monitor stock ageing and reorder points.</li><li>Share verified product information through approved channels.</li></ul><blockquote>The strongest dealer relationships combine product availability, transparent communication and dependable after-sales support.</blockquote><h2>5. Protect trust in every transaction</h2><p>Purchase through authorised channels, maintain proper invoices and store materials correctly. Transparent practices protect the dealer, customer and brand while supporting sustainable growth.</p><h2>Grow through partnership</h2><p>A manufacturer-dealer relationship works best when both sides exchange market feedback, plan demand and resolve service issues quickly. Consistent collaboration creates better outcomes across the distribution network.</p>""",
    },
]


class Command(BaseCommand):
    help = "Create or update professional sample blog articles and their generated cover images."

    def handle(self, *args, **options):
        source_dir = Path(settings.BASE_DIR) / "static" / "images" / "blog" / "posts"
        for data in POSTS:
            category_name, category_slug, category_order = data["category"]
            category, _ = BlogCategory.objects.update_or_create(slug=category_slug, defaults={"name": category_name, "order": category_order, "is_active": True})
            post, _ = BlogPost.objects.update_or_create(slug=data["slug"], defaults={"title": data["title"], "category": category, "excerpt": data["excerpt"], "content": data["content"], "image_alt": data["alt"], "status": BlogPost.PUBLISHED, "is_featured": data["featured"], "meta_title": data["title"][:70], "meta_description": data["meta"][:170]})
            source = source_dir / data["image"]
            if source.exists() and (not post.featured_image or Path(post.featured_image.name).name != data["image"]):
                with source.open("rb") as handle:
                    post.featured_image.save(data["image"], File(handle), save=True)
        self.stdout.write(self.style.SUCCESS(f"Published {len(POSTS)} sample blog articles."))
