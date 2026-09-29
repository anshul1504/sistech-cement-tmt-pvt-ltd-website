import re

from django import forms

from .models import DealerApplication


class DealerApplicationForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="")

    class Meta:
        model = DealerApplication
        fields = (
            "name", "phone", "email", "business_name", "business_type",
            "years_in_business", "gst_number", "product_interest",
            "investment_range", "has_shop", "has_warehouse", "existing_brands",
            "address", "city", "district", "state", "pincode", "message", "consent",
        )
        labels = {
            "name": "Applicant name", "phone": "Mobile number",
            "years_in_business": "Years in business", "gst_number": "GST number",
            "has_shop": "I have a retail shop / office",
            "has_warehouse": "I have warehouse / storage space",
            "existing_brands": "Brands currently handled",
            "message": "Additional information",
            "consent": "I confirm that the information provided is correct and agree to be contacted by SISTECH.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "10-digit mobile number", "inputmode": "numeric", "autocomplete": "tel", "maxlength": 10, "pattern": "[0-9]{10}"}),
            "email": forms.EmailInput(attrs={"placeholder": "Business email (optional)", "autocomplete": "email"}),
            "business_name": forms.TextInput(attrs={"placeholder": "Firm / shop name"}),
            "years_in_business": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "gst_number": forms.TextInput(attrs={"placeholder": "15-character GSTIN (optional)", "maxlength": 15}),
            "existing_brands": forms.TextInput(attrs={"placeholder": "Mention cement/TMT brands, if any"}),
            "address": forms.Textarea(attrs={"placeholder": "Business address", "rows": 3, "autocomplete": "street-address"}),
            "city": forms.TextInput(attrs={"placeholder": "City", "autocomplete": "address-level2"}),
            "district": forms.TextInput(attrs={"placeholder": "District"}),
            "state": forms.TextInput(attrs={"placeholder": "State", "autocomplete": "address-level1"}),
            "pincode": forms.TextInput(attrs={"placeholder": "6-digit PIN code", "inputmode": "numeric", "maxlength": 6, "autocomplete": "postal-code"}),
            "message": forms.Textarea(attrs={"placeholder": "Tell us about your market reach or dealership goals", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs["maxlength"] = 10

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(c for c in phone if c.isdigit())
        if len(digits) == 12 and digits.startswith("91"):
            digits = digits[2:]
        if len(digits) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return f"+91{digits}"

    def clean_pincode(self):
        pincode = self.cleaned_data["pincode"].strip()
        if not re.fullmatch(r"[1-9][0-9]{5}", pincode):
            raise forms.ValidationError("Enter a valid 6-digit PIN code.")
        return pincode

    def clean_gst_number(self):
        gst = self.cleaned_data.get("gst_number", "").strip().upper()
        if gst and not re.fullmatch(r"[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][A-Z0-9]Z[A-Z0-9]", gst):
            raise forms.ValidationError("Enter a valid 15-character GST number.")
        return gst

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Unable to submit this application.")
        if not cleaned.get("consent"):
            self.add_error("consent", "Please accept the declaration to continue.")
        return cleaned
