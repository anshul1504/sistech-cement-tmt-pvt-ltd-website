from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.contrib import admin

from apps.faq.models import FAQCategory, FAQItem


class FAQItemInline(SortableInlineAdminMixin, admin.TabularInline):
    model = FAQItem
    extra = 1
    fields = ("question", "answer", "is_active", "order")


@admin.register(FAQCategory)
class FAQCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "order")
    inlines = [FAQItemInline]


@admin.register(FAQItem)
class FAQItemAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("question", "category", "is_active", "order")
    list_filter = ("category", "is_active")
    search_fields = ("question",)
