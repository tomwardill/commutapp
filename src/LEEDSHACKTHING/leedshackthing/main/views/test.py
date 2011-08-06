# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from leedshackthing.main import tasks
from leedshackthing.main import models

def index(request):
    
    data = {}
    data['currentroad'] = len(models.CurrentRoadWorks.objects.all())
    
    return render_to_response('test.html', data, context_instance = RequestContext(request))


def currentroad(request):
    
    number = tasks.update_current_road()
    return HttpResponse(str(number))

def futureroad(request):
    pass

def unplannedevent(request):
    pass