# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core import serializers
from django.template import RequestContext

from models import Supplier, ItemTemplate
from forms import ItemTemplateForm, SupplierForm
import simplejson as json
from resources import ItemTemplateResource
from generic_views.views import dojo_list_view, single_file_upload
from uti.cvs_io import read_css
from uti.encoder import JSONEncoder
from djangorestframework.serializer import Serializer
from product_availbility.models import inventory_results

def Supplies_create_view(request):
    return render_to_response('dojo/dojo_generic_create.html',{'form':ItemTemplateForm(),'base_template':'supply_base.html'},context_instance=RequestContext(request))

def items_create_view(request):
    return render_to_response('dojo/dojo_generic_create.html',{'form':ItemTemplateForm(),'base_template':'supply_base.html'},context_instance=RequestContext(request))


def process_uploaded_file(filename):

    read_css(filename,ItemTemplate)
    return {'create_success':True,'notice_title':'File upload complete'+filename,
            'notice_list':[{'identification_name':"pp",'identification_id':"9"}]}

def Supplies_create_batch_view(request):
    return single_file_upload(request,process_uploaded_file)


def Supplies_add_view(request):
    return render_to_response('add_by_search.html',{},context_instance=RequestContext(request))

def Supplies_add_view_search(request):
    if request.is_ajax():
        storename = request.GET.get('store')
        pid = request.GET.get('pid').strip()
        name = '%s_%s' % (storename,pid)
            
        # first check if the object exists
        inputdict = {'suppliers':{'name':storename},'suppliers_PID':pid}
        
        search_obj = ItemTemplate.objects.get_or_create(**inputdict)
        print 'lllll', search_obj
        json_ser = Serializer()
        availdata = json_ser.serialize(search_obj)
        #avail_json_data = json.dumps(availdata,use_decimal=True)
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')

def Supplies_add_view_local(request):
    if request.is_ajax():
        #state = request.GET.get('state')
        storename = request.GET.get('store')
        pid = request.GET.get('pid').strip()
        zipcode = request.GET.get('zipcode').strip()
        distance = request.GET.get('distance').strip()
        
        name = '%s_%s' % (storename,pid)
            
        # first check if the object exists
        inputdict = {'name':name,'item':{'suppliers':{'name':storename},'suppliers_PID':pid}}
        
        search_obj = inventory_results.objects.get_or_create(**inputdict)
        LOCALSTOREMODEL = search_obj.get_localstore()
        
        query_req = {}
        #if state != 'ALL':
        #    query_req['state'] = state 
        if len(zipcode) == 5:
            query_req['zipcode_distance'] = [zipcode,distance]

        storequery_full = LOCALSTOREMODEL.objects.by_filter(LOCALSTOREMODEL,**query_req)

        # limit store to 20
        #if len(storequery_full) > 20:
        #    storequery = storequery_full[:20]
        #else:
        #    storequery = storequery_full
        #
        storequery = storequery_full
        
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
        raise error

        storequery = []
            
        json_data = serializers.serialize('json',storequery)
        return HttpResponse(json_data, mimetype='application/json')    
    


def Supplies_create_search_view(request):
    return render_to_response('add_by_search.html',{},context_instance=RequestContext(request))

  
def Supplies_create_search_view_post(request):
    
    if request.is_ajax():
        storename = request.GET.get('store')
        pid = request.GET.get('pid').strip()
        
        cls = Supplier.get_cls(storename)
        
        result = cls.obtain_supply(pid)
        
        availdata = result #[1,2,3,4]
        avail_json_data = json.dumps(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')
    
    else:
        storequery = []
            
        json_data = serializers.serialize('json',storequery)
        return HttpResponse(json_data, mimetype='application/json')     
        
    
  
def Supplies_list_view(request):
    #fields = transactions._meta.fields
    fields = ItemTemplateResource.fields
    fields_set = {}

    return dojo_list_view(request,fields,fields_set)
    
def Supplies_index_view(request):
    return render_to_response('supply_index.html',{},context_instance=RequestContext(request))    