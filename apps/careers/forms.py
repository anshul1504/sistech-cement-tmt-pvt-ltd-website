from django import forms

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="")

    class Meta:
        model = JobApplication
        fields = ("name", "phone", "email", "city", "total_experience", "current_company", "current_ctc", "expected_ctc", "notice_period", "resume", "cover_letter", "consent")
        labels = {
            "name": "Full name", "phone": "Mobile number", "total_experience": "Total experience (years)",
            "current_ctc": "Current CTC", "expected_ctc": "Expected CTC",
            "cover_letter": "Why are you a good fit?",
            "consent": "I confirm that the information provided is correct and consent to SISTECH processing my application.",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your full name", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "10-digit mobile number", "inputmode": "numeric", "pattern": "[0-9]{10}"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "city": forms.TextInput(attrs={"placeholder": "Current city"}),
            "total_experience": forms.NumberInput(attrs={"min": 0, "max": 60, "step": ".5"}),
            "current_company": forms.TextInput(attrs={"placeholder": "Current / most recent employer"}),
            "current_ctc": forms.TextInput(attrs={"placeholder": "Optional"}),
            "expected_ctc": forms.TextInput(attrs={"placeholder": "Optional"}),
            "notice_period": forms.TextInput(attrs={"placeholder": "e.g. Immediate, 30 days"}),
            "resume": forms.ClearableFileInput(attrs={"accept": ".pdf,.doc,.docx"}),
            "cover_letter": forms.Textarea(attrs={"rows": 4, "placeholder": "Briefly describe your relevant experience and interest"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs["maxlength"] = 10

    def clean_phone(self):
        digits = "".join(c for c in self.cleaned_data["phone"] if c.isdigit())
        if len(digits) == 12 and digits.startswith("91"):
            digits = digits[2:]
        if len(digits) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return f"+91{digits}"

    def clean_resume(self):
        resume = self.cleaned_data["resume"]
        allowed_types = {
            "application/pdf", "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        }
        content_type = getattr(resume, "content_type", "")
        if content_type and content_type not in allowed_types:
            raise forms.ValidationError("Upload a PDF, DOC or DOCX resume.")
        return resume

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Unable to submit this application.")
        if not cleaned.get("consent"):
            self.add_error("consent", "Please accept the declaration to continue.")
        return cleaned
