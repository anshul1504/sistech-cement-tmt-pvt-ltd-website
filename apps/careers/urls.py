from django.urls import path

from . import views

app_name = "careers"

urlpatterns = [
    path("", views.career_list, name="list"),
    path("<slug:slug>/", views.job_detail, name="detail"),
    path("<slug:slug>/thank-you/", views.job_detail, {"submitted": True}, name="success"),
]
