from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import JobApplication, JobOpening


class CareerFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.job = JobOpening.objects.create(
            title="Area Sales Executive", slug="area-sales-executive", department="Sales",
            location="Indore, Madhya Pradesh", employment_type="full_time", openings=2,
            experience_min=2, experience_max=5, summary="Grow the dealer network in the assigned market.",
            description="Work with dealers and customers across the assigned territory.",
            responsibilities="Develop the dealer network\nAchieve sales targets",
            requirements="Strong communication\nConstruction-material sales experience",
            qualifications="Graduate in any discipline", skills="Sales, Dealer Management, CRM",
        )

    def test_career_listing_shows_active_job(self):
        response = self.client.get(reverse("careers:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.title)

    def test_job_detail_contains_application_form(self):
        response = self.client.get(self.job.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit Application")

    def test_application_with_resume_is_saved(self):
        resume = SimpleUploadedFile("resume.pdf", b"%PDF-1.4 test resume", content_type="application/pdf")
        response = self.client.post(self.job.get_absolute_url(), {
            "name": "Anita Sharma", "phone": "9876543210", "email": "anita@example.com",
            "city": "Indore", "total_experience": "3.5", "current_company": "ABC Materials",
            "current_ctc": "4 LPA", "expected_ctc": "5 LPA", "notice_period": "30 days",
            "cover_letter": "Relevant dealer network experience.", "consent": "on", "resume": resume,
        })
        self.assertRedirects(response, reverse("careers:success", kwargs={"slug": self.job.slug}))
        application = JobApplication.objects.get()
        self.assertEqual(application.phone, "+919876543210")
        self.assertTrue(application.reference_number.startswith("SCA-"))
        self.assertEqual(application.job, self.job)

# Create your tests here.
