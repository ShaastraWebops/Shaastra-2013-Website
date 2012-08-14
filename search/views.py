from haystack.query import *
from events.models import *
from django.shortcuts import render_to_response

def search_title(search_term):
    titles=SearchQuerySet().autocomplete(title=search_term).models(Event)
    return titles
    
def search_category(search_term):
    categories=SearchQuerySet().autocomplete(category=search_term).models(Event)
    return categories

def search_tabs(search_term):
    tabs = SearchQuerySet().filter(content=search_term).models(Tab)
    return tabs
    
def searchquery(request, search_term=None):
    eventresults=[]
    eventresults.append(search_title(search_term)) 
    eventresults.append(search_category(search_term))
    tabresults=search_tabs(search_term)
    if spellsuggest(search_term) is not '':
        spell=spellsuggest(search_term)
        try:
            spell = spell[0].split('|')
        except:
            pass
    print eventresults, tabresults
    return render_to_response("search/search.html",locals()) 
    
def spellsuggest(search_term):
    spellsuggest1 = SearchQuerySet().spelling_suggestion(search_term)
    spellsuggest2  = SearchQuerySet().auto_query(search_term).spelling_suggestion()
    if(spellsuggest1!=spellsuggest2):
        return spellsuggest1+'|'+spellsuggest2
    else:
        return spellsuggest2
