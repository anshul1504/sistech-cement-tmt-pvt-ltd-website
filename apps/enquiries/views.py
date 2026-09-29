from django.shortcuts import redirect, render

from apps.core.views import get_page_or_none

from .forms import ContactEnquiryForm


def contact(request, submitted=False):
    page = get_page_or_none("contact")
    submitted = submitted or request.GET.get("submitted") == "1"

    if request.method == "POST":
        form = ContactEnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("core:contact_success")
    else:
        form = ContactEnquiryForm()

    return render(request, "pages/contact.html", {
        "page": page,
        "form": form,
        "submitted": submitted,
        "has_cta_section": True,
    })

# Create your views here.
