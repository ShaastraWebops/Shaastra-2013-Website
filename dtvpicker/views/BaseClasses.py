#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module holds the class definitions of all the abstract base classes."""

from django.http import HttpResponseNotAllowed, Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

from dtvpicker.models import SubEvent
from events.models import Event

import datetime


class BaseView(object):

    """Parent class. All classes below inherit this."""

    def __call__(self, request, **kwargs):

        # Handles request and dispatches the corresponding handler based on the type of request (GET/POST)

        requestMethod = request.META['REQUEST_METHOD'].upper()
        handler = getattr(self, 'handle_%s' % requestMethod, None)

        if handler is None:
            methods = []
            for x in dir(self):
                if x.startswith('handle_'):
                    methods.append(x[7:])
            return HttpResponseNotAllowed(methods)

        return handler(request, **kwargs)


class ProtectedView(BaseView):

    """
    ProtectedView requires users to authenticate themselves before proceeding to the computation logic.
    """

    @method_decorator(login_required)
    def userAuthentication(self, request, **kwargs):
        return True

    def __call__(self, request, **kwargs):
        """
        * Checks authentication
        * Handles request
        * Dispatches the corresponding handler based on the type of request (GET/POST)
        """

        # TODO(Anant, anant.girdhar@gmail.com): Overridden class method called after authentication.
        #                                       Confirm working.

        # Overriding BaseView.__call__ to check authentication.

        if self.userAuthentication(request, **kwargs) == False:
            return HttpResponseForbidden()

        return super(ProtectedView, self).__call__(request, **kwargs)  # Calling the base class' __call__() and returning whatever is returned.


class CoordProtectedView(ProtectedView):

    """
    CoordProtectedView requires the user to be authenticated and to be a coord before proceeding to the computation logic.
    """

    @method_decorator(login_required)
    def userAuthentication(self, request, **kwargs):
        if request.user.get_profile().is_coord_of is not None:
            return True
        return False

    def permissionsGranted(self, request, **kwargs):
        """
        Checks if the coord has permissions to access the requested event.
        """

        try:
            if request.user.get_profile().is_coord_of \
                != Event.objects.get(title=kwargs['event']):
                return False  # If the coord is not coord of the requested event
            return True
        except:
            raise Http404('You do not have permissions to view this page.'
                          )


        # TODO(Anant): Make multiple exceptions and put correct error messages. Eg.:
        # If get_profile raises an exception: 'User profile does not exist.'
        # If is_coord_of raises an exception: 'User profile not configured correctly. Contact webmaster for more information.'
        # If Event.objects.get raises an exceptions: 'Event not found.'

class CoreProtectedView(ProtectedView):

    """
    CoreProtectedView requires the user to be authenticated and to be a core before proceeding to the computation logic.
    """

    @method_decorator(login_required)
    def userAuthentication(self, request, **kwargs):
        if request.user.get_profile().is_core:
            return True
        return False


class SubEventAddEditDeleteABC(CoordProtectedView):

    """
    ABC (Abstract Base Class) for Adding, Editing and Deleting SubEvents.
    This includes the functions that are required for all these operations.
    """

    def getSubEvent(self, subevent_name, event_name):
        """
        Gets the subevent referenced by the url from the database.
        Returns an instance of SubEvent having title as given in the url.
        If no object is found, raises Http404.
        """

        eventRequested = self.getEvent(event_name)

        try:  # to get the sub-event
            subeventRequested = \
                SubEvent.objects.filter(event=eventRequested)
            subeventRequested = \
                subeventRequested.get(title=subevent_name)
        except:
            raise Http404('Invalid sub-event supplied')  # If the sub-event requested is not found in the database

        return subeventRequested

    def getEvent(self, event_name):
        """
        Gets the event referenced by the url from the database.
        Returns an instance of Event having title as given in the url.
        If no object is found, raises Http404.
        If the event is locked (ie. no editing is possible), raises Http404.
        """

        try:  # To get the event
            eventRequested = Event.objects.get(title=event_name)
        except:
            raise Http404('Invalid event supplied')  # If the event requested is not found in the database

        if eventRequested.lock_status == 'locked':
            raise Http404('Event cannot be modified')

        return eventRequested

    def updateEventLockStatus(self, eventToUpdate):

        subEventList = SubEvent.objects.filter(event=eventToUpdate)

        newLockStatus = 'cannot_be_locked'

        if subEventList:
            newLockStatus = 'not_locked'
            for subevent in subEventList:
                if not (subevent.start_date_and_time and subevent.end_date_and_time and subevent.venue.count() > 0):  # Checks for missing fields.
                    newLockStatus = 'cannot_be_locked'
                    break

        eventToUpdate.lock_status = newLockStatus
        eventToUpdate.unlock_reason = ''
        eventToUpdate.save()
    
    def updateAndSaveSubEvent(self, form):
        newSubEvent = form.save(commit=False)
        newSubEvent.save()
        form.save_m2m()
        self.updateEventLockStatus(newSubEvent.event)

