from django.http import *
from django.template import *
from django.shortcuts import *
from django.contrib import *
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.contrib import *
from django.contrib.auth.models import User
from events.models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist

# reportlab imports are for pdf generation
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import getFont, getAscentDescent

import os
import datetime
# Create your views here.
    
@login_required
def dtvSummary(request):
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
        return HttpResponse("Sorry. %s's user profile is not available." % request.user.username)
    
    if currentUserProfile.is_core:

        # A core is allowed to see all events
        requestedEventList = Event.objects.all()
        happenings = [] # happenings is a list of tuples where
                        # the tuple structure is:
                        # (Event, [Sub-events under Event])

        enablePDFPrinting = True # Passed to the template to activate the PDF generation link.

        for requestedEvent in requestedEventList:
            Event_SubEventList = SubEvent.objects.filter(event = requestedEvent).order_by('start_date_and_time') # List of sub-events under
                                                                                                                 # requestedEvent
            happenings.append((requestedEvent, Event_SubEventList))
            
            if requestedEvent.lock_status != 'locked':
                # DTV PDF Printing is enabled only when all events are locked.
                # If even one is unlocked, the PDF generation should not be allowed.
                enablePDFPrinting = False

        return render_to_response("events/CoreDTVSummary.html", locals(), context_instance = RequestContext(request))
        
    else:

        # A coord can see only the events for which he is coord
        requestedEvent = request.user.get_profile().is_coord_of
        happenings = [] # happenings is a list of tuples where
                        # the tuple structure is:
                        # (Event, [Sub-events under Event])
        Event_SubEventList = SubEvent.objects.filter(event = requestedEvent).order_by('start_date_and_time') # List of sub-events under
                                                                                                             # requestedEvent
        happenings.append((requestedEvent, Event_SubEventList))
        return render_to_response("events/CoordDTVSummary.html", locals(), context_instance = RequestContext(request))
    
def PDFGenAllowed():
    """
    Checks if PDF Generation is allowed.
    Returns True if it is and False if not.
    PDF Generation is allowed if all events are locked.
    """
    eventList = Event.objects.all()
    
    for event in eventList:
        if event.lock_status != 'locked':
            return False
    return True
    
def PDFSetFont(pdf, font_name, font_size):
    """
    Sets the font and returns the lineheight.
    """
    pdf.setFont(font_name, font_size)
    ascent, descent = getAscentDescent(font_name, font_size)
    return (ascent - descent)  # Returns line height
    
    
def initNewPDFPage(pdf, doc_title, page_no, (pageWidth, pageHeight)):
    """
    Paints the headers on every new page of the PDF document.
    Also returns the coordinates (x, y) where the last painting operation happened.
    """
    y = pageHeight
    
    # Leave a margin of one cm at the top
    y = pageHeight - cm
    
    # Set font for 'SHAASTRA 2013'
    lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

    # SHAASTRA 2013 in centre
    pdf.drawCentredString(pageWidth/2, y, 'SHAASTRA 2013')
    y -= (lineheight + cm)
    
    # Set font for Document Title
    lineheight = PDFSetFont(pdf, 'Times-Roman', 12)
    
    # Document Title in next line, centre aligned
    pdf.drawCentredString(pageWidth/2, y, doc_title)
    
    # Set font for Document Title
    PDFSetFont(pdf, 'Times-Roman', 8)

    # Page number in same line, right aligned
    pdf.drawRightString(pageWidth - cm, y, '#%d' % page_no)
    
    y -= (lineheight + cm)

    return y
    

@login_required
def dtvSummary_PDF(request):
    """
    Generates and returns a PDF containing the DTV Summary (by event).
    Accessible by cores only.
    """
    try:
        currentUserProfile = request.user.get_profile()
    except:
        # If the user's profile is not available
        return HttpResponse("Sorry. %s's user profile is not available." % request.user.username)
    
    if not currentUserProfile.is_core:
        return HttpResponseForbidden("Sorry. You do not have the required permissions to view this page.")
        
    if not PDFGenAllowed():
        return HttpResponse('The PDF cannot be generated until all events are locked.')
    
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=DTVSummary_byEvent.pdf'
    
    # Create the PDF object, using the response object as its "file."
    pdf = canvas.Canvas(response, pagesize = A4)
    
    # Define the title of the document as printed in the document header.
    doc_title = 'DTV Summary (By Event)'

    # Get the width and height of the page.
    A4Width, A4Height = A4
    
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
        Event_SubEventList = SubEvent.objects.filter(event = requestedEvent).order_by('start_date_and_time') # List of sub-events under
                                                                                                             # requestedEvent
        # Construct the table data
        tableData = [ ['Sub-Event', 'Venue', 'Start Date', 'Start Time', 'End Date', 'End Time', 'Duration', ], ]
        for subevent in Event_SubEventList:
            tableData.append([subevent.title, 
                              subevent.venue, 
                              subevent.start_date_and_time.date(), 
                              subevent.start_date_and_time.time(),
                              subevent.end_date_and_time.date(),
                              subevent.end_date_and_time.time(),
                              subevent.end_date_and_time - subevent.start_date_and_time, ])
        t = Table(tableData, repeatRows = 1)
        
        # Set the table style
        tableStyle = TableStyle([('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
                                 ('FONTSIZE', (0,0), (-1,-1), 12),
                                 ('ALIGN', (0,0), (-1,-1), 'CENTRE'),
                                 ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                                 ('GRID', (0,0), (-1,-1), 1, colors.black),
                                 ])
        t.setStyle(tableStyle)
        
        # Set the font for the event title
        lineheight = PDFSetFont(pdf, 'Times-Roman', 14)

        availableWidth = A4Width - 2*cm  # Leaving margins of 1 cm on both sides
        availableHeight = y - (lineheight + 0.2*cm)  # (lineheight + 0.2*cm) subtracted to include title height
        tableWidth, tableHeight = t.wrap(availableWidth, availableHeight) # find required space
        if tableHeight <= availableHeight:

            # Paint the event title
            pdf.drawString(x, y, requestedEvent.title)
            # Add spacing
            y -= (lineheight + 0.2*cm)

            t.drawOn(pdf, x, y-tableHeight)
            y -= (tableHeight + cm)  # Find next position for painting
        else:
            pdf.showPage()
            pageNo += 1
            y = initNewPDFPage(pdf, doc_title, pageNo, A4)

            # Set the font for the event title
            lineheight = PDFSetFont(pdf, 'Times-Roman', 14)            
            # Paint the event title
            pdf.drawString(x, y, requestedEvent.title)
            # Add spacing
            y -= (lineheight + 0.2*cm)

            availableHeight = y - (lineheight + 0.2*cm)  # (lineheight + 0.2*cm) subtracted to include title height
            tableWidth, tableHeight = t.wrap(availableWidth, availableHeight)

            t.drawOn(pdf, x, y-tableHeight)
            y -= (tableHeight + cm)  # Find next position for painting

    pdf.showPage()
    pdf.save()
    
    return response    
    
class BaseView(object):
    # parent class. classes below inherit this
    def __call__(self, request, **kwargs):
        # handles request and dispatches the corresponding handler based on the type of request (GET/POST)
        method = request.META['REQUEST_METHOD'].upper()
        handler = getattr(self, 'handle_%s' %method, None)
        
        if handler is None:
            methods = []
            for x in dir(self):
                if x.startswith('handle_'):
                    methods.append(x[7:])
            return HttpResponseNotAllowed(methods)
            
        return handler(request, **kwargs)
        
    def get_tabs(self,event):
        # returns list of all tabs of a particular event
        try:
            return event.tab_set.all()
        except:
            raise Http404()
            
    def get_files(self, tab):
        # returns list of all files of a particular tab
        try:
            return tab.tabfile_set.all()
        except:
            print 'here too'
            raise Http404()
        
    def get_template(self, file_name):
        #this is used to get templates from the path /.../shaastra/events/templates/events/ajax      (*in my case)
        #note - a separate folder for ajax templates.
        #this function opens files (*.html) and returns them as python string.
        filepath = os.path.join(settings.AJAX_TEMPLATE_DIR, file_name)
        f = open(filepath, mode='r')
        return f.read()

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
        # TODO(Anant, anant.girdhar@gmail.com): Instead of copying the code, it would be better if we override BaseView.__call__
        #                                       and add the necessary lines for authentication.
        
        # Copied code from BaseView.__call__
        # Overriding BaseView.__call__ to check authentication.

        if self.userAuthentication(request, **kwargs) == False:
            return HttpResponseForbidden()
        method = request.META['REQUEST_METHOD'].upper()
        handler = getattr(self, 'handle_%s' %method, None)
        
        if handler is None:
            methods = []
            for x in dir(self):
                if x.startswith('handle_'):
                    methods.append(x[7:])
            return HttpResponseNotAllowed(methods)    
        return handler(request, **kwargs)
        
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
            if request.user.get_profile().is_coord_of != Event.objects.get(title = kwargs['event']):
                return False  # If the coord is not coord of the requested event
            return True
        except:
            raise Http404
        
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
            subeventRequested = SubEvent.objects.filter(event = eventRequested)
            subeventRequested = subeventRequested.get(title = subevent_name)
        except:
            raise Http404  # If the sub-event requested is not found in the database
        
        return subeventRequested
        
    def getEvent(self, event_name):
        """
        Gets the event referenced by the url from the database.
        Returns an instance of Event having title as given in the url.
        If no object is found, raises Http404.
        If the event is locked (ie. no editing is possible), raises Http404.
        """
        try:  # To get the event
            eventRequested = Event.objects.get(title = event_name)
        except:
            raise Http404  # If the event requested is not found in the database
            
        if eventRequested.lock_status == 'locked':
            raise Http404
        
        return eventRequested
        
    def updateEventLockStatus(self, eventToUpdate):

        subEventList = SubEvent.objects.filter(event = eventToUpdate)

        newLockStatus = 'cannot_be_locked'
        
        if subEventList:
            newLockStatus = 'not_locked'
            for subevent in subEventList:
                if not (subevent.start_date_and_time and subevent.end_date_and_time and subevent.venue):
                    newLockStatus = 'cannot_be_locked'
                    break
                
        eventToUpdate.lock_status = newLockStatus
        eventToUpdate.unlock_reason = ''
        eventToUpdate.save()
    
    def updateAndSaveSubEvent(self, subEventObject, newSubEventData):
        subEventObject.title = newSubEventData['title']
        subEventObject.start_date_and_time = newSubEventData['start_date_and_time']
        subEventObject.end_date_and_time = newSubEventData['end_date_and_time']
        subEventObject.venue = newSubEventData['venue']
        subEventObject.event = newSubEventData['event']
        subEventObject.last_modified = datetime.datetime.now() # Is handled by SubEvent.clean().
                                                               # Done here just to make sure.
        subEventObject.save()
        self.updateEventLockStatus(subEventObject.event)
        
class SubEventAdd(SubEventAddEditDeleteABC):
    """
    Adding a sub-event to the database.
    Permissions: Coords only.
    Access: Only own events.
    """
    
    def handle_GET(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()
        
        eventRequested = self.getEvent(kwargs['event'])
        
        form = SubEventForm(initial = {'event' : '%d' % eventRequested.id, })
        form_mode = 'add'  # For re-using the template (only difference: add/edit button)
        return render_to_response ('events/addEditSubEvent.html', locals(), context_instance = RequestContext(request))
    
    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()
        
        eventRequested = self.getEvent(kwargs['event'])
        
        formDataReceived = request.POST.copy()
        formDataReceived['event'] = eventRequested.id
        
        form = SubEventForm(formDataReceived)
        
        if form.is_valid():
            newSubEventData = form.cleaned_data
            newSubEvent = SubEvent()
            self.updateAndSaveSubEvent(newSubEvent, newSubEventData)
            return HttpResponseRedirect('/events/DTVSummary/')
        
        form_mode = 'add'  # For re-using the template (only difference: add/edit button)
        return render_to_response ('events/addEditSubEvent.html', locals(), context_instance = RequestContext(request))
        
class SubEventEdit(SubEventAddEditDeleteABC):
    """
    Editing details of sub-event.
    Permissions: Coords only.
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
                                       'venue'                  : subeventRequested.venue,
                                       'event'                  : eventRequested, })
        form_mode = 'edit'  # For re-using the template (only difference: add/edit button)
        return render_to_response ('events/addEditSubEvent.html', locals(), context_instance = RequestContext(request))
    
    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        eventRequested = self.getEvent(kwargs['event'])
        subeventRequested = self.getSubEvent(kwargs['subevent'], kwargs['event'])
            
        formDataReceived = request.POST.copy()

        form = SubEventForm(formDataReceived, instance = self.getSubEvent(kwargs['subevent'], kwargs['event']))
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
            newSubEvent = subeventRequested  # We want to update this SubEvent instance
            self.updateAndSaveSubEvent(newSubEvent, newSubEventData)
            return HttpResponseRedirect('/events/DTVSummary/')

        form_mode = 'edit'  # For re-using the template (only difference: add/edit button)
        return render_to_response ('events/addEditSubEvent.html', locals(), context_instance = RequestContext(request))
        
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
        subeventRequested = self.getSubEvent(kwargs['subevent'], kwargs['event'])

        return render_to_response ('events/deleteSubEvent.html', locals(), context_instance = RequestContext(request))
    
    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()

        subeventRequested = self.getSubEvent(kwargs['subevent'], kwargs['event'])
        subeventRequested.delete()
        self.updateEventLockStatus(self.getEvent(kwargs['event']))
        return HttpResponseRedirect('/events/DTVSummary/')
        
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
            eventRequested = Event.objects.get(title = kwargs['event'])
        except:
            raise Http404  # If the event requested is not found in the database

        if eventRequested.lock_status != 'not_locked':
            raise Http404
            
        subEventList = SubEvent.objects.filter(event = eventRequested).order_by('start_date_and_time')
        
        return render_to_response ('events/lockEvent.html', locals(), context_instance = RequestContext(request))
        
    def handle_POST(self, request, **kwargs):
        if self.permissionsGranted(request, **kwargs) == False:
            return HttpResponseForbidden()
            
        try:  # To get the event
            eventRequested = Event.objects.get(title = kwargs['event'])
        except:
            raise Http404  # If the event requested is not found in the database

        if eventRequested.lock_status != 'not_locked':
            raise Http404
            
        eventRequested.lock_status = 'locked'
        eventRequested.unlock_reason = ''
        eventRequested.save()
            
        return HttpResponseRedirect('/events/DTVSummary')
        
class UnlockEvent(CoreProtectedView):
    """
    Includes the views to Unlock an event.
    An event can be unlocked only when it is locked
    """
    def handle_GET(self, request, **kwargs):
        try:  # To get the event
            eventRequested = Event.objects.get(title = kwargs['event'])
        except:
            raise Http404  # If the event requested is not found in the database
            
        if eventRequested.lock_status != 'locked':
            raise Http404
            
        unlockForm = EventUnlockForm()
        
        subEventList = SubEvent.objects.filter(event = eventRequested).order_by('start_date_and_time')        
        
        return render_to_response ('events/unlockEvent.html', locals(), context_instance = RequestContext(request))
        
    def handle_POST(self, request, **kwargs):
        try:  # To get the event
            eventRequested = Event.objects.get(title = kwargs['event'])
        except:
            raise Http404  # If the event requested is not found in the database
            
        if eventRequested.lock_status != 'locked':
            raise Http404
            
        unlockForm = EventUnlockForm(request.POST)
        
        if unlockForm.is_valid():
            submittedData = unlockForm.cleaned_data
            eventRequested.lock_status = 'unlocked_by_core'
            eventRequested.unlock_reason = submittedData['unlock_reason']
            eventRequested.save()
            
            return HttpResponseRedirect('/events/DTVSummary')
            
        return render_to_response ('events/unlockEvent.html', locals(), context_instance = RequestContext(request))
        
class CoordDashboard(CoordProtectedView):
    """
    displays the coord dashboard depending on the logged in coords event
    """
    def handle_GET(self, request, **kwargs):
        event = request.user.get_profile().is_coord_of
        tabs = self.get_tabs(event)
        return render_to_response('events/dashboard.html', locals(), context_instance = RequestContext(request))
        
class TabFileSubmit(CoordProtectedView):
    """
    ajax file uploads are directed to this view
    """
    def handle_POST(self, request, **kwargs):
        from django.conf import settings
        # These were the headers set by the function File() to pass additional data. 
        filename = request.META['HTTP_X_FILE_NAME']
        display_name = request.META['HTTP_X_NAME']
        tab_id = request.META['HTTP_X_TAB_ID']
        
        tab = Tab.objects.get(id = tab_id)
        direc = os.path.join(settings.PROJECT_DIR + settings.MEDIA_URL, 'events', str(tab.event.id), tab._meta.object_name, str(tab.id))
        # note that event and tab IDs and not their titles have been used to create folders so that renaming does not affect the folders
        if not os.path.exists(direc):
            os.makedirs(direc)
        path = os.path.join(direc, filename)
        a = TabFile.objects.get_or_create(tab_file = path)
        # get_or_create returns a tuple whose second element is a boolean which is True if it is creating a new object.
        # the first element is the object that has been created/found.
        if a[1]:
            a[0].url = os.path.join(settings.MEDIA_URL, 'events', str(tab.event.id), tab._meta.object_name, str(tab.id), filename)
            f = open(path, 'w')
            with f as dest:
                req = request
                # Right now the file comes as raw input (in form of binary strings). Unfortunately, this is the only way I know that will make ajax work with file uploads.
                foo = req.read( 1024 )
                while foo:
                    dest.write( foo )
                    foo = req.read( 1024 )
        a[0].title = display_name
        a[0].tab = tab
        a[0].save()
        file_list = self.get_files(tab)

        template = self.get_template('file_list.html')
        t = Template(template).render(RequestContext(request, locals()))
        # the ajax function File() assigns this as the innerHTML of a div after the request has been completed.
        return HttpResponse(t)
        
        
