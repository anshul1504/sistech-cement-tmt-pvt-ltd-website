import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import DealerApplication


@admin.register(DealerApplication)
class DealerApplicationAdmin(admin.ModelAdmin):
    list_display = ("application_number", "business_name", "name", "phone", "city", "state", "product_interest", "status", "assigned_to", "follow_up_date", "created_at")
    list_filter = ("status", "product_interest", "business_type", "investment_range", "state", "created_at")
    search_fields = ("application_number", "business_name", "name", "phone", "email", "city", "district", "gst_number")
    readonly_fields = ("application_number", "source_url", "ip_address", "user_agent", "created_at", "updated_at")
    list_editable = ("status",)
    list_select_related = ("assigned_to",)
    date_hierarchy = "created_at"
    actions = ("mark_contacted", "mark_under_review", "export_csv")
    fieldsets = (
        ("Application", {"fields": ("application_number", "status", "assigned_to", "follow_up_date", "created_at", "updated_at")}),
        ("Applicant", {"fields": ("name", "phone", "email")}),
        ("Business", {"fields": ("business_name", "business_type", "years_in_business", "gst_number", "product_interest", "investment_range", "has_shop", "has_warehouse", "existing_brands")}),
        ("Territory", {"fields": ("address", "city", "district", "state", "pincode")}),
        ("Review", {"fields": ("message", "consent", "admin_notes")}),
        ("Submission audit", {"classes": ("collapse",), "fields": ("source_url", "ip_address", "user_agent")}),
    )

    @admin.action(description="Mark selected applications as contacted")
    def mark_contacted(self, request, queryset):
        self.message_user(request, f"{queryset.update(status='contacted')} application(s) marked as contacted.")

    @admin.action(description="Move selected applications to under review")
    def mark_under_review(self, request, queryset):
        self.message_user(request, f"{queryset.update(status='under_review')} application(s) moved to under review.")

    @admin.action(description="Export selected applications as CSV")
    def export_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="dealer-applications.csv"'
        writer = csv.writer(response)
        writer.writerow(("Reference", "Date", "Status", "Applicant", "Phone", "Email", "Business", "Business type", "Products", "Investment", "City", "District", "State", "PIN", "GST"))
        for item in queryset:
            def safe(value):
                text = str(value or "")
                return f"'{text}" if text.startswith(("=", "+", "-", "@")) else text
            writer.writerow((
                item.application_number, item.created_at.isoformat(), item.get_status_display(),
                safe(item.name), safe(item.phone), safe(item.email), safe(item.business_name),
                item.get_business_type_display(), item.get_product_interest_display(),
                item.get_investment_range_display(), safe(item.city), safe(item.district),
                safe(item.state), safe(item.pincode), safe(item.gst_number),
            ))
        return response
