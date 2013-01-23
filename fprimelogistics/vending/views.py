# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect
from models import PurchaseDoc, PurchaseRequest, Purchase_cost
from forms import PurchaseDocForm, PurchaseRequestForm, Purchase_costForm, PurchaseDocSelectForm, PurchaseSelectForm
from django.template import RequestContext
from middleware.fileupload import handle_uploaded_file, handle_uploaded_file_BOXNET
from django.db.models import Q
from djangorestframework.serializer import Serializer
from uti.encoder import JSONEncoder
from django.http import HttpResponse,  HttpResponseBadRequest
from django.core import serializers
from django.http import Http404
import json
from middleware.fileupload import handle_uploaded_file, handle_uploaded_file_BOXNET
from assets.forms import AssetForm, AssetFilterForm
import datetime
def purchase_index(request):
    return render_to_response('purchase_index.html', {
                                                    },
                                                             context_instance=RequestContext(request))
    

def purchase_list(request):
    
    return render_to_response('purchase_select.html', {'forms':AssetFilterForm(),
                                                    },
                                                             context_instance=RequestContext(request))
def purchase_list_monthly(request):
    
    return render_to_response('purchase_select_monthly.html', {'forms':PurchaseSelectForm(),
                                                    },
                                                             context_instance=RequestContext(request))
    
def purchase_search(request):
    if request.is_ajax():
        # add purchase filter, get asset group nad
        if 'purchase' in request.GET.keys() and request.GET['purchase'] != '':
            purobj = PurchaseRequest.objects.get(pk=request.GET['purchase'])
            costobj = Purchase_cost.objects.get(request=purobj)
            
            res = {}
            res['shortname'] = purobj.item.itemproduct.shortname
            res['imagepath'] = purobj.item.itemproduct.mainimagepath
            res['quantity'] = purobj.quantity
            res['storage'] = purobj.storage.nickname
            res['person'] = purobj.person.username

            
            
            res['productcost'] = costobj.productcost
            res['tax']  = costobj.tax if costobj.tax != None else 0.0
            res['account_product_tax'] = costobj.account_product_tax.__unicode__()
            res['shipping'] = costobj.shipping if costobj.shipping != None else 0.0
            res['account_shipping'] = costobj.account_shipping.__unicode__() if costobj.account_shipping != None else res['account_product_tax']
            res['commission'] = costobj.commission if costobj.commission != None else 0.0
            res['account_commission'] = costobj.account_commission.__unicode__() if costobj.account_commission != None else res['account_product_tax']
            json_ser = Serializer()
            availdata = json_ser.serialize([res])

        else:  # querybase search
            cus_filter = {}
            
            if request.GET['year'] != '' and request.GET['month'] != '':
                
                dateend= datetime.datetime.strptime(str(int(request.GET['month'])+1)+'/01/'+request.GET['year'],"%m/%d/%Y")
                datestart = datetime.datetime.strptime(request.GET['month'] + '/01/'+request.GET['year'],"%m/%d/%Y")
                
                cus_filter['orderon__range'] = [datestart,dateend]
                
                purchaseobj = PurchaseRequest.objects.filter(**cus_filter).order_by('orderon')
                
                res_list = []
                for obj in purchaseobj:
                    assetobj = obj.assets.all()
                    res = {}
                    res['id'] = obj.id
                    res['shortname'] = assetobj[0].item.itemproduct.shortname
                    res['imagepath'] = assetobj[0].item.itemproduct.mainimagepath
                    res['quantity'] = len(list(assetobj))
                    res['orderon'] = obj.orderon.date()
                    res_list.append(res)
                
            json_ser = Serializer()
            availdata = json_ser.serialize(res_list)

        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')      
    
    else:
       
        purobj = PurchaseRequest.objects.get(pk=2)

        res = {}
        res['shortname'] = purobj.item.itemproduct.shortname
        res['imagepath'] = purobj.item.itemproduct.mainimagepath
        res['quantity'] = purobj.quantity
        res['storage'] = purobj.storage.nickname
        res['person'] = purobj.person.username
        json_ser = Serializer()
        availdata = json_ser.serialize([res])

        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')           
    
def purchase_create_addfile(request):

    if request.method == 'POST': # If the form has been submitted...
        
        purchasedoc_data = request.POST.copy()
        docform = PurchaseDocForm(data=purchasedoc_data,files=request.FILES)

        if docform.is_valid():
            filename = handle_uploaded_file(request.FILES['doc'])
            docform.files = filename
            docform.save()

            #handle_uploaded_file_BOXNET(request,filename)
                
            return HttpResponseRedirect('success/') # Redirect to details
        else:
            return HttpResponseRedirect('fail/') # Redirect to details
        
        # try backup at box.net
        
    else:
        form = PurchaseDocForm() # An unbound form

    return render_to_response('generic_create_form.html', {'form_list':[form],
                                        'form_display_mode_table':True,
                                        'form_is_multipart':True},
             context_instance=RequestContext(request))


def purchase_create_ajax(request):
    if request.method == 'POST': # If the form has been submitted...    
        if request.is_ajax():           
            post_data = request.POST.copy()
            post_data = json.loads(post_data.keys()[0])  # need to fix that, now all inputs are as key
            
            print request.FILES
            
            purchaseRequestForm = PurchaseRequestForm(post_data['id_purchaseRequestForm'] or None)
            purchase_costForm = Purchase_costForm(post_data['id_purchase_costForm'] or None)
            purchaseDocForm = PurchaseDocForm(post_data['id_purchaseDocForm'] or None)
            #form4 = PurchaseDocForm(request.POST or None)
            
            if purchaseRequestForm.is_valid() and purchase_costForm.is_valid():
                if purchaseDocForm.is_valid():
                    filename = handle_uploaded_file(request.FILES['doc'])
                    purchaseDocForm.files = filename
            
                    purchaseDocForm_instance = purchaseDocForm.save()
                else:
                    purchaseDocForm_instance = None
                    
                purchase_cost_instance = purchase_costForm.save()
                asset_group_instance = purchaseRequestForm.save(cost=purchase_cost_instance,
                                                                person=request.user,
                                                                docs=purchaseDocForm_instance)
                


                json_ser = Serializer()
                availdata = json_ser.serialize([asset_group_instance])
                avail_json_data = JSONEncoder().encode(availdata)
                
                return HttpResponse(avail_json_data, mimetype='application/json')
                
            else:
                json_ser = Serializer()
                availdata = json_ser.serialize({'id_purchaseRequestForm':purchaseRequestForm.errors,
                                                'id_purchase_costForm':purchase_costForm.errors,
                                                'id_purchaseDocForm':purchaseDocForm.errors})
        
                avail_json_data = JSONEncoder().encode(availdata)
                return HttpResponseBadRequest(avail_json_data, mimetype='application/json',status=400)                



def purchase_create(request):
    
    docsselections = PurchaseDoc.objects.filter(id in [1,2])
    purchaseDocSelectForm = PurchaseDocSelectForm(initial={'queryset':PurchaseDoc.objects.all()})
    
    purchaseRequestForm = PurchaseRequestForm()
    purchase_costForm = Purchase_costForm()    
        
    return render_to_response('dojo/dojo_generic_create_multiple.html', {'form_list':[
                                                                {'form':purchaseRequestForm,'id':"purchaseRequestForm"},
                                                                {'form':purchase_costForm,'id':"purchase_costForm"},
                                                                {'form':purchaseDocSelectForm,'id':"purchaseDocSelectForm"}],
                                                               'form_display_mode_table':True,
                                                               'form_is_multipart':True,
                                                               'target':'ajax/'},
             context_instance=RequestContext(request))    
    


''' views for prchase docs '''


def purchasedoc_create_process(request,object_id):
    #raise TypeError
    purchase = get_object_or_404(Purchase, pk=object_id)
    if request.method == 'POST': # If the form has been submitted...
        
        purchasedoc_data = request.POST.copy()
        docform = PurchaseDocForm(data=purchasedoc_data,files=request.FILES,purchase=purchase)

        if docform.is_valid():
            filename = handle_uploaded_file(request.FILES['doc'])
            docform.files = filename
            docform.save()

            handle_uploaded_file_BOXNET(request,filename)
                
            return HttpResponseRedirect(ROOT_URL + 'user/purchasedocs/create/success/') # Redirect to details
        else:
            return HttpResponseRedirect(ROOT_URL + 'user/purchases/create/fail/') # Redirect to details
        
        # try backup at box.net
        
    else:
        form = ContactForm() # An unbound form

    return render_to_response('contact.html', {
        'form': form,
    })
    
def purchasedoc_create_success(request):
    
    
    return render_to_response('purchasedoc_create_success.html', {},context_instance=RequestContext(request))
        
        