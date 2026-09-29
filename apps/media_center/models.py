from pathlib import Path
from urllib.parse import parse_qs, urlparse

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django_ckeditor_5.fields import CKEditor5Field


def validate_media_size(file):
    if file and file.size > 80 * 1024 * 1024:
        raise ValidationError("Uploaded video must be 80 MB or smaller.")


class GalleryCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")
        verbose_name_plural = "Gallery categories"

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    IMAGE = "image"
    VIDEO = "video"
    YOUTUBE = "youtube"
    MEDIA_TYPES = ((IMAGE, "Image"), (VIDEO, "Uploaded video"), (YOUTUBE, "YouTube video"))

    title = models.CharField(max_length=150)
    category = models.ForeignKey(GalleryCategory, on_delete=models.PROTECT, related_name="items")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, default=IMAGE)
    image = models.ImageField(upload_to="gallery/images/", blank=True)
    video = models.FileField(upload_to="gallery/videos/", blank=True, validators=[FileExtensionValidator(["mp4", "webm", "ogg"]), validate_media_size], help_text="MP4, WebM or OGG; maximum 80 MB.")
    youtube_url = models.URLField(blank=True, help_text="Paste a YouTube video or Shorts URL.")
    thumbnail = models.ImageField(upload_to="gallery/thumbnails/", blank=True, help_text="Recommended for uploaded videos. YouTube thumbnails load automatically.")
    caption = models.TextField(blank=True, max_length=500)
    event_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=120, blank=True)
    alt_text = models.CharField(max_length=180, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("order", "-event_date", "-created_at")

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        errors = {}
        if self.media_type == self.IMAGE and not self.image:
            errors["image"] = "Select an image for an image gallery item."
        if self.media_type == self.VIDEO and not self.video:
            errors["video"] = "Upload a video file for an uploaded-video item."
        if self.media_type == self.YOUTUBE:
            if not self.youtube_url:
                errors["youtube_url"] = "Enter a YouTube URL."
            elif not self.youtube_id:
                errors["youtube_url"] = "Enter a valid youtube.com or youtu.be video URL."
        if errors:
            raise ValidationError(errors)

    @property
    def youtube_id(self):
        if not self.youtube_url:
            return ""
        parsed = urlparse(self.youtube_url)
        host = parsed.netloc.lower().removeprefix("www.")
        if host == "youtu.be":
            return parsed.path.strip("/").split("/")[0]
        if host in {"youtube.com", "m.youtube.com"}:
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [""])[0]
            parts = parsed.path.strip("/").split("/")
            if len(parts) > 1 and parts[0] in {"embed", "shorts", "live"}:
                return parts[1]
        return ""

    @property
    def youtube_embed_url(self):
        return f"https://www.youtube-nocookie.com/embed/{self.youtube_id}" if self.youtube_id else ""

    @property
    def youtube_thumbnail_url(self):
        return f"https://i.ytimg.com/vi/{self.youtube_id}/hqdefault.jpg" if self.youtube_id else ""

    @property
    def display_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        if self.media_type == self.IMAGE and self.image:
            return self.image.url
        return self.youtube_thumbnail_url

    @property
    def media_url(self):
        if self.media_type == self.IMAGE and self.image:
            return self.image.url
        if self.media_type == self.VIDEO and self.video:
            return self.video.url
        return self.youtube_embed_url

    @property
    def file_name(self):
        field = self.image if self.media_type == self.IMAGE else self.video
        return Path(field.name).name if field else ""


class BlogCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("order", "name")
        verbose_name_plural = "Blog categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    DRAFT = "draft"
    PUBLISHED = "published"
    STATUS_CHOICES = ((DRAFT, "Draft"), (PUBLISHED, "Published"))

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.PROTECT, related_name="posts")
    author_name = models.CharField(max_length=100, default="SISTECH Editorial Team")
    excerpt = models.TextField(max_length=360)
    content = CKEditor5Field(config_name="default")
    featured_image = models.ImageField(upload_to="blog/posts/")
    image_alt = models.CharField(max_length=180)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=DRAFT)
    is_featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(default=timezone.now)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=170, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def reading_time(self):
        words = len(strip_tags(self.content).split())
        return max(1, round(words / 200))
