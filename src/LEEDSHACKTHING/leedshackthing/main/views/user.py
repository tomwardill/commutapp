from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import models


def createuser(request):
    if request.method=="POST":
        User.objects.create_user(request.POST["username"], request.POST["email"], request.POST["password"])
        return HttpResponseRedirect(reverse ("test"))
    return render_to_response("newuser.html",{},context_instance=RequestContext(request))

def profile(request):
    user=request.user
    user_profile = user.get_profile()
    if request.method=="POST":
        
        if user.check_password(request.POST["password"]):
            user.email=request.POST["email"]
            user.first_name=request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user_profile.phonenum = request.POST["phonenum"]
            user_profile.growlkey = request.POST["growlkey"]
            #user_profile.com_hours = request.POST["com_hours"]
            #user.com_mins = request.POST["com_mins"]
            user.save()
            user_profile.save()
    select_hours_list=range(24)
    return render_to_response("profile.html",locals(),context_instance=RequestContext(request))
  