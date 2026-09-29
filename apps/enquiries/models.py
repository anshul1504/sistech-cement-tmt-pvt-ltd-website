from django.db import models


class ContactEnquiry(models.Model):
    ENQUIRY_TYPES = [
        ("product", "Product enquiry"),
        ("dealer", "Dealership enquiry"),
        ("bulk", "Bulk / project requirement"),
        ("support", "Customer support"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    city = models.CharField(max_length=100, blank=True, default="")
    enquiry_type = models.CharField(max_length=20, choices=ENQUIRY_TYPES)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Contact enquiry"
        verbose_name_plural = "Contact enquiries"

    def __str__(self):
        return f"{self.name} — {self.get_enquiry_type_display()}"
