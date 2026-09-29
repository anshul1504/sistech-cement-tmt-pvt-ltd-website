import uuid

from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


def validate_resume_size(file):
    if file.size > 5 * 1024 * 1024:
        from django.core.exceptions import ValidationError
        raise ValidationError("Resume file must be 5 MB or smaller.")


class JobOpening(models.Model):
    EMPLOYMENT_TYPES = [
        ("full_time", "Full time"), ("part_time", "Part time"),
        ("contract", "Contract"), ("internship", "Internship"),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=120)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES, default="full_time")
    openings = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    experience_min = models.PositiveSmallIntegerField(default=0)
    experience_max = models.PositiveSmallIntegerField(default=0, help_text="Use 0 when there is no upper limit.")
    summary = models.CharField(max_length=300)
    description = models.TextField()
    responsibilities = models.TextField(help_text="Enter one responsibility per line.")
    requirements = models.TextField(help_text="Enter one requirement per line.")
    qualifications = models.TextField(blank=True, help_text="Enter one qualification per line.")
    skills = models.CharField(max_length=300, blank=True, help_text="Comma-separated skills.")
    salary_display = models.CharField(max_length=100, blank=True, help_text="Optional public salary range.")
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-is_featured", "-created_at")
        verbose_name = "Job opening"
        verbose_name_plural = "Job openings"

    @property
    def is_open(self):
        return self.is_active and (not self.application_deadline or self.application_deadline >= timezone.localdate())

    @property
    def experience_display(self):
        if self.experience_min == 0 and self.experience_max == 0:
            return "Freshers welcome"
        if self.experience_max and self.experience_max != self.experience_min:
            return f"{self.experience_min}–{self.experience_max} years"
        return f"{self.experience_min}+ years"

    def get_absolute_url(self):
        return reverse("careers:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUSES = [
        ("new", "New"), ("screening", "Screening"), ("shortlisted", "Shortlisted"),
        ("interview", "Interview"), ("selected", "Selected"), ("rejected", "Not selected"),
    ]

    reference_number = models.CharField(max_length=20, unique=True, editable=False)
    job = models.ForeignKey(JobOpening, on_delete=models.PROTECT, related_name="applications")
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    total_experience = models.DecimalField(
        max_digits=4, decimal_places=1, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(60)],
    )
    current_company = models.CharField(max_length=150, blank=True)
    current_ctc = models.CharField(max_length=80, blank=True)
    expected_ctc = models.CharField(max_length=80, blank=True)
    notice_period = models.CharField(max_length=80, blank=True)
    resume = models.FileField(
        upload_to="careers/resumes/%Y/%m/",
        validators=[FileExtensionValidator(("pdf", "doc", "docx")), validate_resume_size],
    )
    cover_letter = models.TextField(blank=True)
    consent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUSES, default="new")
    admin_notes = models.TextField(blank=True)
    source_url = models.URLField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("status", "created_at")), models.Index(fields=("email",))]

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.reference_number = f"SCA-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} — {self.name} — {self.job.title}"
