from django.test import TestCase
from django.urls import reverse
from django.contrib import admin

from .models import DealerApplication


class DealerApplicationTests(TestCase):
    valid_data = {
        "name": "Rahul Sharma",
        "phone": "9876543210",
        "email": "rahul@example.com",
        "business_name": "Sharma Building Materials",
        "business_type": "retailer",
        "years_in_business": 5,
        "gst_number": "",
        "product_interest": "both",
        "investment_range": "10_25",
        "has_shop": "on",
        "has_warehouse": "on",
        "existing_brands": "Local brands",
        "address": "Main Road",
        "city": "Indore",
        "district": "Indore",
        "state": "Madhya Pradesh",
        "pincode": "452001",
        "message": "Interested in dealership.",
        "consent": "on",
    }

    def test_dealer_page_loads(self):
        response = self.client.get(reverse("core:distribution_network"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tell Us About Your Business")

    def test_valid_application_is_saved_with_reference(self):
        response = self.client.post(reverse("core:distribution_network"), self.valid_data)
        self.assertRedirects(response, reverse("core:dealer_success"))
        application = DealerApplication.objects.get()
        self.assertTrue(application.application_number.startswith("SDL-"))
        self.assertEqual(application.phone, "+919876543210")
        self.assertTrue(application.source_url.endswith("/distribution-network/"))
        self.assertEqual(application.ip_address, "127.0.0.1")

    def test_invalid_phone_and_pincode_are_rejected(self):
        data = {**self.valid_data, "phone": "123", "pincode": "000000"}
        response = self.client.post(reverse("core:distribution_network"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid 10-digit mobile number.")
        self.assertContains(response, "Enter a valid 6-digit PIN code.")
        self.assertFalse(DealerApplication.objects.exists())

    def test_application_is_available_in_admin(self):
        self.assertTrue(admin.site.is_registered(DealerApplication))

# Create your tests here.
