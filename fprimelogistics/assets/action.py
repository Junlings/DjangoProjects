from models import asset, assetgroup, assetstorage, assetestimate
from vending.models import PurchaseRequest, Purchase_cost
from sellings.models import SellRequest, sell_cost, Sellingplatformslot
from decimal import Decimal

def update_estimate(assetobj):
    try:
        estimateobj = assetestimate.objects.get(asset=assetobj)
   
    except:
        estimateobj = assetestimate(asset=assetobj)
        estimate_data = {}
        estimate_data["cost_purchase_product"] = '0.0'
        estimate_data["cost_purchase_tax"] = '0.0'
        estimate_data["cost_purchase_shipping"] = '0.0'
        estimate_data["cost_purchase_commision"] = '0.0'
        estimate_data["earn_product"] = '0.0'
        estimate_data["earn_tax"] = '0.0'
        estimate_data["earn_shipping"] = '0.0'
        estimate_data["cost_sell_tax"] = '0.0'
        estimate_data["cost_sell_shipping"] = '0.0'
        estimate_data["cost_sell_platform"] = '0.0'
        estimate_data["cost_sell_financial"] = '0.0'
        estimate_data["cost_sell_commission"] = '0.0'    
        
        estimateobj.__dict__.update(**estimate_data)
        estimateobj.save()        
        


    # try pull sell record
    try:
        sellreq = SellRequest.objects.get(items=assetobj)
        sellquantity = len(list(sellreq.items.all()))
        
        try:
            sellslot = Sellingplatformslot.objects.get(request=sellreq)
        except:
            sellslot = None
            
    except:
        sellreq = None
        selldoc = None
        sellslot = None
        
    purchasereq = PurchaseRequest.objects.get(assets=assetobj)
    purchasecost = Purchase_cost.objects.get(request=purchasereq)
    
    if sellreq != None:
        sellcost = sell_cost.objects.get(sellingrequest=sellreq)
    
    estimate_data = {}
    estimate_data['asset'] = assetobj
    estimate_data["cost_purchase_product"] = purchasecost.productcost/purchasereq.quantity if purchasecost.productcost != None else '0.0'
    estimate_data["cost_purchase_tax"] = purchasecost.tax/purchasereq.quantity if purchasecost.tax != None else '0.0'
    estimate_data["cost_purchase_shipping"] = purchasecost.shipping/purchasereq.quantity if purchasecost.shipping != None else '0.0'
    estimate_data["cost_purchase_commision"] = purchasecost.commission/purchasereq.quantity if purchasecost.commission != None else '0.0'
    
    if sellreq != None:
        estimate_data["earn_product"] = sellcost.sellprice/sellquantity if sellcost.sellprice != None else '0.0'
        estimate_data["earn_tax"] = sellcost.tax_charged/sellquantity if sellcost.tax_charged != None else '0.0'
        estimate_data["earn_shipping"] = sellcost.shipping_handling/sellquantity if sellcost.shipping_handling != None else '0.0'
        estimate_data["cost_sell_tax"] = '0.0'
        estimate_data["cost_sell_shipping"] = sellcost.shipping/sellquantity if sellcost.shipping != None else '0.0'
        estimate_data["cost_sell_platform"] = sellcost.commission/sellquantity if sellcost.commission != None else '0.0'
        estimate_data["cost_sell_financial"] = sellcost.financialcharge/sellquantity if sellcost.financialcharge != None else '0.0'
        estimate_data["cost_sell_commission"] = '0.0'

        
    estimateobj.__dict__.update(**estimate_data) 
    estimateobj.save()