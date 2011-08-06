from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def createuser(request):
    if request.method=="POST":
        User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
        return HttpResponseRedirect(reverse ("test"))
    return render_to_response("newuser.html",{},context_instance=RequestContext(request))

def profile(request):
    return render_to_response("profile.hmtl",{},context_instance=RequestContext(request))