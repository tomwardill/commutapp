from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import fromstr
from django.contrib import messages

from dateutil.parser import parse as date_parse

from leedshackthing.main.models import Commute
from leedshackthing.main.forms import CommuteForm


def new(request):
    
    user = request.user
    data = {}
    
    if request.method == 'POST':
        form = CommuteForm(request.POST)
        if form.is_valid():

            form.instance.user = request.user
            form.instance.box = fromstr(request.POST['box'])
            form.save()
            messages.success(request, 'Commute created.')
            return HttpResponseRedirect(reverse('index'))
        data['form'] = form
    else:
        data['form'] = CommuteForm()
    
    return render_to_response('commute-new.html', data, context_instance = RequestContext(request))


def edit(request, commute_id):
    
    
    commute = Commute.objects.get(id = commute_id)
    form = CommuteForm(instance = commute)
    
    if request.method == 'POST':
        
        # if the user has pressed the delete button
        if request.POST.has_key('delete'):
            # redirect to the delete confirmation
            return HttpResponseRedirect(reverse('commute-delete', args = [commute.id]))

        form = CommuteForm(request.POST, instance = commute)
        if form.is_valid():

            form.instance.user = request.user
            form.instance.box = fromstr(request.POST['box'])
            form.save()
            messages.success(request, 'Commute edited.')
            return HttpResponseRedirect(reverse('index'))
        

    
    return render_to_response('commute-new.html', locals(), context_instance = RequestContext(request))


def delete(request, commute_id):
    
    commute = get_object_or_404(Commute, id = commute_id)
    
    if request.method == 'POST':
        if request.POST.has_key('Delete'):
            commute.delete()
            messages.success(request, 'Commute deleted.')
            return HttpResponseRedirect(reverse('index'))
        if request.POST.has_key('NoDelete'):
            return HttpResponseRedirect(reverse('commute-edit', args = [commute.id]))
        
    
    return render_to_response('commute-delete.html', locals(), context_instance = RequestContext(request))