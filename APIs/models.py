from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User

EVENT_CATEGORIES = (
	("Aerofest", "Aerofest"),
	("Coding", "Coding"),
	("Design and Build", "Design and Build"),
	("Involve", "Involve"),
	("Quizzes", "Quizzes"),
	("Online", "Online"),
	("Department Flagship", "Department Flagship"),
	("Spotlight", "Spotlight"),
	("Workshops", "Workshops"),
    ("Others", "Others"),
)

CATEGORY = (
    ("Update", "Update"),
    ("Announcement", "Announcement"),
)

GENDER_CHOICES = (
    ('M','Male'),
    ('F','Female'),
)

HOSTEL_CHOICES  =(
        ("Ganga", "Ganga"),
        ("Mandak", "Mandak"),
        ("Jamuna", "Jamuna"),
        ("Alak", "Alak"),
        ("Saraswathi", "Saraswathi"),
        ("Narmada", "Narmada"),
        ("Godav", "Godav"),
        ("Pampa", "Pampa"),
        ("Tambi", "Tambi"),
        ("Sindhu", "Sindhu"),
        ("Mahanadi", "Mahanadi"),
        ("Sharavati", "Sharavati"),
        ("Krishna", "Krishna"),
        ("Cauvery", "Cauvery"),
        ("Tapti", "Tapti"),
        ("Brahmaputra", "Brahmaputra"),
        ("Sarayu", "Sarayu"),
        )

DEP_CHOICES = (
("QMS", "Quality Management"),
("Finance", "Finance"),
("MobOps", "MobOps"),
("WebOps", "WebOps"),
("Hospitality", "Hospitality"),
("Publicity", "Publicity"),
("Graphic Design", "Graphic Design"),
("Photography", "Photography"),
("Ambience", "Ambience"),
("Creative Design", "Creative Design"),
("Videography", "Videography"),
("Air Show", "Air Show"),
("Wright Design", "Wright Design"),
("Paper Plane", "Paper Plane"),
("Aerobotics", "Aerobotics"),
("Hackfest", "Hackfest"),
("OPC", "OPC"),
("Reverse Coding", "Reverse Coding"),
("Triathlon", "Triathlon"),
("Robowars", "Robowars"),
("Contraptions", "Contraptions"),
("Fire n Ice", "Fire n Ice"),
("Robotics", "Robotics"),
("Junkyard Wars", "Junkyard Wars"),
("Ultimate Engineer", "Ultimate Engineer"),
("Project X", "Project X"),
("Shaastra Cube Open", "Shaastra Cube Open"),
("Puzzle Champ", "Puzzle Champ"),
("Math Modelling", "Math Modelling"),
("Shaastra Main Quiz", "Shaastra Main Quiz"),
("Online Events", "Online Events"),
("Desmod", "Desmod"),
("SCDC", "SCDC"),
("Robo-Oceana", "Robo-Oceana"),
("Gamedrome", "Gamedrome"),
("IDP", "IDP"),
("Shaastra Junior", "Shaastra Junior"),
("Sustainable Cityscape", "Sustainable Cityscape"),
("Case Study", "Case Study"),
("Fox Hunt", "Fox Hunt"),
("Magic Materials", "Magic Materials"),
("Computer Literacy For All", "Computer Literacy For All"),
("Face Off", "Face Off"),
("Sketch It", "Sketch It"),
("Pilot Training", "Pilot Training"),
("Hovercraft", "Hovercraft"),
("Lectures and VCs", "Lectures and VCs"),
("Shaastra Nights", "Shaastra Nights"),
("Symposium", "Symposium"),
("Exhibitions", "Exhibitions"),
("IITM Ideas Challenge", "IITM Ideas Challenge"),
("GA PA Materials", "GA/PA Materials"),
("Production", "Production"),
("Equipment", "Equipment"),
("Catering", "Catering"),
("VIP Care", "VIP Care"),
("Prize and Prize Money", "Prize and Prize Money"),
("Sales and Distribution", "Sales and Distribution"),
("Analytics", "Analytics"),
("Spons Creative", "Spons Creative"),
("Spons Publicity", "Spons Publicity"),
("Sponsorship and PR", "Sponsorship and PR"),
("Vishesh", "Vishesh"),
("Newsletter and PR", "Newsletter and PR"),
)

class Event(models.Model):
    title = models.CharField(max_length = 30)
    category = models.CharField(max_length=50,choices= EVENT_CATEGORIES)
    
    def __unicode__(self):
        return '%s' % self.title
    
    class Meta:
        db_table='events_event'

class Update(models.Model):
    description = models.TextField()
    category = models.CharField(max_length = 15, choices = CATEGORY, help_text='You can add 4 updates and 1 announcement. Mark as announcement only if the information is of highest importance')
    event = models.ForeignKey(Event, null=True, blank=True)
    expired = models.BooleanField(default=False, help_text='Mark an update/announcement as expired if it is no longer relevant or you have more than 4 updates (or 1 announcement) ')
    date = models.DateField(default=datetime.now)

    class Meta:
        db_table = 'events_update'

class MobAppTab(models.Model):
    event = models.ForeignKey(Event, blank=True, null=True)
    title = models.CharField(max_length=30)
    text = models.TextField()

    class Meta:
        db_table = 'events_tab'
# This is the initial department model
class Department(models.Model):
    Dept_Name= models.CharField(max_length=50,choices=DEP_CHOICES,default='Events')
    # In case of multiple owners
    owner = models.ManyToManyField(User, blank=True, null=True)
    def __str__(self):
        return self.Dept_Name
    class Meta:
        db_table ='department_department'

class userprofile(models.Model):
    """
    User's profile which contains all personal data.
    """
    user = models.ForeignKey(User, unique=True)
    nickname = models.CharField(max_length=30, blank=True)
    name = models.CharField(max_length=30, blank=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    chennai_number = models.CharField(max_length=15, blank=True)
    summer_number = models.CharField(max_length=15, blank=True)
    summer_stay = models.CharField(max_length=30, blank=True)
    hostel = models.CharField(max_length=15, choices = HOSTEL_CHOICES, blank=True)
    room_no = models.IntegerField(default=0, blank=True)

    class Meta:
        db_table='users_userprofile'
    
    def __str__(self):
        return '%s %s' %(self.user.username, self.nickname)

        
    

