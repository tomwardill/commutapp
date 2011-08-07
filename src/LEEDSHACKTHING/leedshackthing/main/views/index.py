from django.shortcuts import render_to_response
from django.template import RequestContext

from leedshackthing.main.models import Commute

def index(request):
    
    user = request.user
    data = {}
    
    if request.user.is_authenticated():
        # get all the users commutes
        data['commutes'] = Commute.objects.filter(user = user)
    
    
    return render_to_response('index.html', data, context_instance = RequestContext(request))
