from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import fromstr

from dateutil.parser import parse as date_parse

from leedshackthing.main.models import Commute


def new(request):
    
    user = request.user
    data = {}
    
    if request.method == 'POST':

        c = Commute()
        c.user = request.user
        c.name = request.POST['name']
        c.box = fromstr(request.POST['wkt'])
        start_time = date_parse(request.POST['starttime']).time()
        end_time = date_parse(request.POST['endtime']).time()
        c.start_time = start_time
        c.end_time = end_time
        
        c.save()
        
        return HttpResponseRedirect(reverse('index'))
    
    return render_to_response('commute-new.html', {}, context_instance = RequestContext(request))


def edit(request, commute_id):
    
    
    commute = Commute.objects.get(id = commute_id)
    
    if request.method == 'POST':

        c = commute
        c.user = request.user
        c.name = request.POST['name']
        if request.POST['wkt']:
            c.box = fromstr(request.POST['wkt'])
        start_time = date_parse(request.POST['starttime']).time()
        end_time = date_parse(request.POST['endtime']).time()
        c.start_time = start_time
        c.end_time = end_time
        
        c.save()
        
        return HttpResponseRedirect(reverse('index'))
    
    return render_to_response('commute-new.html', locals(), context_instance = RequestContext(request))