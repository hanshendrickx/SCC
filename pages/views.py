from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class AdultPageView(TemplateView):
    template_name = "pages/adult.html"


class ChildPageView(TemplateView):
    template_name = "pages/child.html"


class ParentPageView(TemplateView):
    template_name = "pages/parent.html"


class TeenPageView(TemplateView):
    template_name = "pages/teen.html"


class GuestPageView(TemplateView):
    template_name = "pages/guest.html"
