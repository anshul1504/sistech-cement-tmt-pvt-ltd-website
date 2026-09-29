from django.test import TestCase
from django.urls import reverse

from .models import ContactEnquiry


class ContactPageTests(TestCase):
    def test_contact_page_loads(self):
        response = self.client.get(reverse("core:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How Can We Help?")

    def test_valid_enquiry_is_saved(self):
        response = self.client.post(reverse("core:contact"), {
            "name": "Test Customer",
            "phone": "9876543210",
            "email": "customer@example.com",
            "city": "Indore",
            "enquiry_type": "product",
            "message": "I need information about your products.",
        })
        self.assertRedirects(response, reverse("core:contact_success"))
        self.assertEqual(ContactEnquiry.objects.count(), 1)
        self.assertEqual(ContactEnquiry.objects.get().phone, "+919876543210")

    def test_invalid_phone_is_rejected(self):
        response = self.client.post(reverse("core:contact"), {
            "name": "Test Customer",
            "phone": "123",
            "city": "Indore",
            "enquiry_type": "product",
            "message": "Please call me.",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid 10-digit mobile number.")
        self.assertFalse(ContactEnquiry.objects.exists())

# Create your tests here.
