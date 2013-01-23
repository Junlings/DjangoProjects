from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.utils import simplejson
from models import Local_Stores_Bestbuy, Local_Stores_Staples, Local_Stores_Target, Local_Stores_Walmart 
from django.core import serializers
#data = serializers.serialize("xml", SomeModel.objects.all())
from django.template import RequestContext
import json

def get_local_staples(request, store_id):   
    #message = {"fact_type": "", "fact_note": ""}
    if request.is_ajax():
        store = get_object_or_404(Local_Stores_Staples, id=store_id)
        json_data = serializers.serialize('json',[store])
        #temp = {'1':1,'2':2}
        #json_data = json.dumps(temp)
        return HttpResponse(json_data, mimetype='application/json')
    else:
        store = get_object_or_404(Local_Stores_Staples, id=store_id)
        json_data = serializers.serialize('json',[store])
        #temp = {'1':1,'2':2}
        #json_data = json.dumps(temp)
        return HttpResponse(json_data, mimetype='application/json')
        #return store

def get_local_staples_state(request):
    if request.is_ajax():
        
        state = request.GET.get('state')
        storequery = Local_Stores_Staples.objects.by_state(state)
        json_data = serializers.serialize('json',storequery)
        return HttpResponse(json_data, mimetype='application/json')
    else:
        storequery = Local_Stores_Staples.objects.by_state(state)
        json_data = serializers.serialize('json',storequery)
        return HttpResponse(json_data, mimetype='application/json')
        #return store   
  

def ajax_storelist(request):
    if request.is_ajax():
        store = get_object_or_404(Local_Stores_Staples, id=1)
        return render_to_response('ajax_search_list.html', {'item_list':[store]},
        context_instance=RequestContext(request))

    else:
        store = get_object_or_404(Local_Stores_Staples, id=1)
        return render_to_response('ajax_search_list.html', {'item_list':[store]},
        context_instance=RequestContext(request))
      
def test_storelist(request):
    return render_to_response('storelist.html', {},
        context_instance=RequestContext(request))
    
def store_map(request):
    return render_to_response('storelist.html', {},
        context_instance=RequestContext(request))

def store_map_search(request):
    if request.is_ajax():
        state = request.GET.get('state')
        store = request.GET.get('store')
        if store  == 'staples':
            storequery = Local_Stores_Staples.objects.by_state(state)
        elif store == 'bestbuy':
            storequery = Local_Stores_Bestbuy.objects.by_state(state)
        elif store == 'target':
            storequery = Local_Stores_Target.objects.by_state(state)
        elif store == 'walmart':
            storequery = Local_Stores_Walmart.objects.by_state(state)
        else:
            storequery = []
            
        json_data = serializers.serialize('json',storequery)
        return HttpResponse(json_data, mimetype='application/json')
        
    else:

        storequery = []
            
        json_data = serializers.serialize('json',storequery)
        return HttpResponse(json_data, mimetype='application/json') 

def find_store(request):
    return render_to_response('search_list_state.html',{'item_list':US_STATES},context_instance=RequestContext(request))
    