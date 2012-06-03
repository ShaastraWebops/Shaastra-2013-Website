from django.conf import settings

"""
django.conf.settings is not a module; it is
an object that has the already defined variables
in django.conf.global_settings, and the new
variables defined in the local settings. So do 
not import from global_settings or the settings
file with site-specific settings
"""

def url(request):
    return {'SITE_URL': settings.SITE_URL}
