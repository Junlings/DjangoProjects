from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
#from purchases.models import Purchase

def home(request):
    if request.user.is_authenticated():
        # already logged in
        context = {'user':request.user,
                   'REGISTER_URL': settings.REGISTER_URL,
                   'ROOT_URL':settings.ROOT_URL}
        return render_to_response('userhome.html', context,
             context_instance=RequestContext(request))
    
    else:
        # lead to login or registration
        context = {'LOGIN_URL': settings.LOGIN_URL,
               'REGISTER_URL':settings.REGISTER_URL}

        return render_to_response('home.html', context,
        context_instance=RequestContext(request))     

