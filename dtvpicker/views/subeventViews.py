#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module holds the views to add, edit and delete sub-events."""

from BaseClasses import SubEventAddEditDeleteABC

from django.http import HttpResponseForbidden, HttpResponseRedirect, \
    Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from dtvpicker.models import SubEvent
from events.models import Event
from dtvpicker.forms import SubEventForm
from django.contrib.sitemaps import ping_google


class SubEventAdd(SubEventAddEditDeleteABC):

    """
    Adding a sub-event to the database.
    Permissions: Event Coords only.
    Access: Only own events.
    Description: On adding a sub-event to the database, only the name of the sub-event and its event are added to the database.
                 All other details (start, end, venue) are to be updated separately in EditSubEvent.
                 So, after the sube event is added, we redirect to the EditSubEvent page.
    """

    def handle_GET(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        eventRequested = self.getEvent(kwargs['event'])

        form = SubEventForm(initial={'event': '%d' % eventRequested.id})
        form_mode = 'add'  # For re-using the template (only difference: add/edit button)
        return render_to_response('dtvpicker/SubeventPages/addEditSubEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))

    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        eventRequested = self.getEvent(kwargs['event'])

        formDataReceived = request.POST.copy()
        
        form = SubEventForm(formDataReceived)

        if form.is_valid():
            newSubEventData = form.cleaned_data

            if newSubEventData['event'] != eventRequested:
                # Event was a hidden field, how can it get updated? Some malicious posting has happened. Raise error.
                raise Http404('How did the event get updated? Malicious POSTing huh?! You shouldn\'t be allowed to continue.')
            
            self.updateAndSaveSubEvent(form)
            return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/Summary/')
        
        form_mode = 'add'  # For re-using the template (only difference: add/edit button)
        return render_to_response('dtvpicker/SubeventPages/addEditSubEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))


class SubEventEdit(SubEventAddEditDeleteABC):

    """
    Editing details of sub-event.
    Permissions: Event Coords only.
    Access: Only own events.
    """

    def handle_GET(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        eventRequested = self.getEvent(kwargs['event'])
        subeventRequested = self.getSubEvent(kwargs['subevent'], kwargs['event'])
        form = SubEventForm(initial = {'title'                  : subeventRequested.title,
                                       'start_date_and_time'    : subeventRequested.start_date_and_time,
                                       'end_date_and_time'      : subeventRequested.end_date_and_time,
                                       'venue'                  : subeventRequested.venue.all(),
                                       'event'                  : eventRequested, })
        form_mode = 'edit'  # For re-using the template (only difference: add/edit button)
        return render_to_response('dtvpicker/SubeventPages/addEditSubEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))

    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        eventRequested = self.getEvent(kwargs['event'])
        subeventRequested = self.getSubEvent(kwargs['subevent'], kwargs['event'])
        formDataReceived = request.POST.copy()

        form = SubEventForm(formDataReceived,
                            instance=self.getSubEvent(kwargs['subevent'
                            ], kwargs['event']))

                # Here I have not set the instance as subeventRequested
                # (although I use it for almost everything else)
                # but rather I have called the getSubEvent method again
                # because if the form is posted with a different title
                # then the title of the subeventRequested object is also updated.
                # This does not have any effect on this method
                # but I have used subeventRequested in the template for displaying the
                # the sub-event's title which changes although you still want to update the same instance!

        if form.is_valid():
            newSubEventData = form.cleaned_data

            if newSubEventData['event'] != eventRequested:
                # Event was a hidden field, how can it get updated? Some malicious posting has happened. Raise error.
                raise Http404('How did the event get updated? Malicious POSTing huh?!')
            
            self.updateAndSaveSubEvent(form)
            return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/Summary/')

        form_mode = 'edit'  # For re-using the template (only difference: add/edit button)
        return render_to_response('dtvpicker/SubeventPages/addEditSubEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))


class SubEventDelete(SubEventAddEditDeleteABC):

    """
    Deleting sub-event.
    Permissions: Coords only.
    Access: Only own events.
    """

    def handle_GET(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        eventRequested = self.getEvent(kwargs['event'])
        subeventRequested = self.getSubEvent(kwargs['subevent'],
                kwargs['event'])

        return render_to_response('dtvpicker/SubeventPages/deleteSubEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))

    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        subeventRequested = self.getSubEvent(kwargs['subevent'], kwargs['event'])
    	subeventRequested.delete()
	ping_google()   
        self.updateEventLockStatus(self.getEvent(kwargs['event']))

        return HttpResponseRedirect(settings.SITE_URL
                                    + 'DTVPicker/Summary/')


