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

    #if userProfile.want_accomodation:
    #    accountDetails += '<br/><b>Accomodation requested</b><br/><br/>'
    #else:
    #    accountDetails += '<br/><b>Accomodation not requested</b><br/><br/>'
    
    y = paintParagraph(pdf, x, y, accountDetails)

    accountInstruction = 'Attention: <b>If you have not created an account on the Shaastra website</b>, an account has been created for you. Both your username and password are the local part of your email address. E.g. if your email is \'example@domain.com\', both your username and password will be \'example\' (without the quotes). <b>Please do update your profile on the Shaastra website to avoid any inconvenience later.</b>'
    
    y = paintParagraph(pdf, x, y, accountInstruction)
    
    qmsInstruction = '<para alignment="center"><font size=14><b>QMS Instructions</b></font>'
    
    y -= cm*0.7
    y = paintParagraph(pdf, x, y, qmsInstruction)
    
    qmsInstruction = '</para><para alignment="left"><br/><br/>1. Every participant must bring a printed/e-copy of this form.<br/><br/>2. Every participant can collect his/her Shaastra Passport from the Registration (QMS) Desk (KV Grounds) or one of the Hospitality Control Rooms (Ganga Hostel for Boys and Sharavati Hostel for Girls)  on payment of INR 100.<br/><br/>3. The Shaastra Passport is NON TRANSFERABLE.<br/><br/>4. In case you lose your Shaastra Passport, you can collect a new one at the Registration Desk, on payment of INR 100. To collect the new passport, you need to show this form again.<br/><br/>5. The Shaastra Passport will be your official entry to Shaastra, and will be used to register you for Events, issuing certificates, accommodation and cash prizes.<br/><br/>6. For any queries, please drop us a mail on qms@shaastra.org. We will get back to you within 24 hours.<br/><br/>QMS Team</para>'
    
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
    #    y -= cm * 0.5
    #    pdf.drawString(x, y, 'You are not registered for any events this Shaastra')
    
    #else:
    #    pdf.showPage()
    #    y = initNewPDFPage(pdf, A4, userProfile.shaastra_id, userProfile.user.username)
        
    #    printEventParticipationDetails(pdf, x, y, user, singularEventRegistrations, userTeams)
    
    pdf.showPage()
    pdf.save()

    response = buffer.getvalue()
    buffer.close()

    return response
    
def log(msg):

    destination = open('/home/shaastra/hospi/participantPDFs/log.txt', 'a')
    destination.write(str(msg))
    destination.write('\n')
    destination.close()
    print msg

def mailPDF(user, pdf):

    subject = '[IMPORTANT] Registration Details, Shaastra 2013'
    message = 'Dear '
    if user.first_name and user.last_name:
        message += user.first_name.title() + ' ' + user.last_name.title()
    elif user.first_name:
        message += user.first_name.title()
    elif user.last_name:
        message += user.last_name.title()
    elif user.username:
        message += user.username
    else:
        message += 'participant'
    
    message += ',<br/><br/>The attached PDF contains important information regarding your registration at Shaastra 2013.<br/><br/>'
    message += 'If you have received a similar mail earlier, please <b>discard the <u>previous</u> mail and its attachment</b>. This mail contains an updated pdf.<br/><br/>'
    message += ' Please bring <b>two printed copies</b> of this PDF with you.'
    message += ' For any queries, please contact the QMS Team at qms@shaastra.org.<br/><br/>Team Shaastra 2013<br/>'
    email = user.email
    #email = 'swopstesting@gmail.com' #TODO: Remove this line for finale

    msg = EmailMultiAlternatives(subject, message, 'noreply@iitm.ac.in' , [email,])
    msg.content_subtype = "html"
    msg.attach('%s-registration-details.pdf' % user.get_profile().shaastra_id, pdf, 'application/pdf')
    msg.send()  #TODO: Uncomment this line for finale
    log('Mail sent to %s' % email)  #TODO: Uncomment this line for finale
    #log('NOT sent. Mail will go to %s' % email)  #TODO: Comment this line for finale
    
def savePDF(pdf, user):

    destination = open('/home/shaastra/hospi/participantPDFs/'+user.get_profile().shaastra_id+'-registration-details.pdf', 'wb+')
    destination.write(pdf)
    destination.close()
    log('File '+user.get_profile().shaastra_id+'-registration-details.pdf saved.')
    
def generatePDFs(uid):

    #return ('Comment this line to send the Participant PDFs.')

    #participants = []
    #numPDFsGenerated = 0
    #numPDFsMailed = 0
    #userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    #participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(user__is_superuser = False)
    #for profile in participantProfilesWithShaastraIds:
    #    try:
    #        u = profile.user
    #    except:
    #        continue
    #    participants.append(u)

    participants = [User.objects.get(id = uid)] #TODO: Remove this line for finale

    for participant in participants:
        #if participant.id < 7071:
        #    continue
        log(participant.id)
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        savePDF(pdf, participant)
        if participant.email:
            mailPDF(participant, pdf)
    #        numPDFsMailed += 1
    #    numPDFsGenerated += 1
        
    #log('\n\nPDFs generated: %d' % numPDFsGenerated)
    #log('\n\nPDFs mailed: %d' % numPDFsMailed)
    
def remainingPDFs():

    return ('Comment this line to send the Participant PDFs.')
    
    log('\n\n**********  Now: %s  **********' % datetime.datetime.now())

    fileNameList = ['/home/shaastra/hospi/participantPDFs/ssq.txt', '/home/shaastra/hospi/participantPDFs/rws.txt']
    
    for fileName in fileNameList:

        participants = []
        emails = []

        fileObj = open(fileName, 'r')
        log('\n\nOpened %s.' % fileName)
        for line in fileObj:
            t = line[:-1]  # -1 to remove the last \n character.
            if t:
                emails.append(t)
        fileObj.close()
        log('Closed %s.' % fileName)

        emails = list(set(emails))  # To get rid of duplicates

        for email in emails:
            usersMatchingEmail = User.objects.filter(email = email)
            if len(usersMatchingEmail) == 1:
                participants.append(usersMatchingEmail[0])
            elif len(usersMatchingEmail) < 1:
                log('No users matching %s' % email)
            else:
                log('More than one users matching %s' % email)

        for participant in participants:
            log(participant.id)
            pdf = generateParticipantPDF(participant)
            if pdf is None:
                continue
            savePDF(pdf, participant)
            if participant.email:
                mailPDF(participant, pdf)
                #break  #TODO: Remove this for the finale

def mailRoundTwo():
    
    #return ('Comment this line to send the Participant PDFs.')
    
    log('\n\n**********  Now: %s  **********' % datetime.datetime.now())

    uids = []
    
    participants = []
    userProfilesWithShaastraIds = UserProfile.objects.exclude(shaastra_id = '') #TODO Exclude non active users??
    participantProfilesWithShaastraIds = userProfilesWithShaastraIds.exclude(is_core = True).filter(user__is_superuser = False)
    for profile in participantProfilesWithShaastraIds:
        try:
            u = profile.user
        except:
            continue
        participants.append(u)

    fileObj = open('/home/shaastra/hospi/participantPDFs/mailed.txt', 'r')
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
        
    for participant in participants:
        log(participant.id)
        pdf = generateParticipantPDF(participant)
        if pdf is None:
            continue
        savePDF(pdf, participant)
        if participant.email:
            mailPDF(participant, pdf)
            #break  #TODO: Remove this for the finale
            
def checkData(**kwargs):

    for key in kwargs.keys():
        if key[:len('UserProfile')] == 'UserProfile':
            finalKey = key[len('UserProfile'):]
            searchParams = {finalKey: kwargs[key]}
            profiles = UserProfile.objects.filter(**searchParams)
            users = []
            for profile in profiles:
                try:
                    users.append(profile.user)
                except:
                    continue
        else:
            finalKey = key
            searchParams = {finalKey: kwargs[key]}
            users = User.objects.filter(**searchParams)
        if len(users) == 0:
            print 'No users found with the input data'
            return None
        else:
            print 'Data found...\n'
            for user in users:
                string = user.username + ': ' + user.first_name + ' ' + user.last_name + ' (' + str(user.id) + ')  -->  '
                string += user.email
                singularEventRegistrations = EventSingularRegistration.objects.filter(user = user)
                userTeams = user.joined_teams.all()
                string += '\n  Singular Events:' + str(singularEventRegistrations)
                string += '\n  Teams:' + str(userTeams)
                string += '\n    '
                try:
                    f = open('/home/shaastra/hospi/participantPDFs/SHA'+str(1300000+user.pk)+'-registration-details.pdf', 'r')
                except:
                    
                    if (not singularEventRegistrations) and (not userTeams):
                        string += 'NO mail required'
                    else:
                        string += 'NOT mailed'                    
                    pass
                else:
                    f.close()
                    string += 'Mailed\n'
                print string

            if len(users) == 1:
                return users[0]
                
            else:
                return users

def addLeadersToMembers():
    teams = Team.objects.all()
    for team in teams:
        print team.name
        try:
            l = team.leader
        except:
            print 'Bad team. No leader.'
            print '\n'
            continue
        if l not in team.members.all():
            print 'Leader: ' + l.username
            print str(team.members.all())
            team.members.add(l)
            print 'After adding: ' + str(team.members.all())
            print '\n'
            
def createUser(fullname=None, email=None, mobile=None, college=None):

    try:
        newUser = User.objects.get(username = email.split('@')[0])
    except User.DoesNotExist:
        newUser = User()
        newUser.email = email
        newUser.username = email.split('@')[0]
        newUser.first_name = fullname
        newUser.set_password('default')
        newUser.is_active = True
        newUser.save()
        # Get the college
        try:
            newCollege = College.objects.get(name = college)
        except:
            newCollege = None
        # Create the user's profile
        newUserProfile = UserProfile()
        newUserProfile.user = newUser
        newUserProfile.mobile_number = mobile
        newUserProfile.gender = 'F'
        newUserProfile.age = 0
        newUserProfile.shaastra_id = 'SHA' + str(1300000 + newUser.id)
        if newCollege:
            newUserProfile.college = newCollege
        newUserProfile.branch = 'Others'
        newUserProfile.want_accomodation = False
        newUserProfile.save()
    return newUser
            
def checkParticipationDetailsCSV(path, event_name):
    try:
        partFile = open(path, 'r')
    except IOError:
        print 'Could not open %s.' % path
        return
    print 'Read file opened.'
    try:
        outFile = open(path[:-4]+'_out.csv', 'w')
    except IOError:
        print 'Could not open write file %s.' % (path[:-3]+'out.csv')
        return
    print 'Out file opened.'
    try:
        e = Event.objects.get(title = event_name)
    except Event.DoesNotExist:
        print 'Event \'%s\' not found.' % event_name
        return
    print 'Event obtained.\n'

    for line in partFile:
        print 'Line read: %s' % line
        line = line[:-1]  # -1 to remove the last \n character.
        outLine = line
        data = line.split(',')
        if not data[0].isdigit():  # The first column in the CSV should be a serial number
            print 'First entry not S.No. Continuing...\n'
            continue
        u = User.objects.filter(email=data[3])
        if not u:
            # User not found
            print 'Email not found. Trying to create...'
            u = [createUser(college=data[1], fullname=data[2], email=data[3], mobile=data[4])]
            outLine += ', user Created'
        else:
            # User found
            print 'User found.'
            outLine += ', user Found'
        if len(u) == 1:
            # one user found
            # check registration for event
            # if not registered, register
            u = u[0]
            regn = EventSingularRegistration.objects.filter(user = u).filter(event = e)
            if not regn:
                # The user is not registered
                # go ahead and register
                regn = EventSingularRegistration()
                regn.user = u
                regn.event = e
                regn.save()
                outLine += ', new regn'
                
            elif len(regn) == 1:
                # User is registered
                # Check if mailed
                try:
                    temp = open('/home/shaastra/hospi/participantPDFs/SHA'+str(1300000+u.pk)+'-registration-details.pdf', 'r')
                except IOError:
                    # PDF not found.
                    # Not mailed.
                    outLine += ', not mailed'
                else:
                    # PDF found
                    # mailed
                    outLine += ', Mailed'
                    temp.close()
                
            else:
                # More than one registrations found.
                # Write this to file
                outLine += ', >1 regn found'
            
        else:
            # More than one user found.
            # write this to file
            outLine += ', >1 user found,'
        outLine += '\n'
        outFile.write(outLine)
        
    partFile.close()
    outFile.close()
    
def cleanParticipationCSV(path):
    f = open(path, 'r')
    t = open(path[:-4]+'_mod.csv', 'w')
    for l in f:
        q = False
        n = ''
        for i in range(len(l)):
            if l[i] == '\"':
                if q is True: q = False
                else: q = True
            if l[i] == ',' and q is True: n += ''
            elif l[i] == '\"': n += ''
            else: n += l[i]
        t.write(n)
    f.close()
    t.close()
    
def cleanEmails():
    for u in User.objects.all():
        if u.email and u.email[-1] == ',':
            print u.id
            print u.email
            u.email = u.email[:-1]
            print u.email
            try:
                os.remove('/home/shaastra/hospi/participantPDFs/SHA'+str(1300000+u.id)+'-registration-details.pdf')
            except OSError:
                print 'PDF doesn\'t exist.'
            else:
                print 'PDF deleted.'
            u.save()
            print '\n'

