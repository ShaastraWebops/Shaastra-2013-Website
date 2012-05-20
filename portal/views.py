# Create your views here.
from django.http import *
from django.shortcuts import *
from django.template import *
from portal.models import *
from settings import *
import os
from django.core.urlresolvers import reverse
from django.contrib import admin

def home(request):
    return render_to_response("home.html",locals(),context_instance=RequestContext(request))    
    
def category(request):
    categories = Category.objects.all()
    photos_list = CategoryImage.objects.all()
    return render_to_response("categories.html",locals(),context_instance=RequestContext(request))
    
def events(request, category):
    cleaned_category = category.replace("_"," ")
    c = get_object_or_404(Category, name = cleaned_category)
    events_list = c.events.all()
    photos_list = EventImage.objects.all()
    return render_to_response("events.html",locals(),context_instance=RequestContext(request))
