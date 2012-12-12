#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module holds the views that show the DTV Summary on screen."""

from django.http import HttpResponseRedirect, HttpResponseForbidden, \
    HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

from miscFunctions import PDFGenAllowed

from dtvpicker.models import SubEvent
from events.models import Event
from dtvpicker.VenueChoices import VENUE_CHOICES


@login_required
def dtvHome(request):
    """
    This is the handler for the DTV Picker.
    Super users are shown the links to the various sectors (Venue Mgmt Sector, Venue Alias, Mgmt Sector, DTVP Summany Sector).
    All other users are redirected to the dtvSummaryHandler.
    """
        
    if request.user.is_superuser:
        return render_to_response('dtvpicker/SummaryPages/DTVSuperUserHome.html', locals(), context_instance = RequestContext(request))
        
    return HttpResponseRedirect(settings.SITE_URL + 'DTVPicker/Summary/')

@login_required
def dtvSummaryHandler(request):
    """
    This is the handler for the DTV Summary.
    If a Coord logs in, it redirects him to the By Event Page.
    If a Core logs in, and all the events are locked, it gives three options to see the DTV Summary by Event / Venue / Date.
    If all events are not locked, the Core is redirected to the By Event Page.
    """

    try:
        currentUserProfile = request.user.get_profile()
    except:

        # If the user's profile is not available

        return HttpResponse("Sorry. %s's user profile is not available."
                             % request.user.username)

    if currentUserProfile.is_coord_of:
        return HttpResponseRedirect(settings.SITE_URL
                                    + 'DTVPicker/Summary/ByEvent/')

    if currentUserProfile.is_core:

        if PDFGenAllowed():
            return render_to_response('dtvpicker/SummaryPages/DTVLanding.html'
                    , locals(),
                    context_instance=RequestContext(request))

        return HttpResponseRedirect(settings.SITE_URL
                                    + 'DTVPicker/Summary/ByEvent/')

    return HttpResponseForbidden('This page can be accessed by Cores and Coordinators only. Please login with proper authentication to proceed.'
                                 )


@login_required
def dtvSummaryByEvent(request):
    """
    Displays a summary of the DTV details of all events sorted by event.
    If core logs in: Displays summary of all events and sub-events with their date-time-venue (dtv).
    If coord logs in: Displays summary of his event and sub-events with their date-time-venue (dtv).
    There is a DTV PDF Generating option also which is available only to cores and only after all events are locked.
    """

    try:
        currentUserProfile = request.user.get_profile()
    except:

        # If the user's profile is not available

        return HttpResponse("Sorry. %s's user profile is not available."
                             % request.user.username)

    if currentUserProfile.is_core:

        # A core is allowed to see all events

        requestedEventList = Event.objects.all()
        happenings = []  # happenings is a list of tuples where

                        # the tuple structure is:
                        # (Event, [Sub-events under Event])

        enablePDFPrinting = PDFGenAllowed()  # Passed to the template to activate the PDF generation link.

        for requestedEvent in requestedEventList:
            Event_SubEventList = \
                SubEvent.objects.filter(event=requestedEvent).order_by('start_date_and_time'
                    )  # List of sub-events under

                                                                                                                 # requestedEvent

            happenings.append((requestedEvent, Event_SubEventList))

        return render_to_response('dtvpicker/SummaryPages/CoreDTVSummary_ByEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))
    else:

        # A coord can see only the events for which he is coord

        requestedEvent = request.user.get_profile().is_coord_of
        happenings = []  # happenings is a list of tuples where

                        # the tuple structure is:
                        # (Event, [Sub-events under Event])

        Event_SubEventList = \
            SubEvent.objects.filter(event=requestedEvent).order_by('start_date_and_time'
                )  # List of sub-events under

                                                                                                             # requestedEvent

        happenings.append((requestedEvent, Event_SubEventList))
        return render_to_response('dtvpicker/SummaryPages/CoordDTVSummary_ByEvent.html'
                                  , locals(),
                                  context_instance=RequestContext(request))


@login_required
def dtvSummaryByVenue(request):
    """
    Displays a summary of the DTV details of all events sorted by venue.
    Available to Cores only.
    Displays summary of all sub-events with their date-time-venue (dtv).
    """

    try:
        currentUserProfile = request.user.get_profile()
    except:

        # If the user's profile is not available

        return HttpResponse("Sorry. %s's user profile is not available."
                             % request.user.username)

    if currentUserProfile.is_core:

        requestedVenueList = []
        venues = VENUE_CHOICES
        for (venue_code, venue_name) in venues:
            requestedVenueList.append(venue_code)

        happeningsByVenue = []  # happenings is a list of tuples where

                               # the tuple structure is:
                               # (Venue, [Sub-events happening at Venue])

        enablePDFPrinting = PDFGenAllowed()  # Passed to the template to activate the PDF generation link.

        for requestedVenue in requestedVenueList:
            Venue_SubEventList = \
                SubEvent.objects.filter(venue=requestedVenue).order_by('start_date_and_time'
                    )  # List of sub-events under

                                                                                                                 # requestedVenue

            if Venue_SubEventList:
                happeningsByVenue.append((requestedVenue,
                        Venue_SubEventList))

        return render_to_response('dtvpicker/SummaryPages/CoreDTVSummary_ByVenue.html'
                                  , locals(),
                                  context_instance=RequestContext(request))

    return HttpResponseForbidden('This page can be accessed by Cores only. Please login with proper authentication to proceed.'
                                 )


@login_required
def dtvSummaryByDate(request):
    """
    Displays a summary of the DTV details of all events sorted by start date.
    Available to Cores only.
    Displays summary of all events and sub-events with their date-time-venue (dtv).
    """

    try:
        currentUserProfile = request.user.get_profile()
    except:

        # If the user's profile is not available

        return HttpResponse("Sorry. %s's user profile is not available."
                             % request.user.username)

    if currentUserProfile.is_core:

        requestedDateList = []
        subEventList = \
            SubEvent.objects.all().order_by('start_date_and_time')  # List of all sub-events
        for subEvent in subEventList:
            if subEvent.start_date_and_time.date() \
                not in requestedDateList:
                requestedDateList.append(subEvent.start_date_and_time.date())

        happeningsByDate = []  # happenings is a list of tuples where

                               # the tuple structure is:
                               # (Date, [Sub-events starting on Date])

        enablePDFPrinting = PDFGenAllowed()  # Passed to the template to activate the PDF generation link.

        for requestedDate in requestedDateList:
            Date_SubEventList = \
                SubEvent.objects.filter(start_date_and_time__startswith=requestedDate).order_by('start_date_and_time'
                    )

            # List of sub-events hapenning on requestedDate
            # For the contains part see:
            # http://stackoverflow.com/questions/1317714/how-can-i-filter-a-date-of-a-datetimefield-in-django

            happeningsByDate.append((requestedDate, Date_SubEventList))

        return render_to_response('dtvpicker/SummaryPages/CoreDTVSummary_ByDate.html'
                                  , locals(),
                                  context_instance=RequestContext(request))

    return HttpResponseForbidden('This page can be accessed by Cores only. Please login with proper authentication to proceed.'
                                 )
