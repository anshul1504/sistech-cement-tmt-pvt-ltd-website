from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import robots_txt

urlpatterns = [
    path(settings.ADMIN_URL_PATH, admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("careers/", include("apps.careers.urls")),
    path("gallery/", include("apps.media_center.urls")),
    path("blog/", include("apps.media_center.blog_urls")),
    path("", include("apps.core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / "static")

handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"
