# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core import serializers
from django.template import RequestContext
from django.db.models import Q

from stores.models import Local_Stores_Bestbuy, Local_Stores_Staples, Local_Stores_Target, Local_Stores_Walmart
from forms import CheckForm, ItemForm
#from purchases.models import Supplier, ItemTemplate
import time
from django.contrib.localflavor.us.us_states import US_STATES
#from checker import checker_bestbuy, checker_staples, checker_target, checker_walmart
import json

from models import inventory_results
from supply.models import ItemTemplate, Supplier

def search(request):
    return render_to_response('search.html', {},
        context_instance=RequestContext(request))    


def create_newitem(storename,state,pid,search_interval='1 day'):
    name = '%s_%s_%s' % (storename,state,pid)
    
    tempdict = {"manufacturer":'default',
                "shortname":storename+'_'+pid,
                "longname":'unknown',
                "modelid":'unknown',
                "mainimagepath":None,
                "suppliers":storename,
                "suppliers_PID":pid }

    newitemtemplate = ItemTemplate.batch_create(tempdict)

    newitem = inventory_results(name=name,item=newitemtemplate,search_interval=search_interval)    
    newitem.save()
    return newitem


def search_inventory(request):
    if request.is_ajax():
        state = request.GET.get('state')
        storename = request.GET.get('store')
        pid = request.GET.get('pid').strip()
        name = '%s_%s' % (storename,pid)
            
        # first check if the object exists
        inputdict = {'name':name,'item':{'suppliers':{'name':storename},'suppliers_PID':pid}}
        
        search_obj = inventory_results.objects.get_or_create(**inputdict)
            

        # get storequery
        storequery = search_obj.by_state(state)
        print storequery
        
        
        # check if need to re-search
        re_search_id = search_obj.if_search(storequery)

        if re_search_id != 0 :  # do re-search
            print 'do search code', re_search_id
            print 'start new inventory search, please wait'
            
            availdata = []
            availdata = search_obj.inventory_search(storename,storequery)

                
        else:  # do not do re-search      
            print 'Try load previous inventory search'
            try:
                availdata = search_obj.load_latest(storequery)
                print 'Successfully load previous inventory search'
                
            except:  # if load error, maybe first search or latest file broke
                print 'load inventory result failed, re do the research now, please wait'
                availdata = search_obj.inventory_search(pid,storename,storequery)
            
            
        avail_json_data = json.dumps(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')
        
    else:
        state = request.GET.get('state')
        storename = request.GET.get('store')
        pid = request.GET.get('pid').strip()
        name = '%s_%s' % (storename,pid)
            
        # first check if the object exists
        inputdict = {'name':name,'item':{'suppliers':{'name':storename},'suppliers_PID':pid}}
        
        search_obj = inventory_results.objects.get_or_create(**inputdict)
            

        # get storequery
        storequery = search_obj.by_state(state)[0:10]
        print storequery
        
        
        # check if need to re-search
        re_search_id = search_obj.if_search(storequery)

        if re_search_id != 0 :  # do re-search
            print 'do search code', re_search_id
            print 'start new inventory search, please wait'
            
            availdata = []
            availdata = search_obj.inventory_search(storename,storequery)

                
        else:  # do not do re-search      
            print 'Try load previous inventory search'
            try:
                availdata = search_obj.load_latest(storequery)
                print 'Successfully load previous inventory search'
                
            except:  # if load error, maybe first search or latest file broke
                print 'load inventory result failed, re do the research now, please wait'
                availdata = search_obj.inventory_search(pid,storename,storequery)
            
            
        avail_json_data = json.dumps(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')        
        
        
        
        '''
        raise error

        storequery = []
            
        json_data = serializers.serialize('json',storequery)
        return HttpResponse(json_data, mimetype='application/json')     
        '''
