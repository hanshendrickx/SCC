from django.contrib import admin
from django.urls import include, path
from django.conf import settings          # 👈 add this
from django.conf.urls.static import static # 👈 add this

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("api/", include("snippets.urls")),
]

# 👇 ONLY for development – serves user-uploaded files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
