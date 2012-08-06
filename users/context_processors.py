#!/usr/bin/python
# -*- coding: utf-8 -*-


def site_url(request):
    from django.conf import settings
    return {'site_url': settings.SITE_URL}


