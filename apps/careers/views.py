from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.core.views import get_page_or_none

from .forms import JobApplicationForm
from .models import JobOpening


def career_list(request):
    today = timezone.localdate()
    jobs = JobOpening.objects.filter(is_active=True).filter(Q(application_deadline__isnull=True) | Q(application_deadline__gte=today))
    query = request.GET.get("q", "").strip()
    department = request.GET.get("department", "").strip()
    location = request.GET.get("location", "").strip()
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(skills__icontains=query))
    if department:
        jobs = jobs.filter(department=department)
    if location:
        jobs = jobs.filter(location=location)
    page_obj = Paginator(jobs, 10).get_page(request.GET.get("page"))

    base = JobOpening.objects.filter(is_active=True)
    return render(request, "careers/list.html", {
        "page": get_page_or_none("careers"), "jobs": page_obj, "page_obj": page_obj,
        "query": query, "selected_department": department, "selected_location": location,
        "departments": base.values_list("department", flat=True).distinct().order_by("department"),
        "locations": base.values_list("location", flat=True).distinct().order_by("location"),
        "has_cta_section": True,
    })


def job_detail(request, slug, submitted=False):
    job = get_object_or_404(JobOpening, slug=slug, is_active=True)
    submitted = submitted or request.GET.get("submitted") == "1"
    reference = request.session.pop("job_application_reference", "") if submitted else ""

    if request.method == "POST" and job.is_open:
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.source_url = request.build_absolute_uri(request.path)
            application.ip_address = request.META.get("REMOTE_ADDR") or None
            application.save()
            request.session["job_application_reference"] = application.reference_number
            return redirect("careers:success", slug=job.slug)
    else:
        form = JobApplicationForm()

    return render(request, "careers/detail.html", {
        "page": get_page_or_none("careers"), "job": job, "form": form,
        "submitted": submitted, "reference": reference, "has_cta_section": True,
    })

# Create your views here.
