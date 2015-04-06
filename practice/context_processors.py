from django.conf import settings


def important(request):
    return {'GOOGLE_ANALYTICS': settings.ON_SERVER and not settings.DEBUG}