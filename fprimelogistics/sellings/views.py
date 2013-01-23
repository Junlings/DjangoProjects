# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect
from models import SellDoc, Sellingplatformslot, SellRequest, sell_cost
from forms import SellFilterForm, SellSelectForm
from django.template import RequestContext
from uti.encoder import JSONEncoder
from djangorestframework.serializer import Serializer
from middleware.fileupload import handle_uploaded_file, handle_uploaded_file_BOXNET
from assets.forms import AssetForm, AssetFilterForm
from django.http import HttpResponse,  HttpResponseBadRequest
import datetime
from assets.models import asset

def sell_list(request):
    
    return render_to_response('sell_select.html', {'forms':SellFilterForm(),
                                                    },context_instance=RequestContext(request))

def sell_index(request):
    return render_to_response('sell_index.html', {},
                                                             context_instance=RequestContext(request))
    
def sell_search_monthly(request):
    return render_to_response('sell_select_monthly.html', {'forms':SellSelectForm()},
                                                             context_instance=RequestContext(request))    
    
    
def sell_search(request):
    if request.is_ajax():
        # add purchase filter, get asset group nad
        if request.GET['sell'] != '':
            sellobj = SellRequest.objects.get(pk=request.GET['sell'])
            
            assetobj = sellobj.items.all()
            
            costobj = sell_cost.objects.get(sellingrequest=sellobj)
            
            res = {}
            res['shortname'] = assetobj[0].item.itemproduct.shortname
            res['imagepath'] = assetobj[0].item.itemproduct.mainimagepath
            res['quantity'] = len(list(assetobj))


            

            res['sellprice'] = costobj.sellprice
            res['tax_charged']  = costobj.tax_charged if costobj.tax_charged != None else 0.0
            res['shipping_handling']  = costobj.shipping_handling if costobj.shipping_handling != None else 0.0
            
            res['account_product_tax'] = costobj.account_product_tax.__unicode__()
            res['shipping'] = costobj.shipping if costobj.shipping != None else 0.0
            res['account_shipping'] = costobj.account_shipping.__unicode__() if costobj.account_shipping != None else res['account_product_tax']
            res['financialcharge'] = costobj.financialcharge if costobj.financialcharge != None else 0.0
            res['account_financial'] = costobj.account_financial.__unicode__() if costobj.account_financial != None else res['account_product_tax']
            res['commission'] = costobj.commission if costobj.commission != None else 0.0
            res['account_commission'] = costobj.account_commission.__unicode__() if costobj.account_commission != None else res['account_product_tax']
            
            json_ser = Serializer()
            availdata = json_ser.serialize([res])
            
            avail_json_data = JSONEncoder().encode(availdata)
            return HttpResponse(avail_json_data, mimetype='application/json')
            
        else:
                # filter sell by querydict
            cus_filter = {}
            
            if request.GET['year'] != '' and request.GET['month'] != '':
                
                dateend= datetime.datetime.strptime(str(int(request.GET['month'])+1)+'/01/'+request.GET['year'],"%m/%d/%Y")
                datestart = datetime.datetime.strptime(request.GET['month'] + '/01/'+request.GET['year'],"%m/%d/%Y")
                
                cus_filter['sellingplatformslot__orderon__range'] = [datestart,dateend]

            
            sellobj = SellRequest.objects.filter(**cus_filter).order_by('sellingplatformslot__orderon')
            
            res_list = []
            for obj in sellobj:
                assetobj = obj.items.all()
                res = {}
                res['id'] = obj.id
                res['shortname'] = assetobj[0].item.itemproduct.shortname
                res['imagepath'] = assetobj[0].item.itemproduct.mainimagepath
                res['quantity'] = len(list(assetobj))
                res['platform'] = obj.sale_platform().name
                res['customer'] = obj.custom.__unicode__()
                res['orderon'] = obj.order_on().date()
                res['tracking'] = obj.tracking_number()
                res['fullfilled'] = obj.fullfilled
                res['estimate'] = asset.objects.summarize_estimates(assetobj)
                res_list.append(res)
  
            # get sell summary
            summary = {}
            total_profit = 0
            for item in res_list:
                total_profit += item['estimate']['profit']
                
            summary['profit'] = total_profit
            summary['ntrans'] = len(res_list)
            
            
            json_ser = Serializer()
            availdata = json_ser.serialize([summary,res_list])
            
            avail_json_data = JSONEncoder().encode(availdata)
            return HttpResponse(avail_json_data, mimetype='application/json')               
    
    else:
       
        cus_filter = {}
        
        dateend= datetime.datetime.strptime(str(int(4)+1)+'/01/'+'2012',"%m/%d/%Y")
        datestart = datetime.datetime.strptime('4' + '/01/'+'2012',"%m/%d/%Y")
        
        cus_filter['sellingplatformslot__orderon__range'] = [datestart,dateend]

        
        sellobj = SellRequest.objects.filter(**cus_filter).order_by('sellingplatformslot__orderon')
        
        res_list = []
        for obj in sellobj:
            assetobj = obj.items.all()
            res = {}
            res['id'] = obj.id
            res['shortname'] = assetobj[0].item.itemproduct.shortname
            res['imagepath'] = assetobj[0].item.itemproduct.mainimagepath
            res['quantity'] = len(list(assetobj))
            res['platform'] = obj.sale_platform().name
            res['customer'] = obj.custom.__unicode__()
            res['orderon'] = obj.order_on().date()
            res['tracking'] = obj.tracking_number()
            res['fullfilled'] = obj.fullfilled
            res['estimate'] = asset.objects.summarize_estimates(assetobj)
            res_list.append(res)


        
        json_ser = Serializer()
        availdata = json_ser.serialize(res_list)
        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')        
    