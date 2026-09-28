from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from apps.core.models import (
    HeroSlide,
    MenuItem,
    Page,
    PageSection,
    SectionDownload,
    SectionFAQLink,
    SectionFeatureCard,
    SectionGalleryImage,
    SectionStat,
    SectionStep,
    SectionTimelineItem,
    SiteSettings,
    ThemeSettings,
)


class NoAddDeleteSingletonAdmin(admin.ModelAdmin):
    """Prevents adding a second row or deleting the only row of a singleton."""

    def has_add_permission(self, request):
        return self.model.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ThemeSettings)
class ThemeSettingsAdmin(NoAddDeleteSingletonAdmin):
    fieldsets = (
        ("Colors", {"fields": (
            "color_primary", "color_primary_dark", "color_accent", "color_text", "color_muted",
            "color_background", "color_alt_background", "color_border", "color_header_bg", "color_footer_bg",
        )}),
        ("Typography & layout", {"fields": (
            "heading_font", "body_font", "base_font_size", "border_radius", "container_width", "button_style",
        )}),
        ("Toggles", {"fields": (
            "sticky_header", "top_bar_enabled", "whatsapp_button_enabled", "back_to_top_enabled",
            "scroll_animations_enabled", "dark_footer",
        )}),
    )
    actions = ["reset_to_default"]

    @admin.action(description="Reset to default theme")
    def reset_to_default(self, request, queryset):
        for obj in queryset:
            for field in ThemeSettings._meta.fields:
                if field.name == "id":
                    continue
                setattr(obj, field.name, field.default)
            obj.save()
        self.message_user(request, "Theme reset to defaults.")


@admin.register(SiteSettings)
class SiteSettingsAdmin(NoAddDeleteSingletonAdmin):
    fieldsets = (
        ("Company", {"fields": ("company_name", "legal_name", "tagline")}),
        ("Branding", {"fields": ("logo_header", "logo_footer", "favicon", "default_share_image")}),
        ("Contact", {"fields": (
            "phone_primary", "phone_secondary", "whatsapp_number", "whatsapp_message",
            "email_contact", "email_career", "email_support",
        )}),
        ("Location", {"fields": ("address", "map_lat", "map_lng", "map_zoom", "business_hours")}),
        ("Legal", {"fields": ("gst_number", "cin_number")}),
        ("Social", {"fields": (
            "social_facebook", "social_instagram", "social_linkedin", "social_youtube", "social_x", "social_indiamart",
        )}),
        ("Footer", {"fields": ("footer_about", "copyright_text")}),
        ("Tracking & scripts (staff only)", {"fields": ("ga_id", "head_scripts", "footer_scripts")}),
        ("Maintenance & SEO", {"fields": ("maintenance_mode", "maintenance_message", "robots_txt")}),
    )


@admin.register(HeroSlide)
class HeroSlideAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("heading", "is_active", "order", "thumb")
    list_editable = ()
    search_fields = ("heading",)

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px;" />', obj.image.url)
        return "-"


@admin.register(MenuItem)
class MenuItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("label", "parent", "show_in_header", "show_in_footer", "is_active", "order")
    list_filter = ("show_in_header", "show_in_footer", "is_active")
    search_fields = ("label",)


class SectionFeatureCardInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionFeatureCard
    extra = 1


class SectionStatInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionStat
    extra = 1


class SectionTimelineItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionTimelineItem
    extra = 1


class SectionStepInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionStep
    extra = 1


class SectionFAQLinkInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionFAQLink
    extra = 1


class SectionGalleryImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionGalleryImage
    extra = 1


class SectionDownloadInline(SortableInlineAdminMixin, admin.TabularInline):
    model = SectionDownload
    extra = 1


class PageSectionInline(admin.StackedInline):
    """Read/quick-edit only; drag-and-drop reordering happens on the Page Section list (sortable there)."""
    model = PageSection
    extra = 0
    show_change_link = True
    fields = ("section_type", "is_visible", "heading", "subheading", "background_style", "alignment", "padding_size", "order")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "page_type", "is_published", "view_on_site_link")
    list_filter = ("is_published", "page_type")
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageSectionInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "page_type", "is_published")}),
        ("Hero", {"fields": (
            "hero_title", "hero_subtitle", "hero_bg_image", "hero_overlay_opacity",
            "hero_cta_label", "hero_cta_url", "hero_cta_2_label", "hero_cta_2_url",
        )}),
        ("Layout", {"fields": ("show_breadcrumb",)}),
        ("SEO", {"fields": ("meta_title", "meta_description", "share_image", "noindex")}),
    )
    actions = ["publish", "unpublish"]

    @admin.action(description="Publish selected pages")
    def publish(self, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Unpublish selected pages")
    def unpublish(self, request, queryset):
        queryset.update(is_published=False)

    def view_on_site_link(self, obj):
        return format_html('<a href="{}" target="_blank">View on site</a>', obj.get_absolute_url())


@admin.register(PageSection)
class PageSectionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("page", "section_type", "is_visible", "order")
    list_filter = ("section_type", "is_visible", "page")
    inlines = [
        SectionFeatureCardInline, SectionStatInline, SectionTimelineItemInline,
        SectionStepInline, SectionFAQLinkInline, SectionGalleryImageInline, SectionDownloadInline,
    ]
