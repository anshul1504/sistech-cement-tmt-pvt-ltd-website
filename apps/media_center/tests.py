from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import BlogCategory, BlogPost, GalleryCategory, GalleryItem


class GalleryTests(TestCase):
    def setUp(self):
        self.category = GalleryCategory.objects.create(name="Dealer Events", slug="dealer-events")

    def test_gallery_lists_active_youtube_media_and_filters(self):
        GalleryItem.objects.create(title="Annual Dealer Meet", category=self.category, media_type="youtube", youtube_url="https://youtu.be/dQw4w9WgXcQ")
        response = self.client.get(reverse("media_center:gallery"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Annual Dealer Meet")
        self.assertContains(response, "data-filter=\"youtube\"")
        self.assertContains(response, "youtube-nocookie.com/embed/dQw4w9WgXcQ")

    def test_inactive_media_is_hidden(self):
        GalleryItem.objects.create(title="Private Event", category=self.category, media_type="youtube", youtube_url="https://youtu.be/dQw4w9WgXcQ", is_active=False)
        response = self.client.get(reverse("media_center:gallery"))
        self.assertNotContains(response, "Private Event")

    def test_media_type_source_is_validated(self):
        item = GalleryItem(title="Broken video", category=self.category, media_type="youtube", youtube_url="https://example.com/video")
        with self.assertRaises(ValidationError):
            item.full_clean()


class BlogTests(TestCase):
    def setUp(self):
        category = BlogCategory.objects.create(name="Construction", slug="construction")
        image = SimpleUploadedFile("cover.gif", b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;", content_type="image/gif")
        self.post = BlogPost.objects.create(title="Strong Construction Guide", slug="strong-construction-guide", category=category, excerpt="Practical construction guidance.", content="<p>Useful article content.</p>", featured_image=image, image_alt="Construction guide", status=BlogPost.PUBLISHED, is_featured=True)

    def test_blog_listing_and_detail_are_available(self):
        listing = self.client.get(reverse("blog:list"))
        detail = self.client.get(self.post.get_absolute_url())
        self.assertEqual(listing.status_code, 200)
        self.assertContains(listing, self.post.title)
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, "Useful article content")

    def test_draft_post_is_not_public(self):
        self.post.status = BlogPost.DRAFT
        self.post.save(update_fields=["status"])
        self.assertNotContains(self.client.get(reverse("blog:list")), self.post.title)
        self.assertEqual(self.client.get(self.post.get_absolute_url()).status_code, 404)

    def test_blog_category_filter(self):
        response = self.client.get(reverse("blog:list"), {"category": "construction"})
        self.assertContains(response, self.post.title)

    def test_blog_listing_is_paginated(self):
        category = self.post.category
        for index in range(10):
            BlogPost.objects.create(
                title=f"Construction Article {index}", slug=f"construction-article-{index}",
                category=category, excerpt="Article summary", content="<p>Article body</p>",
                featured_image=self.post.featured_image.name, image_alt="Construction article",
                status=BlogPost.PUBLISHED,
            )
        first_page = self.client.get(reverse("blog:list"))
        second_page = self.client.get(reverse("blog:list"), {"page": 2})
        self.assertEqual(first_page.context["page_obj"].paginator.per_page, 9)
        self.assertEqual(second_page.context["page_obj"].number, 2)
