import datetime
import os
from django.db import models
from financial.models import accounts
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from supply.models import ItemTemplate
from shipping.models import shipments
from inventory.models import storage
from assets.models import asset

PURCHASE_STATES = (
    ('Requested', 'Order Requested'),
    ('Placed', 'Order Placed'),
    ('Refunded', 'Purchased Items refunded'),
    ('Refused', 'Refunded Refused'),
)

PURCHASE_DOC_TYPES =(
    ('ItemReceipt', 'Purchase receipt'),
    ('ItemPhoto', 'Item Photo'),
    ('Other', 'Other'),
)


class PurchasecostManager(models.Manager):
    def states_for_purchase(self, purchase):
        return self.filter(purchase=purchase)
        







class PurchaseRequest(models.Model):
    ''' the location of the products'''
    person = models.ForeignKey(User, verbose_name=_(u"Submit Person"))
    item = models.ForeignKey(ItemTemplate, verbose_name=_(u"item"))
    assets = models.ManyToManyField(asset, verbose_name=_(u"Assets"), null=True, blank=True)
    
    storage = models.ForeignKey(storage, verbose_name=_(u"ship to/storage location"))
    quantity = models.PositiveIntegerField()
    orderon = models.DateTimeField(verbose_name=_(u"Order placed date"),blank=True,null=True)
    order_id = models.CharField(max_length=1000,verbose_name=_(u"Order Id"),blank=True,null=True)    
    fullfilled = models.BooleanField(verbose_name=_("Fullfilled?"),default=False)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Purchase Request")
        verbose_name_plural = _(u"Purchases Request")
        
    def __unicode__(self):
        return _(u"Purchase Request %(id)s: %(quantity)s %(name)s") % {'id':self.id,'quantity':self.quantity,'name':self.item.__unicode__()}

    def docs_count(self):
        docs = PurchaseDoc.objects.filter(request=self)
        namelist = []
        
        for doc in docs:
            namelist.append(doc.filename())
        return namelist
    
    def account_info(self):
        
        cost = Purchase_cost.objects.get(request=self)
        return cost.account_product_tax.__unicode__()
        
    
    
class PurchaseDoc(models.Model):

    type = models.CharField(max_length=50, choices=PURCHASE_DOC_TYPES,verbose_name=_(u'type'),blank=True)
    date = models.DateTimeField(verbose_name=_(u"date"), auto_now_add=True)
    doc = models.FileField(upload_to='doc/purchase/%Y/%m/%d',verbose_name=_(u"document"),blank=True)
    request = models.ForeignKey(PurchaseRequest,verbose_name=_(u"Purchase request"))
    
    
    class Meta:
        verbose_name = _(u"Purchase Document")
        verbose_name_plural = _(u"Purchase Documents")
        
    def __unicode__(self):
        return _(u"Docs id=%(id)s, upload on %(date)s") % {'id':self.id, 'date':self.date}
    def filename(self):
        return os.path.basename(self.doc.name)        

class Purchase_cost(models.Model):
    ''' This is the model to quantify the cost of certain purchase'''
    request = models.OneToOneField(PurchaseRequest,verbose_name=_(u"Purchase request"))
    
    productcost = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Total product cost before tax"))
    tax = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Total Tax charged"),default=0.0)
    account_product_tax = models.ForeignKey(accounts, verbose_name=_(u"purchase account"),related_name='purchase')
    
    shipping = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"total shipping cost"),blank=True,null=True,default=0.0)
    account_shipping = models.ForeignKey(accounts, verbose_name=_(u"shipping account"),related_name='purchase_shipping',blank=True,null=True)
    shippment = models.ForeignKey(shipments, verbose_name=_(u"shipments"),blank=True,null=True)
    
    commission = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Purchase commission cost"),blank=True,null=True,default=0.0)
    account_commission = models.ForeignKey(accounts, verbose_name=_(u"Commision account"),related_name='purchase_comission',blank=True,null=True)
    
    total_cost = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Total purchase cost"),editable=False, null=True, blank=True)
    
    objects = PurchasecostManager()
    
    class Meta:
        verbose_name = _(u"Purchase cost")
        verbose_name_plural = _(u"Purchase costs")
        
    def __unicode__(self):
        return _(u"%(info)s") % {'info':self.request.__unicode__()}
        
