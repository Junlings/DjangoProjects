from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from models import companys

def company_list(request):
    p = companys.objects.all()
    fields = ['id','abbrname','type']
    return render_to_response('generic_list_debug.html',{'item_list':p,'fields':fields,'detail_view':''},context_instance=RequestContext(request))


def company_detail(request,id):
    
    
    return render_to_response('generic_list.html',{'item_list':[],'fields':[],'detail_view':''},context_instance=RequestContext(request))
