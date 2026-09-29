from django.shortcuts import redirect, render

from apps.core.views import get_page_or_none

from .forms import DealerApplicationForm


def dealer_application(request, submitted=False):
    page = get_page_or_none("distribution_network")
    submitted = submitted or request.GET.get("submitted") == "1"
    application_number = request.session.pop("dealer_application_number", "") if submitted else ""

    if request.method == "POST":
        form = DealerApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.source_url = request.build_absolute_uri(request.path)
            application.ip_address = request.META.get("REMOTE_ADDR") or None
            application.user_agent = request.META.get("HTTP_USER_AGENT", "")[:500]
            application.save()
            request.session["dealer_application_number"] = application.application_number
            return redirect("core:dealer_success")
    else:
        form = DealerApplicationForm()

    return render(request, "pages/dealer_application.html", {
        "page": page,
        "form": form,
        "submitted": submitted,
        "application_number": application_number,
        "has_cta_section": True,
    })

# Create your views here.
