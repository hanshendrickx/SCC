from django.urls import path
from . import views

app_name = "emergency"

urlpatterns = [
    path("start/", views.start, name="emergency-start"),
    path("threat/", views.threat, name="threat"),
]
