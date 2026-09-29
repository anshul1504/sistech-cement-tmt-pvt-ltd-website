from django.contrib import admin

from .models import ContactEnquiry


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "city", "enquiry_type", "created_at", "is_resolved")
    list_filter = ("enquiry_type", "is_resolved", "created_at")
    search_fields = ("name", "phone", "email", "city", "message")
    list_editable = ("is_resolved",)
    readonly_fields = ("created_at",)
