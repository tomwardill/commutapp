# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

from leedshackthing.main import tasks

def index(request):
    
    return render_to_response('test.html', {}, context_instance = RequestContext(request))


def currentroad(request):
    
    tasks.update_current_road()

def futureroad(request):
    pass

def unplannedevent(request):
    pass