from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from dtvpicker.forms import VenueForm

def addVenue(request):
    """This view allows super users to add new venues to the venues table in the database."""

    if not request.user.is_superuser:
        return HttpResponseForbidden('This view can be accessed by superusers only. If you want to add a venue, please contact the Core Team.')
        
    form = VenueForm()
        
    if request.method == 'POST':
        
        form = VenueForm(request.POST.copy())
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/AddVenue/')
    
    return render_to_response ('dtvpicker/VenuePages/addEditVenue.html', locals(), context_instance = RequestContext(request))
    

