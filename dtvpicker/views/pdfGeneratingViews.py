#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the views that generate the PDFs for the DTV Picker feature."""

from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from dtvpicker.models import SubEvent
from events.models import Event

# reportlab imports are for pdf generation

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import getFont, getAscentDescent

from timedeltaFormattingClass import strfdelta
from miscFunctions import PDFGenAllowed
from dtvpicker.VenueChoices import VENUE_CHOICES


def PDFSetFont(pdf, font_name, font_size):
    """
    Sets the font and returns the lineheight.
    """

    pdf.setFont(font_name, font_size)
    (ascent, descent) = getAscentDescent(font_name, font_size)
    return ascent - descent  # Returns line height


def initNewPDFPage(
    pdf,
    doc_title,
    page_no,
    (pageWidth, pageHeight),
    ):
    """
    Paints the headers on every new page of the PDF document.
    Also returns the coordinates (x, y) where the last painting operation happened.
    """

    y = pageHeight

    # Leave a margin of one cm at the top

    y = pageHeight - cm

    # Set font for 'SHAASTRA 2013'

    lineheight = PDFSetFont(pdf, 'Times-Roman', 18)

    # SHAASTRA 2013 in centre

    pdf.drawCentredString(pageWidth / 2, y, 'SHAASTRA 2013')
    y -= lineheight + cm

    # Set font for Document Title

    lineheight = PDFSetFont(pdf, 'Times-Roman', 16)

    # Document Title in next line, centre aligned

    pdf.drawCentredString(pageWidth / 2, y, doc_title)

    # Set font for Document Title

    PDFSetFont(pdf, 'Times-Roman', 9)

    # Page number in same line, right aligned

    pdf.drawRightString(pageWidth - cm, y, '#%d' % page_no)

    y -= lineheight + cm

    return y


@login_required
def dtvSummaryByVenue_PDF(request):
    """
    Generates and returns a PDF containing the DTV Summary (by venue).
    Accessible by cores only.
    """

    try:
        currentUserProfile = request.user.get_profile()
    except:

        # If the user's profile is not available

        return HttpResponse("Sorry. %s's user profile is not available."
                             % request.user.username)

    if not currentUserProfile.is_core:
        return HttpResponseForbidden('Sorry. You do not have the required permissions to view this page.'
                )

    if not PDFGenAllowed():
        return HttpResponse('The PDF cannot be generated until all events are locked.'
                            )

    # Create the HttpResponse object with the appropriate PDF headers.

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = \
        'attachment; filename=DTVSummary-ByVenue.pdf'

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(response, pagesize=A4)

    # Define the title of the document as printed in the document header.

    doc_title = 'DTV Summary (By Venue)'

    # Get the width and height of the page.

    (A4Width, A4Height) = A4

    # Page number

    pageNo = 1

    # Paint the headers and get the coordinates

    y = initNewPDFPage(pdf, doc_title, pageNo, A4)

    # Setting x to be a cm from the left edge

    x = cm

    # Print DTV Summary in PDF

    # Get all venues

    requestedVenueList = []
    venues = VENUE_CHOICES
    for (venue_code, venue_name) in venues:
        requestedVenueList.append(venue_code)

    # Sort venue list in alphabetical order

    requestedVenueList.sort()

    # List to hold venues where no events are happening

    venuesWithNoEvents = []

    # Will be printed at the end of the document

    for requestedVenue in requestedVenueList:

        # Get all sub-events happening at requestedVenue

        Venue_SubEventList = \
            SubEvent.objects.filter(venue=requestedVenue).order_by('start_date_and_time'
                )  # List of sub-events happening at

                                                                                                             # requestedVenue

        if not Venue_SubEventList:  # If there are no events happening at the venue
            venuesWithNoEvents.append(requestedVenue)
            continue

        # Construct the table data

        tableData = [[
            'Event',
            'Sub-Event',
            'Start Date',
            'Start Time',
            'End Date',
            'End Time',
            'Duration',
            ]]
        for subevent in Venue_SubEventList:
            tableData.append([
                subevent.event.title,
                subevent.title,
                subevent.start_date_and_time.date().strftime('%d-%b-%y'
                        ),
                subevent.start_date_and_time.time().strftime('%I:%M %p'
                        ),
                subevent.end_date_and_time.date().strftime('%d-%b-%y'),
                subevent.end_date_and_time.time().strftime('%I:%M %p'),
                strfdelta(subevent.end_date_and_time
                          - subevent.start_date_and_time, '%H:%M'),
                ])

                              # For strftime documentation and the format specifiers see
                              # http://docs.python.org/library/datetime.html#strftime-strptime-behavior

        t = Table(tableData, repeatRows=1)

        # Set the table style

        tableStyle = TableStyle([  # Font style for Table Data
                                   # Font style for Table Header
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
        t.setStyle(tableStyle)

        # Set the font for the venue code

        lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

        availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
        availableHeight = y - (lineheight + 0.2 * cm)  # (lineheight + 0.2*cm) subtracted to include title height
        (tableWidth, tableHeight) = t.wrap(availableWidth,
                availableHeight)  # find required space
        if tableHeight <= availableHeight:

            # Paint the venue code

            pdf.drawString(x, y, requestedVenue)

            # Add spacing

            y -= lineheight + 0.2 * cm

            t.drawOn(pdf, x, y - tableHeight)
            y -= tableHeight + cm  # Find next position for painting
        else:
            pdf.showPage()
            pageNo += 1
            y = initNewPDFPage(pdf, doc_title, pageNo, A4)

            # Set the font for the venue code

            lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

            # Paint the venue code

            pdf.drawString(x, y, requestedVenue)

            # Add spacing

            y -= lineheight + 0.2 * cm

            availableHeight = y - (lineheight + 0.2 * cm)  # (lineheight + 0.2*cm) subtracted to include title height
            (tableWidth, tableHeight) = t.wrap(availableWidth,
                    availableHeight)

            t.drawOn(pdf, x, y - tableHeight)
            y -= tableHeight + cm  # Find next position for painting

    y -= cm

    if venuesWithNoEvents:

        # Paint all the venues that have no events happening

        # Set the font for all following text

        lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

        # Calculate the space requried for all following text

        numberOfVenues = venuesWithNoEvents.__len__()

        availableHeight = y

        spaceRequired = lineheight + cm / 2 + numberOfVenues \
            * lineheight + (numberOfVenues - 1) * (cm / 3)

        # Explanation for the above calculation:
        # lineheight                        -->  for message that says 'There are no events happening at the following venues:'
        # (cm / 2)                          -->  for the space after the message
        # (numberOfVenues * lineheight)     -->  for each venue (one venue per line)
        # ((numberOfVenues - 1) * (cm / 3)) -->  for the space after each venue (except the last)

        if spaceRequired > availableHeight:

            # Paint on next page
            # If there is space available on the same page, this will not happen and the painting will continue on the same page

            pdf.showPage()
            pageNo += 1
            y = initNewPDFPage(pdf, doc_title, pageNo, A4)

            # Set the font for all following text

            lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

        pdf.drawString(x, y,
                       'There are no events happening at the following venues:'
                       )
        y -= lineheight + cm / 2

        for requestedVenue in venuesWithNoEvents:

            # Check if the next event can be painted on the same page, else change the page

            availableHeight = y
            if availableHeight < lineheight:
                pdf.showPage()
                pageNo += 1
                y = initNewPDFPage(pdf, doc_title, pageNo, A4)

                # Set the font for all following text

                lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

            pdf.drawString(x, y, requestedVenue)
            y -= lineheight + cm / 3

    pdf.showPage()
    pdf.save()

    return response


@login_required
def dtvSummaryByDate_PDF(request):
    """
    Generates and returns a PDF containing the DTV Summary (by date).
    Accessible by cores only.
    """

    try:
        currentUserProfile = request.user.get_profile()
    except:

        # If the user's profile is not available

        return HttpResponse("Sorry. %s's user profile is not available."
                             % request.user.username)

    if not currentUserProfile.is_core:
        return HttpResponseForbidden('Sorry. You do not have the required permissions to view this page.'
                )

    if not PDFGenAllowed():
        return HttpResponse('The PDF cannot be generated until all events are locked.'
                            )

    # Create the HttpResponse object with the appropriate PDF headers.

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = \
        'attachment; filename=DTVSummary-ByDate.pdf'

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(response, pagesize=A4)

    # Define the title of the document as printed in the document header.

    doc_title = 'DTV Summary (By Date)'

    # Get the width and height of the page.

    (A4Width, A4Height) = A4

    # Page number

    pageNo = 1

    # Paint the headers and get the coordinates

    y = initNewPDFPage(pdf, doc_title, pageNo, A4)

    # Setting x to be a cm from the left edge

    x = cm

    # Print DTV Summary in PDF

    # Get all dates

    requestedDateList = []
    subEventList = SubEvent.objects.all().order_by('start_date_and_time'
            )  # List of all sub-events
    for subEvent in subEventList:
        if subEvent.start_date_and_time.date() not in requestedDateList:
            requestedDateList.append(subEvent.start_date_and_time.date())

    for requestedDate in requestedDateList:

        # Get all sub-events happening at requestedVenue

        Date_SubEventList = \
            SubEvent.objects.filter(start_date_and_time__startswith=requestedDate).order_by('start_date_and_time'
                )

            # List of sub-events hapenning on requestedDate
            # For the contains part see:
            # http://stackoverflow.com/questions/1317714/how-can-i-filter-a-date-of-a-datetimefield-in-django

        # Construct the table data

        tableData = [[
            'Event',
            'Sub-Event',
            'Start Time',
            'End Date',
            'End Time',
            'Venue',
            'Duration',
            ]]
        for subevent in Date_SubEventList:
            tableData.append([subevent.event.title, 
                              subevent.title, 
                              subevent.start_date_and_time.time().strftime("%I:%M %p"),
                              subevent.end_date_and_time.date().strftime("%d-%b-%y"),
                              subevent.end_date_and_time.time().strftime("%I:%M %p"),
                              subevent.display_venue(),
                              strfdelta(subevent.end_date_and_time - subevent.start_date_and_time, "%H:%M"), ])
                              # For strftime documentation and the format specifiers see
                              # http://docs.python.org/library/datetime.html#strftime-strptime-behavior

        t = Table(tableData, repeatRows=1)

        # Set the table style

        tableStyle = TableStyle([  # Font style for Table Data
                                   # Font style for Table Header
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
        t.setStyle(tableStyle)

        # Set the font for the date

        lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

        availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
        availableHeight = y - (lineheight + 0.2 * cm)  # (lineheight + 0.2*cm) subtracted to include title height
        (tableWidth, tableHeight) = t.wrap(availableWidth,
                availableHeight)  # find required space
        if tableHeight <= availableHeight:

            # Paint the date

            pdf.drawString(x, y, requestedDate.strftime('%A %d %B %Y'))

            # Add spacing

            y -= lineheight + 0.2 * cm

            t.drawOn(pdf, x, y - tableHeight)
            y -= tableHeight + cm  # Find next position for painting
        else:
            pdf.showPage()
            pageNo += 1
            y = initNewPDFPage(pdf, doc_title, pageNo, A4)

            # Set the font for the date

            lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

            # Paint the date
            pdf.drawString(x, y, requestedDate.strftime("%A %d %B %Y"))
            # Add spacing

            y -= lineheight + 0.2 * cm

            availableHeight = y - (lineheight + 0.2 * cm)  # (lineheight + 0.2*cm) subtracted to include title height
            (tableWidth, tableHeight) = t.wrap(availableWidth,
                    availableHeight)

            t.drawOn(pdf, x, y - tableHeight)
            y -= tableHeight + cm  # Find next position for painting

    pdf.showPage()
    pdf.save()

    return response


@login_required
def dtvSummaryByEvent_PDF(request):
    """
    Generates and returns a PDF containing the DTV Summary (by event).
    Accessible by cores only.
    """

    try:
        currentUserProfile = request.user.get_profile()
    except:

        # If the user's profile is not available

        return HttpResponse("Sorry. %s's user profile is not available."
                             % request.user.username)

    if not currentUserProfile.is_core:
        return HttpResponseForbidden('Sorry. You do not have the required permissions to view this page.'
                )

    if not PDFGenAllowed():
        return HttpResponse('The PDF cannot be generated until all events are locked.'
                            )

    # Create the HttpResponse object with the appropriate PDF headers.

    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = \
        'attachment; filename=DTVSummary-ByEvent.pdf'

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(response, pagesize=A4)

    # Define the title of the document as printed in the document header.

    doc_title = 'DTV Summary (By Event)'

    # Get the width and height of the page.

    (A4Width, A4Height) = A4

    # Page number

    pageNo = 1

    # Paint the headers and get the coordinates

    y = initNewPDFPage(pdf, doc_title, pageNo, A4)

    # Setting x to be a cm from the left edge

    x = cm

    # Print DTV Summary in PDF

    # Get all events

    requestedEventList = Event.objects.all()

    for requestedEvent in requestedEventList:

        # Get all sub-events under the event

        Event_SubEventList = \
            SubEvent.objects.filter(event=requestedEvent).order_by('start_date_and_time'
                )  # List of sub-events under

                                                                                                             # requestedEvent
        # Construct the table data

        tableData = [[
            'Sub-Event',
            'Venue',
            'Start Date',
            'Start Time',
            'End Date',
            'End Time',
            'Duration',
            ]]
        for subevent in Event_SubEventList:
            tableData.append([subevent.title, 
                              subevent.display_venue(), 
                              subevent.start_date_and_time.date().strftime("%d-%b-%y"), 
                              subevent.start_date_and_time.time().strftime("%I:%M %p"),
                              subevent.end_date_and_time.date().strftime("%d-%b-%y"),
                              subevent.end_date_and_time.time().strftime("%I:%M %p"),
                              strfdelta(subevent.end_date_and_time - subevent.start_date_and_time, "%H:%M"), ])
                              # For strftime documentation and the format specifiers see
                              # http://docs.python.org/library/datetime.html#strftime-strptime-behavior

        t = Table(tableData, repeatRows=1)

        # Set the table style

        tableStyle = TableStyle([  # Font style for Table Data
                                   # Font style for Table Header
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
        t.setStyle(tableStyle)

        # Set the font for the event title

        lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

        availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
        availableHeight = y - (lineheight + 0.2 * cm)  # (lineheight + 0.2*cm) subtracted to include title height
        (tableWidth, tableHeight) = t.wrap(availableWidth,
                availableHeight)  # find required space
        if tableHeight <= availableHeight:

            # Paint the event title

            pdf.drawString(x, y, requestedEvent.title)

            # Add spacing

            y -= lineheight + 0.2 * cm

            t.drawOn(pdf, x, y - tableHeight)
            y -= tableHeight + cm  # Find next position for painting
        else:
            pdf.showPage()
            pageNo += 1
            y = initNewPDFPage(pdf, doc_title, pageNo, A4)

            # Set the font for the event title

            lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

            # Paint the event title

            pdf.drawString(x, y, requestedEvent.title)

            # Add spacing

            y -= lineheight + 0.2 * cm

            availableHeight = y - (lineheight + 0.2 * cm)  # (lineheight + 0.2*cm) subtracted to include title height
            (tableWidth, tableHeight) = t.wrap(availableWidth,
                    availableHeight)

            t.drawOn(pdf, x, y - tableHeight)
            y -= tableHeight + cm  # Find next position for painting

    pdf.showPage()
    pdf.save()

    return response
