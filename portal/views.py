# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from portal.models import *
from settings import *
import os
from topics.models import *
from django.core.urlresolvers import reverse
from django.contrib import admin

def home(request):
	topics=Topic.objects.all()
	topic_images=TopicImage.objects.all()
	return render_to_response("home.html",locals(),context_instance=RequestContext(request))    
    
def category(request):
	topics=Topic.objects.all()
	topic_images=TopicImage.objects.all()
	categories = Category.objects.all()
	photos_list = CategoryImage.objects.all()
	return render_to_response("categories.html",locals(),context_instance=RequestContext(request))
    
def events(request, category):
	topics=Topic.objects.all()
	topic_images=TopicImage.objects.all()
	cleaned_category = category.replace("_"," ")
	c = get_object_or_404(Category, name = cleaned_category)
	events_list = c.events.all()
	photos_list = EventImage.objects.all()
	return render_to_response("events.html",locals(),context_instance=RequestContext(request))

def topic_details(request,topic_url_name):
	topics=Topic.objects.all()
	topic_images=TopicImage.objects.all()
	present_topic=Topic.objects.get(url_name=topic_url_name)
	present_topic_images=TopicImage.objects.filter(topic = present_topic)
	return render_to_response("topic_details.html",locals(),context_instance=RequestContext(request))
