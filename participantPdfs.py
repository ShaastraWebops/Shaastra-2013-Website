from users.models import UserProfile, College, Team
from django.contrib.auth.models import User
from events.models import Event, EventSingularRegistration

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import getFont, getAscentDescent
from reportlab.platypus import Paragraph, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
    
import datetime

def PDFSetFont(pdf, font_name, font_size):
    """
    Sets the font and returns the lineheight.
    """

    pdf.setFont(font_name, font_size)
    (ascent, descent) = getAscentDescent(font_name, font_size)
    return ascent - descent  # Returns line height

def paintParagraph(pdf, x, y, text):

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name = 'paraStyle', fontSize = 12))
    
    p = Paragraph(text, styles['paraStyle'], None) # None for bullet type

    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (paraWidth, paraHeight) = p.wrap(availableWidth, availableHeight)  # find required space
    
    p.drawOn(pdf, x, y - paraHeight)
    
    y -= paraHeight + cm
    
    return y

def paintImage(pdf, x, y, im):

    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (imWidth, imHeight) = im.wrap(availableWidth, availableHeight)  # find required space
    
    im.drawOn(pdf, x, y - imHeight)
    
    x -= imWidth + cm
    y -= imHeight + cm
    
    return (x, y)

def initNewPDFPage(pdf, (pageWidth, pageHeight), shaastra_id, username):
    """
    Paints the headers on every new page of the PDF document.
    Also returns the coordinates (x, y) where the last painting operation happened.
    """

    y = pageHeight

    # Leave a margin of one cm at the top

    y = pageHeight - cm
    x = cm

    im = Image("/home/shaastra/hospi/participantPDFs/shaastralogo.jpg", width=3*inch, height=2*inch)
    im.hAlign = 'LEFT'
    
    (x, t) = paintImage(pdf, x, y, im)

    # Set font for Header
    lineheight = PDFSetFont(pdf, 'Times-Bold', 20)

    # Page number in same line, right aligned
    
    y = pageHeight-2*cm

    pdf.drawRightString(pageWidth - cm*1.5, y, '%s' % shaastra_id)

    y -= lineheight + cm
    
    lineheight = PDFSetFont(pdf, 'Times-Roman', 18)
    
    pdf.drawRightString(pageWidth - cm*1.5, y, '%s' % username)

    return t
    
def printParticipantDetails(pdf, x, y, user, userProfile):

    #accountDetails =  'Username:     <b>' + user.username + '</b> (UID: ' + str(user.id) + ')<br/><br/>'
    #accountDetails += 'Shaastra ID:  <b>%s</b><br/><br/>' % userProfile.shaastra_id
    accountDetails = ''
    if user.first_name and user.last_name:
        accountDetails +=  'Name:         <b>%s %s</b><br/><br/>' % (user.first_name, user.last_name)
    else:
        accountDetails +=  'Name:         <br/><br/>'
    accountDetails += 'Email:        <b>%s</b><br/><br/>' % user.email if user.email else ''
    accountDetails += 'Mobile No:    <b>%s</b><br/><br/>' % userProfile.mobile_number if userProfile.mobile_number else ''
    try:
        accountDetails += 'College:      <b>%s</b><br/><br/>' % userProfile.college.name
    except:
        accountDetails += 'College:      <b>%s</b><br/><br/>' % ''
    #accountDetails += 'College Roll: <b>%s</b><br/><br/>' % userProfile.college_roll
    try:
        accountDetails += 'City:         <b>%s</b><br/><br/>' % userProfile.college.city
    except:
        accountDetails += 'City:         <b>%s</b><br/><br/>' % ''
    try:
        accountDetails += 'State:        <b>%s</b><br/><br/>' % userProfile.college.state
    except:
        accountDetails += 'State:        <b>%s</b><br/><br/>' % ''
    accountDetails += 'Branch:       <b>%s</b><br/><br/>' % userProfile.branch if userProfile.branch else ''
    if userProfile.gender == 'M':
        accountDetails += 'Gender:       <b>%s</b><br/><br/>' % 'Male'
    elif userProfile.gender == 'F':
        accountDetails += 'Gender:       <b>%s</b><br/><br/>' % 'Female'
    else:
        accountDetails += 'Gender:       <b>%s</b><br/><br/>' % ''
    accountDetails += 'Age:          <b>%s</b><br/><br/>' % str(userProfile.age) if userProfile.age else ''

    if userProfile.want_accomodation:
        accountDetails += '<br/><b>Accomodation requested</b><br/><br/>'
    else:
        accountDetails += '<br/><b>Accomodation not requested</b><br/><br/>'
    
    y = paintParagraph(pdf, x, y, accountDetails)

    accountInstruction = 'Attention: <b>If you have not created an account on the Shaastra website</b>, an account has been created for you. Both your username and password are the local part of your email address. E.g. if your email is \'example@domain.com\', both your username and password will be \'example\' (without the quotes). <b>Please do update your profile on the Shaastra website to avoid any inconvenience later.</b>'
    
    y = paintParagraph(pdf, x, y, accountInstruction)
    
    qmsInstruction = '<para alignment="center"><font size=14><b>QMS Instructions</b></font>'
    
    y -= cm*0.7
    y = paintParagraph(pdf, x, y, qmsInstruction)
    
    qmsInstruction = '</para><para alignment="left"><br/><br/>1. Please carry a printout or an e-copy of this form.<br/><br/>2. Every participant must register for Shaastra at the <b>QMS Desk (KV Grounds) or the Hospitality Control Rooms (Mahanadi for boys, Sharavati for girls)</b> after reaching IIT Madras.<br/><br/>3. Upon paying a sum of INR 100, the participant would receive a <b>Shaastra Passport</b> (non transferable)<br/><br/>4. The Shaastra Passport will be your official entry to Shaastra allowing you to register at the <b>Event Venue</b> and participate for events.<br/><br/>5. For more information, please drop us a mail at qms@shaastra.org</para>'
    
    y += cm*0.7
    y = paintParagraph(pdf, x, y, qmsInstruction)

    return y
    
def printEventParticipationDetails(pdf, x, y, user, singularEventRegistrations, userTeams):

    lineheight = PDFSetFont(pdf, 'Times-Bold', 16)

    (A4Width, A4Height) = A4

    pdf.drawCentredString(A4Width/2, y, 'PARTICIPATION DETAILS')

    y -= lineheight + cm

    # Construct the table data
    
    sNo = 1
    
    tableData = [ ['Serial No', 'Event Name', 'Team Name', 'Team ID', 'Team Leader'] ]
    
    for eventRegistration in singularEventRegistrations:
        tableData.append([sNo, eventRegistration.event.title, '', ''])
        sNo += 1
        
    for team in userTeams:
        tableData.append([sNo, team.event.title, team.name, team.id, team.leader.get_profile().shaastra_id])
        sNo += 1
        
    t = Table(tableData, repeatRows=1)

    # Set the table style

    tableStyle = TableStyle([ ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'), # Font style for Table Data
                              ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'), # Font style for Table Header
                              ('FONTSIZE', (0, 0), (-1, -1), 12),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTRE'),
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ])
    t.setStyle(tableStyle)
    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (tableWidth, tableHeight) = t.wrap(availableWidth, availableHeight)  # find required space
    
    t.drawOn(pdf, x, y - tableHeight)
    
def generateParticipantPDF(user):

    userProfile = UserProfile.objects.get(user = user)
    
    # Create a buffer to store the contents of the PDF.
    # http://stackoverflow.com/questions/4378713/django-reportlab-pdf-generation-attached-to-an-email
    buffer = StringIO()

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Define the title of the document as printed in the document header.

    page_title = 'PARTICIPANT DETAILS'

    # Get the width and height of the page.

    (A4Width, A4Height) = A4

    # Paint the headers and get the coordinates

    y = initNewPDFPage(pdf, A4, userProfile.shaastra_id, userProfile.user.username)

    # Setting x to be a cm from the left edge

    x = cm

    # Print Participant Details in PDF

    y = printParticipantDetails(pdf, x, y, user, userProfile)
    
    # Print Event Participation Details in PDF
    
    singularEventRegistrations = EventSingularRegistration.objects.filter(user = user)
    userTeams = user.joined_teams.all()
    
    if (not singularEventRegistrations) and (not userTeams):
        # The user is not registered for any event.
        buffer.close()
        return None
        y -= cm * 0.5
        pdf.drawString(x, y, 'You are not registered for any events this Shaastra')
    
    else:
        pdf.showPage()
        y = initNewPDFPage(pdf, A4, userProfile.shaastra_id, userProfile.user.username)
        
        printEventParticipationDetails(pdf, x, y, user, singularEventRegistrations, userTeams)
    
    pdf.showPage()
    pdf.save()

    response = buffer.getvalue()
    buffer.close()

    return response
    
def mailPDF(user, pdf):

    subject = '[IMPORTANT] Registration Details, Shaastra 2013'
    message = 'Dear '
    if user.first_name and user.last_name:
        message += user.first_name.title() + ' ' + user.last_name.title()
    elif user.first_name:
        message += user.first_name.title()
    elif user.last_name:
        message += user.last_name.title()
    else:
        message += user.username
    
    message += ',<br/><br/>The attached PDF contains important information regarding your registration at Shaastra 2013.'
    message += ' Please bring <b>two printed copies</b> of this PDF with you. For any queries, please contact the QMS Team at qms@shaastra.org.<br/><br/>Team Shaastra 2013<br/>'
    email = user.email
    #email = 'swopstesting@gmail.com' #TODO: Remove this line for finale

    msg = EmailMultiAlternatives(subject, message, 'noreply@iitm.ac.in' , [email,])
    msg.content_subtype = "html"
    msg.attach('%s-registration-details.pdf' % user.username, pdf, 'application/pdf')
    #msg.send()
    print 'Mail sent to %s' % email
    
@login_required
def mailParticipantPDFs(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden('The participant mailer can only be accessed by superusers. You don\'t have enough permissions to continue.')
    
    participants = []
    userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(is_coord_of = None)
    for profile in participantProfilesWithShaastraIds:
        try:
            u = profile.user
        except:
            continue
        participants.append(u)
        
    participantsMailed = []
    
    participants = [User.objects.get(id = 5787)] #TODO: Remove this line for finale

    for participant in participants:
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        mailPDF(participant, pdf)
    
    return HttpResponse('Mails sent. Timestamp: %s' % str(datetime.datetime.now()))
    
def savePDF(pdf, user):

    destination = open('/home/shaastra/hospi/participantPDFs/'+user.username+'-registration-details.pdf', 'wb+')
    destination.write(pdf)
    destination.close()
    print 'File '+user.username+'-registration-details.pdf saved.'

@login_required
def generateParticipantPDFs(request):

    if not request.user.is_superuser:
        return HttpResponseForbidden('The participant mailer can only be accessed by superusers. You don\'t have enough permissions to continue.')
        
    participants = []
    userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(is_coord_of = None)
    for profile in participantProfilesWithShaastraIds:
        try:
            u = profile.user
        except:
            continue
        participants.append(u)

    participants = [User.objects.get(id = 5787)] #TODO: Remove this line for finale

    for participant in participants:
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        savePDF(pdf, participant.get_profile().shaastra_id)
    
    return HttpResponse('PDFs generated. Timestamp: %s' % str(datetime.datetime.now()))

def generatePDFs():

    participants = []
    numPDFsGenerated = 0
    userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(user__is_superuser = False)
    for profile in participantProfilesWithShaastraIds:
        try:
            u = profile.user
        except:
            continue
        participants.append(u)

    #participants = [User.objects.get(id = 1351)] #TODO: Remove this line for finale

    for participant in participants:
        print participant.id
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        savePDF(pdf, participant)
        mailPDF(participant, pdf)
        numPDFsGenerated += 1
        
    print '\n\nPDFs generated: %d' % numPDFsGenerated

