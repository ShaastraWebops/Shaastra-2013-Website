from users.models import UserProfile, College, Team
from django.contrib.auth.models import User
from events.models import Event, EventSingularRegistration
from prizes.models import BarcodeMap

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseForbidden, HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
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

def log(msg):

    destination = open('/home/shaastra/hospi/certis/log.txt', 'a')
    destination.write(str(msg))
    destination.write('\n')
    destination.close()
    print msg

def PDFSetFont(pdf, font_name, font_size):
    """
    Sets the font and returns the lineheight.
    """

    pdf.setFont(font_name, font_size)
    (ascent, descent) = getAscentDescent(font_name, font_size)
    return ascent - descent  # Returns line height

def paintImage(pdf, x, y, im):

    (A4Width, A4Height) = A4
    availableWidth = A4Width - 2 * cm  # Leaving margins of 1 cm on both sides
    availableHeight = y
    (imWidth, imHeight) = im.wrap(availableWidth, availableHeight)  # find required space
    
    im.drawOn(pdf, x, y - imHeight)
    
    x -= imWidth + cm
    y -= imHeight + cm
    
    return (x, y)
    
def constructName(user):
    name = ''
    if user.first_name or user.last_name:
        if user.first_name:
            name += user.first_name
        if user.last_name:
            if len(name) > 0:
                name += ' '
            name += user.last_name
        name = name.title()
    else:
        log('User %s (%d) does not have a first/last name.' % (user.username, user.id))
        name += user.username
    return name    

def generateCertificate(user):

    userProfile = UserProfile.objects.get(user = user)
    
    # Create a buffer to store the contents of the PDF.
    # http://stackoverflow.com/questions/4378713/django-reportlab-pdf-generation-attached-to-an-email
    buffer = StringIO()
    
    CS = (3508, 2480)  # Certificate [Page] Size
    #CS = landscape(A4)

    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(buffer, pagesize=CS)

    # Get the width and height of the page.

    (pageWidth, pageHeight) = CS
    
    y = pageHeight
    x = 0
    
    im = Image("/home/shaastra/hospi/certis/certback_final.jpg")
    im.hAlign = 'LEFT'
    
    paintImage(pdf, x, y, im)

    # Set font for Participant Name
    lineheight = PDFSetFont(pdf, 'Times-Bold', 105)
    x = (43.8 + (65.54/2))*cm
    y = 42.62*cm + lineheight
    name = constructName(user)
    pdf.drawCentredString(x, y, '%s' % name)

    pdf.showPage()
    pdf.save()

    response = buffer.getvalue()
    buffer.close()

    return response
    
def mailPDF(user, pdf):

    subject = 'Participation Certificate (Corrected), Shaastra 2013'
    message = 'PFA the <b>corrected</b> certificate. <br/><br/>Team Shaastra 2013<br/>'
    email = user.email
    #email = 'swopstesting@gmail.com' #TODO: Remove this line for finale

    msg = EmailMultiAlternatives(subject, message, 'noreply@iitm.ac.in' , [email,])
    msg.content_subtype = "html"
    msg.attach('%s-certificate.pdf' % user.get_profile().shaastra_id, pdf, 'application/pdf')
    msg.send()  #TODO: Uncomment this line for finale
    log('Mail sent to %s' % email)  #TODO: Uncomment this line for finale
    #log('NOT sent. Mail will go to %s' % email)  #TODO: Comment this line for finale
    
def savePDF(pdf, user):

    destination = open('/home/shaastra/hospi/certis/'+user.get_profile().shaastra_id+'-certificate.pdf', 'wb+')
    destination.write(pdf)
    destination.close()
    log('File '+user.get_profile().shaastra_id+'-certificate.pdf saved.')

def cookAndServeCertis():
    
    #return ('Comment this line to send the Participant PDFs.')
    
    log('\n\n**********  Now: %s  **********' % datetime.datetime.now())

    uids = []
    
    participants = []
    scannedBarcodes = BarcodeMap.objects.using('erp').all() #TODO Exclude non active users??
    for scan in scannedBarcodes:
        try:
            p = UserProfile.objects.get(shaastra_id = scan.shaastra_id)
        except:
            continue
        try:
            u = p.user
        except:
            continue
        participants.append(u)

    fileObj = open('/home/shaastra/hospi/certis/mailed.txt', 'r')
    log('\n\nOpened %s to get uids of all mailed participants.' % 'mailed.txt')
    for line in fileObj:
        t = line[:-1]  # -1 to remove the last \n character.
        if t:
            uids.append(t)
    fileObj.close()
    log('Closed %s.' % 'mailed.txt')
    
    uids = list(set(uids))  # To get rid of duplicates
    log('Found: %d uids have been mailed already.' % len(uids))
    
    for uid in uids:
        try:
            participants.remove(User.objects.get(pk=int(uid)))
        except User.DoesNotExist:
            continue
        except ValueError:
            continue
        else:
            log('Already mailed uid %d. Removing from mailing list.' % int(uid))

    #participants = [User.objects.get(id=2199)]  # Comment this line for the finale

    for participant in participants:
        log(participant.id)
        pdf = generateCertificate(participant)
        if pdf is None:
            continue
        if participant.email:
            mailPDF(participant, pdf)
            savePDF(pdf, participant)
            #break  #TODO: Remove this for the finale

