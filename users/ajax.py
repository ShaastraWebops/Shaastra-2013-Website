#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template import Template, Context, RequestContext, loader
from dajax.core import Dajax
from users.forms import AddCollegeForm
from users.models import College


@dajaxice_register
def college_register(request, form=''):
    if form == '':
        template = \
            loader.get_template('ajax/users/college_register.html')
        coll_form = AddCollegeForm()
        html = template.render(RequestContext(request, locals()))
        dajax = Dajax()
        dajax.assign('#reg', 'innerHTML', html)
        return dajax.json()
    dajax = Dajax()
    coll_form = AddCollegeForm(form)
    if coll_form.is_valid():
        college = coll_form.cleaned_data['name']
        if college.find('&') >= 0:
            college = college.replace('&', 'and')
        city = coll_form.cleaned_data['city']
        state = coll_form.cleaned_data['state']

        if len(College.objects.filter(name=college, city=city,
               state=state)) == 0:
            college = College(name=college, city=city, state=state)
            college.save()
            data = college.name + ',' + college.city
            flag = 1
        else:
            flag = 2
    else:
        flag = 0
    dajax.add_data(flag, 'reg_done')
    return dajax.json()
