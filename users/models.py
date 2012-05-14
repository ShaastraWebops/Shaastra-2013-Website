from django.db import models
from django.contrib.auth.models import User
import urllib,json
#from main_test.events.models import Event

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)

STATE_CHOICES = (
	("Andhra Pradesh" , "Andhra Pradesh"),
	("Arunachal Pradesh" , "Arunachal Pradesh"),
	("Assam" , "Assam"),
	("Bihar" , "Bihar"),
	("Chhattisgarh" , "Chhattisgarh"),
	("Goa" , "Goa"),
	("Gujarat" , "Gujarat"),
	("Haryana" , "Haryana"),
	("Himachal Pradesh" , "Himachal Pradesh"),
	("Jammu And Kashmir" , "Jammu And Kashmir"),
	("Jharkhand" , "Jharkhand"),
	("Karnataka" , "Karnataka"),
	("Kerala" , "Kerala"),
	("Madhya Pradesh" , "Madhya Pradesh"),
	("Maharashtra" , "Maharashtra"),
	("Manipur" , "Manipur"),
	("Meghalaya" , "Meghalaya"),
	("Mizoram" , "Mizoram"),
	("Nagaland" , "Nagaland"),
	("Orissa" , "Orissa"),
	("Punjab" , "Punjab"),
	("Rajasthan" , "Rajasthan"),
	("Sikkim" , "Sikkim"),
	("Tamil Nadu" , "Tamil Nadu"),
	("Tripura" , "Tripura"),
	("Uttar Pradesh" , "Uttar Pradesh"),
	("Uttarakhand" , "Uttarakhand"),
	("West Bengal" , "West Bengal"),
	("Andaman And Nicobar Islands" , "Andaman And Nicobar Islands"),
	("Chandigarh" , "Chandigarh"),
	("Dadra And Nagar Haveli" , "Dadra And Nagar Haveli"),
	("Daman And Diu" , "Daman And Diu"),
	("Lakshadweep" , "Lakshadweep"),
	("NCT/Delhi" , "NCT/Delhi"),
	("Puducherry" , "Puducherry"),
	("Outside India" , "Outside India"),
)
'''
class College(models.Model):
    name=models.CharField (max_length = 255,help_text  = 'The name of your college. Please refrain from using short forms.')
    city=models.CharField (max_length = 30,help_text  = 'The name of the city where your college is located. Please refrain from using short forms.' )
    state=models.CharField (max_length = 40,choices    = STATE_CHOICES,help_text  = 'The state where your college is located. Select from the drop down list' )

    def __unicode__(self):
        return "%s, %s, %s"%(self.name, self.city, self.state)

    class Admin:
        pass
'''
#User profile common to all users
class UserProfile(models.Model):
    user 			= models.OneToOneField		(User, unique = True)
    gender 			= models.CharField		(max_length = 1, choices = GENDER_CHOICES, default = 'F')   #Defaults to 'girl' ;-)
    age 			= models.IntegerField 	(default = 18 , help_text = 'You need to be over 12 and under 80 years of age to participate')
    branch 			= models.CharField		(max_length = 50, default = 'Enter Branch Here', blank = True, null=True, help_text = 'Your branch of study')
    mobile_number 	= models.CharField		(max_length = 15, null=True , help_text='Please enter your current mobile number')
#    college 		= models.ForeignKey		(College,null=True,blank=True)
    college_roll 	= models.CharField		(max_length = 40, null=True)
    shaastra_id 	= models.CharField		(max_length = 20, unique = True, null=True)
    activation_key 	= models.CharField		(max_length = 40, null=True)
    key_expires 	= models.DateTimeField	(null=True)
    want_hospi 		= models.BooleanField	(default = False)
    is_coord        = models.BooleanField	(default = False)
#    coord_event     = models.ForeignKey     (Event, null = True)
#    registered      = models.ManyToManyField(Event, null=True, related_name='registered_users')        #Events which this user has registered for
    facebook_id = models.BigIntegerField()
    access_token = models.CharField(max_length=150)

    def get_facebook_profile(self):
        fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token=%s' % self.access_token)
        return json.load(fb_profile)
    
    def __unicode__(self):
        return self.user.username

    class Admin:
        pass
'''
class Feedback(models.Model):
    name    = models.CharField  ( max_length = 30, null = True,  help_text = 'Your first name' )
    email   = models.EmailField ( null = True, help_text = 'The email id to respond to' )
    content = models.CharField  ( max_length = 10000, null = True, help_text= 'Please stick to the point' )
    radiocontent = models.CharField  ( max_length = 10000, null = True)
    def __unicode__(self):
        return self.content
    
    class Admin:
        pass            


class Team(models.Model):
    name            = models.CharField(max_length = 50) 
    event           = models.ForeignKey(Event, null = False)
    leader          = models.ForeignKey(User, related_name = 'own_teams', blank = False, null = False)
    members         = models.ManyToManyField(User, related_name = 'joined_teams', blank = True, null = True)
    
    def __unicode__(self):
        return self.name
    
    class Admin:
        pass

'''
