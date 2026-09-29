from django.contrib import admin

from .models import JobApplication, JobOpening


@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display = ("title", "department", "location", "employment_type", "openings", "application_deadline", "is_active", "is_featured", "application_count")
    list_filter = ("is_active", "is_featured", "employment_type", "department", "location")
    search_fields = ("title", "department", "location", "summary", "skills")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_active", "is_featured")
    date_hierarchy = "created_at"

    @admin.display(description="Applications")
    def application_count(self, obj):
        return obj.applications.count()


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("reference_number", "name", "job", "phone", "city", "total_experience", "status", "created_at")
    list_filter = ("status", "job__department", "job", "created_at")
    search_fields = ("reference_number", "name", "phone", "email", "city", "job__title")
    readonly_fields = ("reference_number", "source_url", "ip_address", "created_at", "updated_at")
    list_editable = ("status",)
    list_select_related = ("job",)
    date_hierarchy = "created_at"
    fieldsets = (
        ("Application", {"fields": ("reference_number", "job", "status", "created_at", "updated_at")}),
        ("Candidate", {"fields": ("name", "phone", "email", "city", "total_experience", "current_company")}),
        ("Compensation & availability", {"fields": ("current_ctc", "expected_ctc", "notice_period")}),
        ("Documents", {"fields": ("resume", "cover_letter", "consent")}),
        ("Internal review", {"fields": ("admin_notes",)}),
        ("Submission audit", {"classes": ("collapse",), "fields": ("source_url", "ip_address")}),
    )
