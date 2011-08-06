# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    
    return render_to_response('test.html', {}, context_instance = RequestContext(request))


def currentroad(request):
    
    pass

def futureroad(request):
    pass

def unplannedevent(request):
    pass