from users.models import UserProfile, College, Team
from django.contrib.auth.models import User
from events.models import Event, EventSingularRegistration

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import getFont, getAscentDescent
from reportlab.platypus import Paragraph
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


def initNewPDFPage(pdf, page_title, page_no, (pageWidth, pageHeight),):
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

    # Set font for Page Title

    lineheight = PDFSetFont(pdf, 'Times-Roman', 16)

    # Page Title in next line, centre aligned

    pdf.drawCentredString(pageWidth / 2, y, page_title)

    # Set font for Document Title

    PDFSetFont(pdf, 'Times-Roman', 9)

    # Page number in same line, right aligned

    pdf.drawRightString(pageWidth - cm, y, '#%d' % page_no)

    y -= lineheight + cm

    return y
    
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
    
    
def printParticipantDetails(pdf, x, y, user, userProfile):

    lineheight = PDFSetFont(pdf, 'Times-Roman', 12)
    
    LINESPACE = 0.5 * cm
    
    pdf.drawString(x, y, 'Username: <b>%s</b> (UID: %d)' % (user.username, user.id))
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'Shaastra ID: %s' % userProfile.shaastra_id)
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'Name: %s %s' % (user.first_name, user.last_name))
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'Email: %s' % user.email)
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'Mobile No: %s' % userProfile.mobile_number)
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'College: %s' % userProfile.college.name)
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'Branch: %s' % userProfile.branch)
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'Gender: %s' % 'Male' if userProfile.gender == 'M' else 'Female')
    y -= lineheight + (LINESPACE)
    pdf.drawString(x, y, 'Age: %d' % userProfile.age)
    y -= lineheight + (LINESPACE)
    
    accountDetails = 'Username: <b>' + user.username + '</b> (UID: ' + user.id + ')<br/>'
    accountDetails += 'Shaastra ID: <b>%s</b><br/>' % userProfile.shaastra_id
    accountDetails += 'Name: %s <b>%s</b><br/>' % (user.first_name, user.last_name)
    accountDetails += 'Email: <b>%s</b><br/>' % user.email
    accountDetails += 'Mobile No: <b>%s</b><br/>' % userProfile.mobile_number
    accountDetails += 'College: <b>%s</b><br/>' % userProfile.college.name
    accountDetails += 'Branch: <b>%s</b><br/>' % userProfile.branch
    accountDetails += 'Gender: <b>%s</b><br/>' % 'Male' if userProfile.gender == 'M' else 'Female'
    accountDetails += 'Age: <b>%d</b><br/>' % userProfile.age
    
    y = paintParagraph(pdf, x, y, accountDetails)

    accountInstruction = 'Attention: <b>If you have not created an account on the Shaastra website</b>, an account has been created for you. Both your username and password are the local part of your email address. E.g. if your email is \'example@domain.com\', both your username and password will be \'example\' (without the quotes). <b>Please do update your profile on the Shaastra website to avoid any inconvenience later.</b>'
    
    y = paintParagraph(pdf, x, y, accountInstruction)

    return y
    
def printEventParticipationDetails(pdf, x, y, user, singularEventRegistrations, userTeams):

    # Construct the table data
    
    sNo = 1
    
    tableData = [ ['Serial No', 'Event Name', 'Team Name', 'Team ID'] ]
    
    for eventRegistration in singularEventRegistrations:
        tableData.append([sNo, eventRegistration.event.title, '', ''])
        sNo += 1
        
    for team in userTeams:
        tableData.append([sNo, team.event.title, team.name, team.id])
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
    
def printQMSInstructions(pdf, x, y):
    
    text = 'This is the QMS instructions. Please do not forget to load the qms instructions before sending this out to the recipients. This is the first paragraph. I hope you enjoyed reading this PDF. Please do not forget to read it till the very end.<br/><br/>This PDF is designed to let you know what exactly you have to do. It gives you details about you, which we hope you know better than us. It also contains some details that we hope that you now know. Please do keep this PDF for reference. It contains some very important identification numbers about you.<br/><br/>If you have any problems, do contact our QMS Team.<br/><br/><b>Shaastra 2013!</b>!!'''
    
    y = paintParagraph(pdf, x, y, text)

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

    # Page number

    pageNo = 1

    # Paint the headers and get the coordinates

    y = initNewPDFPage(pdf, page_title, pageNo, A4)

    # Setting x to be a cm from the left edge

    x = cm

    # Print Participant Details in PDF

    y = printParticipantDetails(pdf, x, y, user, userProfile)
    
    # Print Event Participation Details in PDF
    
    singularEventRegistrations = EventSingularRegistration.objects.filter(user = user)
    userTeams = user.joined_teams.all()
    
    if (not singularEventRegistrations) and (not userTeams):
        # The user is not registered for any event.
        return None
        y -= cm * 0.5
        pdf.drawString(x, y, 'You are not registered for any events this Shaastra')
    
    else:
        pdf.showPage()
        pageNo += 1
        page_title = 'PARTICIPATION DETAILS'
        y = initNewPDFPage(pdf, page_title, pageNo, A4)
        
        printEventParticipationDetails(pdf, x, y, user, singularEventRegistrations, userTeams)
    
    pdf.showPage()
    pageNo += 1
    page_title = 'QMS INSTRUCTIONS'
    y = initNewPDFPage(pdf, page_title, pageNo, A4)
    
    printQMSInstructions(pdf, x, y)
    
    pdf.showPage()
    pdf.save()

    response = buffer.getvalue()
    buffer.close()

    return response
    
def mailPDF(user, pdf):

    subject = 'Participation PDF'
    message = 'Dear participant,<br/>Please find attached the PDF that contains important information. Please go through it and address any querries to the QMS Team.<br/>Shaastra 2013 Team.<br/>'
    email = user.email
    email = 'swopstesting@gmail.com' #TODO: Remove this line for finale

    msg = EmailMultiAlternatives(subject, message, 'noreply@iitm.ac.in' , [email,])
    msg.content_subtype = "html"
    msg.attach('PP#%s.pdf' % user.get_profile().shaastra_id, pdf, 'application/pdf')
    msg.send()
    
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
    
def savePDF(pdf, sID):

    destination = open('/home/shaastra/hospi/participantPDFs/'+sID+'.pdf', 'wb+')
    destination.write(pdf)
    destination.close()
    print 'File '+sID+'.pdf saved.'

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
    userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(is_coord_of = None)
    for profile in participantProfilesWithShaastraIds:
        try:
            u = profile.user
        except:
            continue
        participants.append(u)

    participants = [User.objects.get(id = 1351)] #TODO: Remove this line for finale

    for participant in participants:
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        savePDF(pdf, participant.get_profile().shaastra_id)

