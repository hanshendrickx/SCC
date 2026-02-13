from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from emergency import views as emergency_views  # add

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include("snippets.urls")),
    path("emergency/", include("emergency.urls")),
    path("start.html", emergency_views.start, name="start-html"),
    path("threat.html", emergency_views.threat, name="threat-html"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
