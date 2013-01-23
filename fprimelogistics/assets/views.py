# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.template import RequestContext
from django.core import serializers
from models import asset, assetstorage, assetgroup, assetestimate
from forms import AssetForm, AssetFilterForm
from uti.encoder import JSONEncoder
#from resources import AssetResource
from generic_views.views import dojo_list_view, single_file_upload
from uti.cvs_io import read_css
from djangoextension.djangorestframework.serializer import Serializer

from inventory.models import storage
from vending.models import PurchaseRequest, PurchaseDoc, Purchase_cost
from sellings.models import SellRequest,Sellingplatformslot, sell_cost, SellDoc

def Asset_create_view(request):
    """ asset create, not activated """
    return render_to_response('dojo/dojo_generic_create.html',{'form':AssetForm()},context_instance=RequestContext(request))
 
def Asset_index(request):
    """ index page with """
    return render_to_response('asset_index.html', {}, context_instance=RequestContext(request))


def Asset_list_view(request):
    """ asset select search view """
    return render_to_response('asset_select.html', {'forms':AssetFilterForm(),
                                                    }, context_instance=RequestContext(request))

def Asset_details(request,FSIN):
    """ detail view """
    assetobj = asset.objects.get(FSIN=FSIN)
    storageobjs = assetstorage.objects.filter(item=assetobj)
    purchasereq = PurchaseRequest.objects.get(assets=assetobj)

    # try pull purchase document record
    try:
        purchasedoc = PurchaseDoc.objects.filter(request=purchasereq)
    except:
        purchasedoc = None  
    
    # try pull sell record
    try:
        sellreq = SellRequest.objects.get(items=assetobj)
        sellquantity = len(list(sellreq.items.all()))
        
        try:
            sellslot = Sellingplatformslot.objects.get(request=sellreq)
        except:
            sellslot = None
        
        try:
            selldoc = SellDoc.objects.get(sellingrequest=sellreq)
        except:
            selldoc = None
    except:
        sellreq = None
        selldoc = None
        sellslot = None
    
    # try pull profit estimation record

    estimateobj = assetestimate.objects.get(asset=assetobj)
    return render_to_response('asset_details.html', {'asset':assetobj,
                                                     'purchasereq':purchasereq,
                                                     'purchasedoc':purchasedoc,
                                                     'sellreq':sellreq,
                                                     'selldoc':selldoc,
                                                     'sellslot':sellslot,
                                                     'storageobjs':storageobjs,
                                                     'estimateobj':estimateobj,
                                                    },
                                                             context_instance=RequestContext(request))

def Asset_list_user_view(request):

    location,prod_dict = asset.objects.user_instock(request)
    print location,prod_dict
    return render_to_response('asset_select_user.html', {'storage':location,'asset_instock':prod_dict,
                                                    },
                                                             context_instance=RequestContext(request))    
    
    

def Asset_list_view_search(request):
    """ search engine view """
    if request.is_ajax():
        cus_filter = {}
        obj_list = asset.objects.all()
        
        # add storage filter
        if request.GET['storage'] != '':
            location = storage.objects.get(pk=request.GET['storage'])
            cus_filter['assetstorage__location'] = location
            cus_filter['assetstorage__moveout'] = None
        
        # add onsale filter
        if request.GET['onsale'] == '2':
            cus_filter['onsale'] = True
        elif request.GET['onsale'] == '3':
            cus_filter['onsale'] = False

        # add sold filter
        if request.GET['sold'] == '2':
            cus_filter['sold'] = True
        elif request.GET['sold'] == '3':
            cus_filter['sold'] = False
            
        # add purchase filter, get asset group nad
        if request.GET['purchase'] != '':
            purobj = PurchaseRequest.objects.get(pk=request.GET['purchase'])
            groupname = 'Purchase Request %i:' % purobj.id
            assetgroupobj = assetgroup.objects.get(name__startswith=groupname)
            obj_list = obj_list & assetgroupobj.assets.all()
            
        if request.GET['sell_platform'] != '':
            #sellslotobjs = Sellingplatformslot.objects.filter(platform__id=request.GET['sell_platform'])
            #sellrequobjs = SellRequest.objects.filter(sellingplatformslot__platform__id=request.GET['sell_platform'])
            obj_list = obj_list & asset.objects.filter(sellrequest__sellingplatformslot__platform__id=request.GET['sell_platform'])

        obj_list = obj_list.filter(**cus_filter) #onsale=True,item__itemproduct__shortname=u'Xbox 360 Wireless')
        json_ser = Serializer()
        availdata = json_ser.serialize(obj_list)
        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')  
        
    else:
        obj_list = asset.objects.filter(onsale=True,item__itemproduct__shortname=u'Xbox 360 Wireless')
               
        json_ser = Serializer()
        availdata = json_ser.serialize(obj_list)
        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')        