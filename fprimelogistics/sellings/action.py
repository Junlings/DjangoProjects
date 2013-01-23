from assets.models import asset, assetgroup, assetstorage
from financial.models import transactions, accounts, TransactionConfirmDebit, TransactionConfirmCredit
from models import SellRequest, sell_cost, Sellingplatformslot
from django.contrib.contenttypes.models import ContentType
from inventory.models import storage
import datetime
from vending.action import record_transaction_basic

def Commit_selling_fullfill(sellrequest):
    
    for asset in sellrequest.items.all():
        # 1) Add moveout data to the last storage and change asset status
        storageobj = asset.curent_stoarge()
        storageobj.moveout = datetime.datetime.now()
        storageobj.save()
        
        # 2) change sell request status to sold
        asset.sold = True
        asset.save()
    
    #3) change the sell request    
    sellrequest.fullfilled = True
    sellrequest.save()


        
def record_sell_transaction(sellrequest):
    sellcost = sell_cost.objects.get(sellingrequest=sellrequest)
    asset_account = accounts.objects.get(nickname='assets')
    expanse_tax_account = accounts.objects.get(nickname='expanse_tax')
    expanse_shipping_account = accounts.objects.get(nickname='expanse_shipping')
    expanse_commission_account = accounts.objects.get(nickname='expanse_commision')
    income_account = accounts.objects.get(nickname='income')#,owner__username='fprimes')

    orderon = Sellingplatformslot.objects.get(request=sellrequest).orderon
    record_transaction_basic(sellcost.account_product_tax,
                             asset_account,         # credit
                             sellcost,
                             'sellprice',lastmodified=orderon)
    
    if sellcost.tax_charged != 0 and sellcost.tax_charged != None:
        record_transaction_basic(sellcost.account_product_tax,
                                 expanse_tax_account,
                                 sellcost,
                                 'tax_charged',lastmodified=orderon)

    if sellcost.shipping_handling != 0 and sellcost.shipping_handling != None:
        record_transaction_basic(sellcost.account_product_tax,
                                 expanse_shipping_account,
                                 sellcost,
                                 'shipping_handling',lastmodified=orderon)
        
        
        
    if float(sellcost.shipping) != 0 and sellcost.shipping != None:
        debit_account = sellcost.account_shipping if sellcost.account_shipping != None else  sellcost.account_product_tax
        record_transaction_basic(expanse_shipping_account,
                                 debit_account,
                                 sellcost,
                                 'shipping',lastmodified=orderon)
        
    if float(sellcost.commission) != 0 and sellcost.commission != None:
        debit_account = sellcost.account_commission if sellcost.account_commission != None else  sellcost.account_product_tax
        record_transaction_basic(expanse_commission_account,
                                 debit_account,
                                 sellcost,
                                 'commission',lastmodified=orderon)

    if float(sellcost.financialcharge) != 0 and sellcost.financialcharge != None:
        debit_account = sellcost.account_financial if sellcost.account_financial != None else  sellcost.account_product_tax
        record_transaction_basic(expanse_commission_account,
                                 debit_account,
                                 sellcost,
                                 'financialcharge',lastmodified=orderon)    
    