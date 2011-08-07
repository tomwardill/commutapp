# Create your views here.
from datetime import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from leedshackthing.main import tasks
from leedshackthing.main import models

def index(request):
    
    data = {}
    data['currentroad'] = len(models.CurrentRoadWorks.objects.all())
    data['futureroad'] = len(models.FutureRoadWorks.objects.all())
    data['unplannedevent'] = len(models.UnplannedEvent.objects.all())
    
    return render_to_response('test.html', data, context_instance = RequestContext(request))


def currentroad(request):
    
    number = tasks.update_current_road()
    return HttpResponseRedirect(reverse('test'))

def futureroad(request):
    
    number = tasks.update_future_road()
    return HttpResponseRedirect(reverse('test'))

def unplannedevent(request):
    
    number = tasks.update_unplanned_events()
    return HttpResponseRedirect(reverse('test'))

def affected(request):

    commutes = tasks.notify_users()
    return HttpResponseRedirect(reverse('test'))
