from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from accounts.models import UserRefLib
from lreviews_2.models import reviewproj
from django.db.models import Q

def home(request):
    if request.user.is_authenticated():
        # already logged in
        libs = UserRefLib.objects.filter(Q(Owner=request.user) | Q(Contributor=request.user))
        
        userlibdict = {}
        for lib in libs:
            userlibdict[lib.name] = {'lib':lib}
            if request.user == lib.Owner:
                userlibdict[lib.name]['owner'] = True
            else:
                userlibdict[lib.name]['owner'] = False
            if request.user in lib.Contributor.all():
                userlibdict[lib.name]['Contributor'] = True
            else:
                userlibdict[lib.name]['Contributor'] = False

        return render_to_response('userhome.html', {'UserRefLib':userlibdict},
             context_instance=RequestContext(request))
    
    else:
        # lead to login or registration
        context = {'LOGIN_URL': settings.LOGIN_URL,
               'REGISTER_URL':settings.REGISTER_URL}

        return render_to_response('home.html', context,
        context_instance=RequestContext(request))     

def reflib(request,id):
    if request.user.is_authenticated():
        # already logged in
        context = {}
        lib = UserRefLib.objects.get(id=id)
        if request.user == lib.Owner or request.user in lib.Contributor.all():
            lib = UserRefLib.objects.get(id=id)
            
            context['UserRefLib'] = lib
            context['refs'] = lib.get_refs()
            context['revprj'] = reviewproj.objects.filter(associateLab=lib)        
            return render_to_response('userreflib.html', context,
                 context_instance=RequestContext(request))
        
        else:
            return render_to_response('userreflib.html', {},
                 context_instance=RequestContext(request))
        

    
    else:
        # lead to login or registration
        context = {'LOGIN_URL': settings.LOGIN_URL,
               'REGISTER_URL':settings.REGISTER_URL}

        return render_to_response('home.html', context,
        context_instance=RequestContext(request)) 