from django.shortcuts import render

from apps.core.models import SiteSettings

EXEMPT_PATH_PREFIXES = ("/admin", "/static", "/media")


class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings_obj = SiteSettings.load()
        if settings_obj.maintenance_mode and not request.path.startswith(EXEMPT_PATH_PREFIXES) and not request.user.is_staff:
            return render(request, "errors/maintenance.html", {"site": settings_obj}, status=503)
        return self.get_response(request)
