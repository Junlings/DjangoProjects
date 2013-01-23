from assets.models import asset, assetgroup, assetstorage
from financial.models import transactions, accounts, TransactionConfirmDebit, TransactionConfirmCredit
from models import PurchaseDoc, PurchaseRequest, Purchase_cost
from django.contrib.contenttypes.models import ContentType
from inventory.models import storage
import datetime

def Commit_vending_fullfill(purchaserequest):
    # create group first
    groupname = purchaserequest.__unicode__()
    assetgroupinst = assetgroup(name=groupname)
    assetgroupinst.save()
    


    
    # create asset and add to group
    for j in range(0,purchaserequest.quantity):
        FSIN = str(purchaserequest.id).zfill(6)+str(j).zfill(6)
        assetinst = asset(item=purchaserequest.item,FSIN=FSIN)
        assetinst.save()
        
        # add default storage
        assetstorageinst = assetstorage(item=assetinst,location=purchaserequest.storage)
        assetstorageinst.save()
        
        # add asset to purchase asset group
        assetgroupinst.assets.add(assetinst)
        purchaserequest.assets.add(assetinst)
    # change fullfill status
    purchaserequest.fullfilled = True
    purchaserequest.save()


        
def record_purchase_transaction(purchaserequest):
    purchasecost = Purchase_cost.objects.get(request=purchaserequest)
    asset_account = accounts.objects.get(nickname='assets')
    expanse_tax_account = accounts.objects.get(nickname='expanse_tax')
    expanse_shipping_account = accounts.objects.get(nickname='expanse_shipping')
    expanse_commission_account = accounts.objects.get(nickname='expanse_commision')
    
    record_transaction_basic(asset_account,
                             purchasecost.account_product_tax,
                             purchasecost,
                             'productcost',lastmodified=purchaserequest.orderon)
    
    if purchasecost.account_product_tax != '0.0' and purchasecost.account_product_tax != None:
        record_transaction_basic(expanse_tax_account,
                                 purchasecost.account_product_tax,
                                 purchasecost,
                                 'tax',lastmodified=purchaserequest.orderon)
        
    if purchasecost.account_shipping != '0.0' and purchasecost.account_shipping != None:
        record_transaction_basic(expanse_shipping_account,
                                 purchasecost.account_shipping,
                                 purchasecost,
                                 'shipping',lastmodified=purchaserequest.orderon)
    if purchasecost.account_commission != '0.0' and purchasecost.account_commission != None:
        record_transaction_basic(expanse_commission_account,
                                 purchasecost.account_commission,
                                 purchasecost,
                                 'commission',lastmodified=purchaserequest.orderon)

    
def record_transaction_basic(credit_account,debit_account,minstance,fieldname,notes='',lastmodified=None):
    ''' this is the generic transaction generator
        the amount will be retrived from the model at designated field
    '''
    objtype = ContentType.objects.get_for_model(minstance) #'PurchaseRequest') 
    objid = minstance.id
    amount = minstance.__dict__[fieldname]
    
    if lastmodified == None:
        lastmodified = datetime.datetime.now()
        
    if amount != 'null' and amount != None and float(amount) != 0.0:
        record_transaction_ini(credit_account,debit_account,amount,notes,objtype,objid,fieldname,lastmodified)


def record_transaction_ini(credit_account,debit_account,amount,notes,objtype,objid,fieldname,lastmodified,fullfilled=False):
    inputdict = {'accountA':credit_account,
                 'modeA':'credit',
                 'accountB':debit_account,
                 'modeB':'debit',
                 'amount':amount,
                 'notes':notes,
                 'lastmodified':lastmodified,
                 'fullfilled':fullfilled}
    
    if objtype != None and objid != None:
        inputdict['content_type'] = objtype
        inputdict['object_id'] = objid
        inputdict['fieldname'] = fieldname
        
    trans = transactions(**inputdict)
    #print trans
    trans.save()
    
    dd = TransactionConfirmDebit(transaction=trans)
    cc = TransactionConfirmCredit(transaction=trans)
    
    dd.save()
    cc.save()
    
    
    
    