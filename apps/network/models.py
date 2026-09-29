import uuid

from django.conf import settings
from django.db import models


class DealerApplication(models.Model):
    BUSINESS_TYPES = [
        ("retailer", "Building material retailer"),
        ("wholesaler", "Wholesaler / distributor"),
        ("contractor", "Contractor / builder"),
        ("new", "Starting a new business"),
        ("other", "Other"),
    ]
    INVESTMENT_RANGES = [
        ("under_5", "Below ₹5 lakh"),
        ("5_10", "₹5–10 lakh"),
        ("10_25", "₹10–25 lakh"),
        ("25_plus", "Above ₹25 lakh"),
    ]
    PRODUCT_INTERESTS = [
        ("cement", "Cement"),
        ("tmt", "TMT Bars"),
        ("both", "Cement and TMT Bars"),
    ]
    STATUSES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("under_review", "Under review"),
        ("approved", "Approved"),
        ("rejected", "Not approved"),
    ]

    application_number = models.CharField(max_length=20, unique=True, editable=False)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    business_name = models.CharField(max_length=150)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPES)
    years_in_business = models.PositiveSmallIntegerField(default=0)
    gst_number = models.CharField(max_length=15, blank=True)
    product_interest = models.CharField(max_length=20, choices=PRODUCT_INTERESTS)
    investment_range = models.CharField(max_length=20, choices=INVESTMENT_RANGES)
    has_shop = models.BooleanField(default=False)
    has_warehouse = models.BooleanField(default=False)
    existing_brands = models.CharField(max_length=250, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    message = models.TextField(blank=True)
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUSES, default="new")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="assigned_dealer_applications",
    )
    follow_up_date = models.DateField(null=True, blank=True)
    admin_notes = models.TextField(blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("status", "created_at")),
            models.Index(fields=("phone",)),
        ]
        verbose_name = "Dealer application"
        verbose_name_plural = "Dealer applications"

    def save(self, *args, **kwargs):
        if not self.application_number:
            self.application_number = f"SDL-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.application_number} — {self.business_name}"
