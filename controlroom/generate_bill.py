from users.models import UserProfile, College, Team
from django.contrib.auth.models import User
from events.models import Event, EventSingularRegistration
from controlroom.models import *

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

    lineheight = PDFSetFont(pdf, 'Times-Roman', 12)

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

def generatetable(pdf, x, y, leader,s_ids):


    lineheight = PDFSetFont(pdf, 'Times-Bold', 16)

    (A4Width, A4Height) = A4

    pdf.drawCentredString(A4Width/2, y, 'TEAM ACCOMODATION DETAILS')

    y -= lineheight + cm

    # Construct the table data
    

    
    tableData = [ ['Shaastra ID', 'Room', 'Name', 'Phone No'] ]
    
    tm = Team.objects.filter(leader = leader)
    """
    for t in tm:
        for m in t.members.all():
            if int(team) == 1:
                try:
                    profile = UserProfile.objects.get(user = m,gender = 'M')
                    checkin = IndividualCheckIn.objects.get(shaastra_ID = profile.shaastra_id)
                    tableData.append([checkin.shaastra_ID, checkin.room])
                except:
                    pass
            elif int(team) == 2:
                print m
                try:
                    profile = UserProfile.objects.get(user = m,gender = 'F')
                    checkin = IndividualCheckIn.objects.get(shaastra_ID = profile.shaastra_id)
                    tableData.append([checkin.shaastra_ID, checkin.room])
                except:
                    pass    
    """        
    for s in s_ids:
        checkin = IndividualCheckIn.objects.get(id = s)
        tableData.append([checkin.shaastra_ID, checkin.room,(checkin.first_name+checkin.last_name),checkin.phone_no])    
        
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

def printParticipantDetails(pdf, x, y, s_id,team,number):
    if not number:
        n=1  
    else:
        n=0
        for s in number:
            n = n+1  
    print n
    if team == 0:
        CD = 0
        try:
            checkedin = IndividualCheckIn.objects.get(shaastra_ID=s_id)  
            profile = UserProfile.objects.get(shaastra_id = s_id)
        except:
            msg = "This participant has not been checked in!" 
    else:
        profile = UserProfile.objects.get(shaastra_id = s_id)
        checkedin = IndividualCheckIn.objects.get(shaastra_ID=s_id)  
        leader = User.objects.get(id = profile.user_id)
     
       
    if n<=3:
        CD = 500
    elif n>3 and n<=6:
        CD = 1000
    else:
        CD=1500
    
    lineheight = PDFSetFont(pdf, 'Times-Roman', 12)
    
    if team == 0:
        pdf.drawString(x, y, 'Shaastra ID: %s' % checkedin.shaastra_ID)
        y -= lineheight + (cm * 0.8)

        pdf.drawString(x, y, 'Name: %s %s' % (checkedin.first_name, checkedin.last_name))
        y -= lineheight + (cm * 0.8)

        pdf.drawString(x, y, 'Mattresses: %s' % checkedin.number_of_mattresses_given)
        y -= lineheight + (cm * 0.8)

        pdf.drawString(x, y, 'Room Allotted: %s' % checkedin.room)
        y -= lineheight + (cm * 0.8)
    
    else:
        pdf.drawString(x, y, "Team Leader's Shaastra ID: %s" % profile.shaastra_id)    
        y -= lineheight + (cm * 0.8)

        pdf.drawString(x, y, "Team Leader's Name: %s %s" % (leader.first_name, leader.last_name))
        y -= lineheight + (cm * 0.8)
    
        matt = Mattresses.objects.get(team_leader_id = profile.shaastra_id)

        pdf.drawString(x, y, 'Mattresses: %s' % matt.no_of_mattresses)
        y -= lineheight + (cm * 0.8)
    
    pdf.drawString(x, y, 'Mobile No: %s' % profile.mobile_number)
    
    y -= lineheight + (cm * 0.8)

    pdf.drawString(x, y, 'College: %s' % profile.college)
    
    y -= lineheight + (cm * 0.8)

    d = checkedin.duration_of_stay

    
    pdf.drawString(x, y, 'Check In date & time: %s' % checkedin.check_in_date)
    
    y -= lineheight + (cm * 0.8)

    pdf.drawString(x, y, 'No of days of stay: %s' % checkedin.duration_of_stay)
    
    y -= lineheight + (cm * 0.8)

   
    pdf.drawString(x, y, 'Caution Deposit: %s' % CD)
    
    y -= lineheight + (cm * 0.8)

    if int(d)>2:
        amount = CD + (320 + 160 *(int(d)-2))*n
    else:
        amount = CD +320*int(n)
    pdf.drawString(x, y, 'Amount: %s' % amount)
    
    y -= lineheight + (cm * 0.8)

    pdf.drawString(x, y, 'Mattress Room: %s' % checkedin.mattress_room)
    
    y -= lineheight + (cm * 0.8)

    pdf.drawString(x, y, "Coordinator's Signature:")
    
    y -= lineheight + (cm * 0.8)

    return y

def generateParticipantPDF(s_id,team,number=[]):
    
    print number
    userProfile = UserProfile.objects.get(shaastra_id = s_id)
    
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = \
        'filename=AccomodationBill.pdf'
    
    # Create the PDF object, using the response object as its "file."

    pdf = canvas.Canvas(response, pagesize=A4)

    # Define the title of the document as printed in the document header.

    page_title = 'Accomodation Bill'

    # Get the width and height of the page.

    (A4Width, A4Height) = A4

    # Page number

    pageNo = 1

    # Paint the headers and get the coordinates

    y = initNewPDFPage(pdf, page_title, pageNo, A4)

    # Setting x to be a cm from the left edge

    x = cm

    # Print Participant Details in PDF
    
    y = printParticipantDetails(pdf, x, y, userProfile.shaastra_id,int(team),number)
  
    if not int(team) == 0:
        generatetable(pdf,x,y,userProfile.user,number)

    pdf.showPage()
    pdf.save()
    
    return response


