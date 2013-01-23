import datetime
import os
from django.db import models
from djangoextension.financial.models import accounts
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from assets.models import asset
from shipping.models import shipments
from customer.models import customers


SELL_STATES = (
    ('Listed', 'Lised on the website'),
    ('Sold', 'Sold indicted'),
    ('Paid', 'Custom make the payment'),
    ('Settled', 'Funds transferred to company account'),
    ('shipped', 'Product shipped'),
)

SELL_DOC_TYPES =(
    ('Order slip', 'Order details send to customer'),
    ('picture-sn', 'picture-sn'),
    ('picture-package', 'picture-package'),
    ('Other', 'Other'),
)

class SellRequest(models.Model):
    ''' the location of the products'''
    items = models.ManyToManyField(asset, verbose_name=_(u"Items Selling"))
    custom = models.ForeignKey(customers, verbose_name=_(u"Customer"))
    fullfilled = models.BooleanField(verbose_name=_("Fullfilled?"),default=False)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Sell Request")
        verbose_name_plural = _(u"Sells Request")
        
    def __unicode__(self):
        #return _(u"Sell Request: %(id)s of %(items)s") % {'id':self.id, 'items':self.item_list()}
        return _(u"Sell Request: %(id)s on %(items)s") % {'id':self.id, 'items':self.items.all()[0]}
    
    def item_list(self):
        list = []
        for items in self.items.all():
            list.append(items.__unicode__())
        
        return list[0] + 'x'+str(len(list)) 
    
    def item_num(self):
        list = []
        for items in self.items.all():
            list.append(items.__unicode__())
        
        return str(len(list)) 

        
    def sale_platform(self):
        sellslot = Sellingplatformslot.objects.get(request=self)
        return sellslot.platform

    
    def tracking_number(self):
        try:
            cost = sell_cost.objects.get(sellingrequest=self)
        
            return cost.shippment.tracking
        except:
            return None
        
    def sale_URL(self):
        sellslot = Sellingplatformslot.objects.get(request=self)
        return sellslot.url

    def order_id(self):
        sellslot = Sellingplatformslot.objects.get(request=self)
        return sellslot.order_id

    def order_on(self):
        sellslot = Sellingplatformslot.objects.get(request=self)
        return sellslot.orderon

    def create_on(self):
        sellslot = Sellingplatformslot.objects.get(request=self)
        return sellslot.createdon
    
    def fee_platform(self):
        cost = sell_cost.objects.get(sellingrequest=self)
        return cost.commission
        
    '''    
    def total_income(self):
        cost = sell_cost.objects.get(sellingrequest=self)
        return str(cost.sellprice + cost.tax_charged+cost.shipping_handling)# + '@' + cost.account_product_tax.__unicode__()

    def total_deducation(self):
        cost = sell_cost.objects.get(sellingrequest=self)
        return str(cost.shipping + cost.financialcharge+cost.commission)

    def net_earn(self):
        cost = sell_cost.objects.get(sellingrequest=self)
        return str(cost.sellprice + cost.tax_charged+cost.shipping_handling-cost.shipping - cost.financialcharge-cost.commission)
    '''
    
    
class sell_cost(models.Model):
    ''' This is the model to quantify the cost of certain purchase'''
    sellingrequest = models.OneToOneField(SellRequest, verbose_name=_(u"Selling Request"))
    
    sellprice = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Total product sale price"),default=0.0)
    tax_charged = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Tax charged"),default=0.0)
    shipping_handling = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"S/H charged"),default=0.0)
    account_product_tax = models.ForeignKey(accounts, verbose_name=_(u"purchase account"),related_name='selling')
    
    shipping = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"total shipping cost"),blank=True,null=True,default=0.0)
    account_shipping = models.ForeignKey(accounts, verbose_name=_(u"shipping account"),related_name='selling_shipping',blank=True,null=True)
    shippment = models.ForeignKey(shipments, verbose_name=_(u"shipments"),blank=True,null=True)
    
    
    financialcharge = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Financial Transaction Charge"),blank=True,null=True,default=0.0)
    account_financial = models.ForeignKey(accounts, verbose_name=_(u"Financial Transaction account"),related_name='selling_financial',blank=True,null=True)
    
    
    commission = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Selling platform commission cost"),blank=True,null=True,default=0.0)
    account_commission = models.ForeignKey(accounts, verbose_name=_(u"Commision platform account"),related_name='selling_comission',blank=True,null=True)
    
    net_income = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"net income"),editable=False,blank=True,null=True)
    
    class Meta:
        verbose_name = _(u"Selling charge")
        verbose_name_plural = _(u"Selling charge")
        
    def __unicode__(self):
        return _(u"%(info)s") % {'info':self.sellingrequest.__unicode__()}


class SellDoc(models.Model):
    sellingrequest = models.ForeignKey(SellRequest, verbose_name=_(u"Selling Request"))
    
    type = models.CharField(max_length=50, choices=SELL_DOC_TYPES,verbose_name=_(u'type'),blank=True)
    date = models.DateTimeField(verbose_name=_(u"date"), auto_now_add=True)
    doc = models.FileField(upload_to='doc/sell/%Y/%m/%d',verbose_name=_(u"document"),blank=True)
    
    class Meta:
        verbose_name = _(u"Sell Document")
        verbose_name_plural = _(u"Sell Documents")
        
    def __unicode__(self):
        return _(u"Docs id=%(id)s, upload on %(date)s") % {'id':self.id, 'date':self.date}
    def filename(self):
        return os.path.basename(self.doc.name)




class Sellingplatform(models.Model):
    ''' the location of the products'''
    name = models.CharField(max_length=200,verbose_name=_(u"Platform Name"))
    note = models.TextField(max_length=1000,verbose_name=_(u"Note"))
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Platform")
        verbose_name_plural = _(u"Platforms")
        
    def __unicode__(self):
        return _(u"Selling Platform: %(name)s") % {'name':self.name}
        

   
class Sellingplatformslot(models.Model):
    ''' the location of the products'''
    request = models.ForeignKey(SellRequest,verbose_name=_(u"Selling Request"))
    platform = models.ForeignKey(Sellingplatform,verbose_name=_(u"Platform"))
    url = models.URLField(max_length=250,verbose_name=_(u"Selling URL"),blank=True,null=True)
    createdon = models.DateTimeField(verbose_name=_(u"Create date"), auto_now_add=True,blank=True,null=True)
    orderon = models.DateTimeField(verbose_name=_(u"Order placed date"),blank=True,null=True)
    order_id = models.CharField(max_length=1000,verbose_name=_(u"Order Id"),blank=True,null=True)
    note = models.TextField(max_length=1000,verbose_name=_(u"Note"),blank=True,null=True)
    
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Selling Slot")
        verbose_name_plural = _(u"Selling Slots")
        
    def __unicode__(self):
        return _(u"Selling Slot %(id)s on %(platform)s:%(product)s") % {'platform':self.platform.name,'id':self.id,'product':self.request.item_list()}

