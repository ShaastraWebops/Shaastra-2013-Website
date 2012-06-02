from django.conf import settings

def url(request):
    return {'SITE_URL': settings.SITE_URL}
