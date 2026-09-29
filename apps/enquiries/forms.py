from django import forms

from .models import ContactEnquiry


class ContactEnquiryForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="")

    class Meta:
        model = ContactEnquiry
        fields = ("name", "phone", "email", "enquiry_type", "message")
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "10-digit mobile number", "autocomplete": "tel", "inputmode": "numeric", "maxlength": 10, "pattern": "[0-9]{10}"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "enquiry_type": forms.Select(),
            "message": forms.Textarea(attrs={"placeholder": "Tell us how we can help", "rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs["maxlength"] = 10

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(character for character in phone if character.isdigit())
        if len(digits) == 12 and digits.startswith("91"):
            digits = digits[2:]
        if len(digits) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return f"+91{digits}"

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("website"):
            raise forms.ValidationError("Unable to submit this enquiry.")
        return cleaned_data
