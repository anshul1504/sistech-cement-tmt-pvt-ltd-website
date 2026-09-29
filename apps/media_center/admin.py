from django.contrib import admin

from .models import BlogCategory, BlogPost, GalleryCategory, GalleryItem


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active", "item_count")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Media items")
    def item_count(self, obj):
        return obj.items.count()


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "media_type", "category", "event_date", "order", "is_featured", "is_active")
    list_filter = ("media_type", "category", "is_featured", "is_active", "event_date")
    list_editable = ("order", "is_featured", "is_active")
    search_fields = ("title", "caption", "location", "alt_text")
    list_select_related = ("category",)
    date_hierarchy = "created_at"
    fieldsets = (
        ("Media information", {"fields": ("title", "category", "media_type", "caption", "event_date", "location", "alt_text")}),
        ("Media source", {"description": "Complete only the field required by the selected media type.", "fields": ("image", "video", "youtube_url", "thumbnail")}),
        ("Publishing", {"fields": ("is_featured", "is_active", "order")}),
    )


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "published_at", "is_featured", "updated_at")
    list_filter = ("status", "is_featured", "category", "published_at")
    list_editable = ("status", "is_featured")
    search_fields = ("title", "excerpt", "content", "author_name")
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ("category",)
    date_hierarchy = "published_at"
    fieldsets = (
        ("Article", {"fields": ("title", "slug", "category", "author_name", "excerpt", "content")}),
        ("Featured image", {"fields": ("featured_image", "image_alt")}),
        ("Publishing", {"fields": ("status", "published_at", "is_featured")}),
        ("Search engine optimisation", {"fields": ("meta_title", "meta_description")}),
    )
