#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module holds the views to lock and unlock events."""

from BaseClasses import CoordProtectedView, CoreProtectedView

from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from dtvpicker.models import SubEvent
from events.models import Event
from dtvpicker.forms import EventUnlockForm


class LockEvent(CoordProtectedView):

    """
    Includes the views to Lock an event.
    An event can be locked only when its lock status is False. This happens when:
        * The event has atleast one registered sub-event.
        * All fields of all sub-events are filled.
    """

    def handle_GET(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        try:  # To get the event
            eventRequested = Event.objects.get(title=kwargs['event'])
        except:
            raise Http404('Invalid event supplied.')  # If the event requested is not found in the database

        if eventRequested.lock_status != 'not_locked':
            raise Http404('Event cannot be locked.')

        subEventList = \
            SubEvent.objects.filter(event=eventRequested).order_by('start_date_and_time'
                )

        return render_to_response('dtvpicker/EventPages/lockEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))

    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        try:  # To get the event
            eventRequested = Event.objects.get(title=kwargs['event'])
        except:
            raise Http404('Invalid event supplied.')  # If the event requested is not found in the database

        if eventRequested.lock_status != 'not_locked':
            raise Http404('Event cannot be locked.')

        eventRequested.lock_status = 'locked'
        eventRequested.unlock_reason = ''
        eventRequested.save()

        return HttpResponseRedirect(settings.SITE_URL
                                    + 'DTVPicker/Summary/')


class UnlockEvent(CoreProtectedView):

    """
    Includes the views to Unlock an event.
    An event can be unlocked only when it is locked
    """

    def handle_GET(self, request, **kwargs):
        try:  # To get the event
            eventRequested = Event.objects.get(title=kwargs['event'])
        except:
            raise Http404('Invalid event supplied.')  # If the event requested is not found in the database

        if eventRequested.lock_status != 'locked':
            raise Http404('Event cannot be unlocked.')

        unlockForm = EventUnlockForm()

        subEventList = \
            SubEvent.objects.filter(event=eventRequested).order_by('start_date_and_time'
                )

        return render_to_response('dtvpicker/EventPages/unlockEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))

    def handle_POST(self, request, **kwargs):
        try:  # To get the event
            eventRequested = Event.objects.get(title=kwargs['event'])
        except:
            raise Http404('Invalid event supplied.')  # If the event requested is not found in the database

        if eventRequested.lock_status != 'locked':
            raise Http404('Event cannot be unlocked.')

        unlockForm = EventUnlockForm(request.POST)

        if unlockForm.is_valid():
            submittedData = unlockForm.cleaned_data
            eventRequested.lock_status = 'unlocked_by_core'
            eventRequested.unlock_reason = submittedData['unlock_reason'
                    ]
            eventRequested.save()

            return HttpResponseRedirect(settings.SITE_URL
                    + 'DTVPicker/Summary/')

        return render_to_response('dtvpicker/EventPages/unlockEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))


