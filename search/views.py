# Create your views here.
from haystack.query import *
from events.models import *

def searchquery(search_term = None):
    #skeleton for queries
    event_titles=SearchQuerySet().filter(content=search_term).models(Event)
    best_match_title=SearchQuerySet().autocomplete(title_autocomplete=search_term).models(Event)
    best_match_category=SearchQuerySet().autocomplete(category_autocomplete=search_term).models(Event)
    #this isn't working currently, some whoosh_backend.py hack is needed?
    tab_content = SearchQuerySet().filter(content=search_term).models(Tab)
    print event_titles, best_match_title, best_match_category, tab_content, 'FIN'
     
    # Return search results to template here. 
    
    spellsuggest1 = SearchQuerySet.spelling_suggestion(search_term)
    spellsuggest2  = SearchQuerySet.auto_query(search_term).spelling_suggestion()
    print 'did you mean', spellsuggest, 'or', spellsuggest2
    
    '''
    Later modifications include <em> tags for search terms 
    Currently, the tab model is improperly indexing for some reason.
    Also, RealtimeSearchIndex everything? Server can handle?
    '''
