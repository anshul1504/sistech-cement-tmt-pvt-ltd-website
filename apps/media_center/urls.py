from django.urls import path

from .views import gallery

app_name = "media_center"
urlpatterns = [path("", gallery, name="gallery")]
