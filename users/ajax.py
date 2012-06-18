from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.template import Template, Context, RequestContext
from dajax.core import Dajax
from django.conf import settings
from users.forms import AddCollegeForm
from users.models import College
import os

def get_template(file_name):
    #this is used to get templates from the path /.../shaastra/events/templates/events/ajax      (*in my case)
    #note - a separate folder for ajax templates.
    #this function opens files (*.html) and returns them as python string.
    filepath = os.path.join(settings.AJAX_TEMPLATE_DIR, file_name)
    f = open(filepath, mode='r')
    return f.read()

@dajaxice_register
def college_register(request, form=""):
    if form == "" :
        template = get_template('college_register.html')
        coll_form=AddCollegeForm()
        html=Template(template).render(RequestContext(request,locals()))
        dajax = Dajax()
        dajax.assign('#reg', 'innerHTML', html)
        return dajax.json()
    dajax = Dajax()
    coll_form = AddCollegeForm(form)
    if coll_form.is_valid():
        college=coll_form.cleaned_data['name']
        if college.find('&')>=0:
            college = college.replace('&','and')
        city=coll_form.cleaned_data['city']
        state=coll_form.cleaned_data['state']
        
        if len(College.objects.filter(name=college, city=city, state=state))== 0 :
            college=College (name = college, city = city, state = state)
            college.save()
            data = college.name+","+college.city
            flag=1            
        else:
            flag=2
    else:
        flag=0
    dajax.add_data(flag, 'reg_done')
    return dajax.json()
