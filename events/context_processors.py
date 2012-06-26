# instead of importing settings in each function, and then calling {{settings.PROJECT_DIR_NAME}} in templates, now you can directly write {{pro_dir}} and get the same thing. Make sure this function is included in your TEMPLATE_CONTEXT_PROCESSORS in your local settings.
def project_dir_name(request):
    from django.conf import settings
    return {'pro_dir':settings.PROJECT_DIR_NAME}
