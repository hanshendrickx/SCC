from django.urls import path
from .views import (
    HomePageView,
    AboutPageView,
    AdultPageView,
    ChildPageView,
    ParentPageView,
    TeenPageView,
    GuestPageView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("adult/", AdultPageView.as_view(), name="adult"),
    path("child/", ChildPageView.as_view(), name="child"),
    path("parent/", ParentPageView.as_view(), name="parent"),
    path("teen/", TeenPageView.as_view(), name="teen"),
    path("guest/", GuestPageView.as_view(), name="guest"),
]
