from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.decorators import login_required
from dtvpicker.models import Venue, VenueGroupAlias
from dtvpicker.forms import VenueForm, VenueGroupAliasForm

@login_required
def venuesHome(request):
    """This view allows super users to add or modify the venues stores in the database."""
    
    if not request.user.is_superuser:
        return HttpResponseForbidden('Restricted access. For details contact the SWOps Team.')
     
    form = VenueForm()
    venues = Venue.objects.all().order_by('block', 'title')
     
    if request.method == 'POST':
        
        form = VenueForm(request.POST.copy())
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/Venues/')
     
    return render_to_response('dtvpicker/VenuePages/venuesHome.html', locals(), context_instance = RequestContext(request))
     
@login_required
def editVenue(request, venueID):
    """This view allows super users to edit the venues stored in the database."""

    if not request.user.is_superuser:
        return HttpResponseForbidden('Restricted access. For details contact the SWOps Team.')

    venueID = int(venueID)
    
    try:
        venueObj = Venue.objects.get(id = venueID)
    except Venue.DoesNotExist:
        raise Http404('The requested venue id does not exist.')
    
    form = VenueForm(instance = venueObj)
    
    if request.method == 'POST':
        
        form = VenueForm(request.POST.copy(), instance = venueObj)
        
        if form.is_valid():
            form.save
            return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/Venues/')

    return render_to_response('dtvpicker/VenuePages/venueEdit.html', locals(), context_instance = RequestContext(request))
    
@login_required
def deleteVenue(request, venueID):
    """This view allows super users to delete the venue aliases stored in the database."""

    if not request.user.is_superuser:
        return HttpResponseForbidden('Restricted access. For details contact the SWOps Team.')

    venueID = int(venueID)
    
    try:
        venueObj = Venue.objects.get(id = venueID)
    except Venue.DoesNotExist:
        raise Http404('The requested venue id does not exist.')
        
    venueObj.delete()
    
    return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/Venues/')

@login_required
def venueAliasesHome(request):
    """This view allows super users to add or modify the venue aliases stores in the database."""
    
    if not request.user.is_superuser:
        return HttpResponseForbidden('Restricted access. For details contact the SWOps Team.')
     
    form = VenueGroupAliasForm()
    aliases = VenueGroupAlias.objects.all().order_by('alias')
     
    if request.method == 'POST':
        
        form = VenueGroupAliasForm(request.POST.copy())
        
        if form.is_valid():
            newAlias = form.save(commit=False)
            newAlias.save()
            form.save_m2m()
            return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/VenueAliases/')
     
    return render_to_response('dtvpicker/VenuePages/venueGroupAliasHome.html', locals(), context_instance = RequestContext(request))
     
@login_required
def editVenueAliases(request, aliasID):
    """This view allows super users to edit the venue aliases stored in the database."""

    if not request.user.is_superuser:
        return HttpResponseForbidden('Restricted access. For details contact the SWOps Team.')

    aliasID = int(aliasID)
    
    try:
        aliasObj = VenueGroupAlias.objects.get(id = aliasID)
    except VenueGroupAlias.DoesNotExist:
        raise Http404('The requested alias id does not exist.')
    
    form = VenueGroupAliasForm(instance = aliasObj)
    
    if request.method == 'POST':
        
        form = VenueGroupAliasForm(request.POST.copy(), instance = aliasObj)
        
        if form.is_valid():
            newAlias = form.save(commit=False)
            newAlias.save()
            form.save_m2m()
            return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/VenueAliases/')

    return render_to_response('dtvpicker/VenuePages/venueGroupAliasEdit.html', locals(), context_instance = RequestContext(request))
    
@login_required
def deleteVenueAliases(request, aliasID):
    """This view allows super users to delete the venue aliases stored in the database."""

    if not request.user.is_superuser:
        return HttpResponseForbidden('Restricted access. For details contact the SWOps Team.')

    aliasID = int(aliasID)
    
    try:
        aliasObj = VenueGroupAlias.objects.get(id = aliasID)
    except VenueGroupAlias.DoesNotExist:
        raise Http404('The requested alias id does not exist.')
        
    aliasObj.delete()
    
    return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/VenueAliases/')

