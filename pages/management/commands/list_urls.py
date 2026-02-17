from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import URLPattern, URLResolver


class Command(BaseCommand):
    help = "List all URL patterns in the project"

    def handle(self, *args, **options):
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [""])

        def list_urls(patterns, path=None):
            if path is None:
                path = []
            result = []
            for pattern in patterns:
                if isinstance(pattern, URLPattern):
                    result.append("".join(path) + str(pattern.pattern))
                elif isinstance(pattern, URLResolver):
                    result += list_urls(
                        pattern.url_patterns, path + [str(pattern.pattern)]
                    )
            return result

        for p in list_urls(urlconf.urlpatterns):
            self.stdout.write(p)
