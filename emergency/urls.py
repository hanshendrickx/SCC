from django.urls import path
from . import views

app_name = "emergency"

urlpatterns = [
    path("start/", views.start, name="start"),
    path("threat/", views.threat, name="threat"),
]

# in templates use {% url 'emergency:start' %} {% url 'emergency:threat' %}
