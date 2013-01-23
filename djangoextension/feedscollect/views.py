# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from djangorestframework.serializer import Serializer
from django.template import RequestContext
from models import Messages
from uti.encoder import JSONEncoder





def Collect_feeds_action_back(request):

    obj_list = Messages.objects.process()
    #obj_list = Messages.objects.all()
    fields = ['title','updated','author','link']

    if request.is_ajax():
        json_ser = Serializer()
        availdata = json_ser.serialize(obj_list)
        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')
    else:    
        return render_to_response('generic_list_nodetails.html',{'item_list':obj_list,'fields':fields},context_instance=RequestContext(request))


def Collect_feeds_action(request):

    obj_list = Messages.objects.process()
    
    #obj_outputlist = obj_list.filter(updated__gte=last_login)

    
    #obj_list = Messages.objects.all()
    fields = ['title','updated','author','link']

    if request.is_ajax():
        json_ser = Serializer()
        availdata = json_ser.serialize(obj_list)
        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')
    else:    
        return render_to_response('generic_list_nodetails.html',{'item_list':obj_list,'fields':fields},context_instance=RequestContext(request))

    
def Collect_feeds(request):

 
    return render_to_response('feeds_update.html',{},context_instance=RequestContext(request))