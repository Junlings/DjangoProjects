from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from financial.models import accounts
from vending.models import PurchaseRequest
from inventory.models import storage
from sellings.models import SellRequest, Sellingplatformslot
from assets.models import asset

def home(request):
    if request.user.is_authenticated():
        # already logged in
        
        myaccounts = accounts.objects.filter(owner=request.user)
        mystorages = storage.objects.filter(owner=request.user)
        
        latest_purchase = PurchaseRequest.objects.filter()#person=request.user)
        latest_sell= Sellingplatformslot.objects.all()
        asset_onsale = asset.objects.summarize_onsale()
        asset_instock = asset.objects.summarize_instock()
        
        context = {'user':request.user,
                   'REGISTER_URL': settings.REGISTER_URL,
                   'ROOT_URL':settings.ROOT_URL,
                   'accounts':myaccounts,
                   'storages':mystorages,
                   'latest_Purchase':latest_purchase.order_by('-orderon')[:10],
                   'latest_Sell':latest_sell.order_by('-orderon')[:10],
                   'asset_onsale':asset_onsale,
                   'asset_instock':asset_instock,
                   }
        return render_to_response('userhome.html', context,
             context_instance=RequestContext(request))
    
    else:
        # lead to login or registration
        context = {'LOGIN_URL': settings.LOGIN_URL,
               'REGISTER_URL':settings.REGISTER_URL}

        return render_to_response('home.html', context,
        context_instance=RequestContext(request))     

