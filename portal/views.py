# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from portal.models import *
from portal.forms import *
import os
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.auth import logout
from django.conf import settings


def home(request):
    categories = Category.objects.all()
    topics=Topic.objects.all()
    topic_images=TopicImage.objects.all()
    previous_sponsors=PreviousSponsor.objects.all()
    quotes=Quote.objects.all()
    one_home_content=Home.objects.filter(id=1)
    if one_home_content:
        home_content=Home.objects.get(id=1)
    else:
        home_content=Home(info=" ")
        home_content.save()
    if request.method == "POST":
        form = HomeForm(request.POST, instance=home_content)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = HomeForm(instance=home_content) 	
    return render_to_response("home.html",locals(),context_instance=RequestContext(request))    
    
def category(request):
    topics=Topic.objects.all()
    topic_images=TopicImage.objects.all()
    categories = Category.objects.all()
    events= Event.objects.all()
    photos_list = CategoryImage.objects.all()
    return render_to_response("categories.html", locals(),context_instance=RequestContext(request))
    
def events(request, category):
	topics=Topic.objects.all()
	categories = Category.objects.all()
	events= Event.objects.all()
	topic_images=TopicImage.objects.all()
	c = get_object_or_404(Category, url_name = category)
	events_list = c.events.all()
	photos_list = EventImage.objects.all()
	event_less_photos=[]
	event_more_photos=[]
	for event in events:
		photos_event=EventImage.objects.filter(event=event)
		count=0
		for photos in photos_event:
			count+=1
		if count == 1 or count ==0:
			event_less_photos.append(event)
	for event1 in events:
		photos_event1=EventImage.objects.filter(event=event1)
		count=0
		for photos1 in photos_event1:
			count+=1
		if count>1:
			event_more_photos.append(event1)

	return render_to_response("events.html",locals(),context_instance=RequestContext(request))

def topic_details(request,topic_url_name):
	topics=Topic.objects.all()
	topic_images=TopicImage.objects.all()
	present_topic=Topic.objects.get(url_name=topic_url_name)
	present_topic_images=TopicImage.objects.filter(topic = present_topic)
	quotes=Quote.objects.all()
	"""
	Form for textfield. This is required because usually html is not processed 
	when displaying on screen. Only plain text will be displayed. 
	mark_safe explicitly marks a string as safe for (HTML) output purposes.
	Here information is stored, marked as safe in display_MySafeField
	in Topic model so that when it is displayed on the screen, unlike usual all
	the html is processed and text editing is enabled.
	"""
	if request.method == "POST":
	    form = TextForm(request.POST, instance=present_topic)
	    if form.is_valid:
	        form.save()
	        return HttpResponseRedirect(request.path)
	else:
	    form = TextForm(instance=present_topic)       
	return render_to_response("topic_details.html",locals(),context_instance=RequestContext(request))


def logout_admin(request):
	logout(request)
	return HttpResponseRedirect(reverse('portal.views.home'))
