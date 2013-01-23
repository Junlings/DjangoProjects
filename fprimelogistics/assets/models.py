import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from financial.models import accounts as financial_accounts
from supply.models import ItemTemplate
from inventory.models import storage
from decimal import Decimal

class AssetManager(models.Manager):
    """ asset manager """
    
    def classify(self,objs):#onsale=True,sold=False,location=None):
        """ asset classify based on input queryset """


        prod_dict = {}
        for obj in objs:
            location = obj.location()
            if obj.item.__unicode__ not in prod_dict.keys():
                prod_dict[obj.item.__unicode__] = {'quantity':1,'img':obj.item.itemproduct.mainimagepath,'location':[location]}
            else:
                prod_dict[obj.item.__unicode__]['quantity'] += 1
                if location not in prod_dict[obj.item.__unicode__]['location']:
                    prod_dict[obj.item.__unicode__]['location'].append(location)
        return prod_dict

    def summarize_onsale(self):
        """ Select all assets now on sale"""
        objs = self.filter(onsale=True,sold=False)
        return self.classify(objs)

    def summarize_instock(self):
        """ Select all assets current in stock """
        objs = self.filter(onsale=False,sold=False)
        return self.classify(objs)

    def summarize_sold(self):
        """ Select all assets already sold """
        objs = self.filter(sold=True)
        return self.classify(objs)

    def user_instock(self,request):
        """ Select all assets current at user storage location """
        location = storage.objects.get(owner=request.user)
        objs = self.filter(assetstorage__location=location,assetstorage__moveout=None)
        return location,self.classify(objs)
        
        #try:
        #    location = storage.objects.get(owner=request.user)
        #    return location,self.classify(assetstorage__location=location,assetstorage__moveout=None)
        #except:
        #    return None,[]
    
    def summarize_estimates(request,objs):
        prod_dict = {'cost':Decimal('0.0'),'income':Decimal('0.0'),'profit':Decimal('0.0')}
        for obj in objs:
            estimateobj = obj.get_estimate()
            estimate = estimateobj.summary()
            prod_dict['cost'] += estimate['cost']
            prod_dict['income'] += estimate['income']
            prod_dict['profit'] += estimate['profit']
        return prod_dict
    
    
class asset(models.Model):
    ''' this is the asset class which will be purchased, stored, and then sold '''
    item = models.ForeignKey(ItemTemplate,verbose_name=_(u"item")) #models.ForeignKey("Supplier")
    sn = models.CharField(max_length=50, verbose_name=_(u"Serial Number"), null=True, blank=True)
    FSIN = models.CharField(max_length=15, verbose_name=_(u"12 digits product identification number"))
    created = models.DateTimeField(verbose_name=_(u"Created Date"),blank=True,auto_now_add=True)
    notes = models.TextField(max_length=500, verbose_name=_(u"notes"), null=True, blank=True)
    
    onsale = models.NullBooleanField(verbose_name=_("onsale?"),default=False, null=True, blank=True)
    sold = models.NullBooleanField(verbose_name=_("sold?"),default=False, null=True, blank=True)
    objects = AssetManager()
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"asset")
        verbose_name_plural = _(u"assets")
    
    def __unicode__(self):
        #return "%(itemname)s_%(FSIN)s" % {'itemname':self.item.itemproduct.__unicode__(),'FSIN':self.FSIN}        
        return "%(name)s|%(FSIN)s|onsale:%(onsale)s" % {'name':self.item.__unicode__(),'FSIN':self.FSIN,'onsale':self.onsale} 

    def curent_stoarge(self):
        curent_stoarge = assetstorage.objects.filter(item=self).order_by('-movein')[0]
        return curent_stoarge

    def stoarge_history(self):
        stoarges = assetstorage.objects.filter(item=self).order_by('-movein')
        return stoarges

    
    def location(self):
        current_location = assetstorage.objects.filter(item=self).order_by('-movein')[0]
        return current_location.location
    
    def get_estimate(self):
        estimate = assetestimate.objects.get(asset=self)
        return estimate

    
class assetgroup(models.Model):
    """ This is the asset group model """
    name = models.CharField(max_length=200, verbose_name=_(u"asset group name"))
    assets = models.ManyToManyField(asset,verbose_name=_(u"Asset group"), null=True, blank=True)


    created = models.DateTimeField(verbose_name=_(u"Created Date"),blank=True,auto_now_add=True)
    status = models.CharField(max_length=200, verbose_name=_(u"asset group status"), null=True, blank=True)
    lockdown = models.BooleanField(verbose_name=_("Lock Down?"),default=False)

    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"asset group")
        verbose_name_plural = _(u"asset groups")
    
    def __unicode__(self):
        return "%(id)s" % {'id':self.id}
        




class assetstorage(models.Model):
    item = models.ForeignKey(asset, verbose_name=_("asset"))
    location = models.ForeignKey(storage, verbose_name=_("location"))
    movein = models.DateTimeField(verbose_name=_(u"Movein Date"), null=True, blank=True,default=datetime.datetime.now())
    moveout = models.DateTimeField(verbose_name=_(u"Moveout Date"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"asset location")
        verbose_name_plural = _(u"asset locations")
    
    def __unicode__(self):
        return "%(id)s" % {'id':self.id}
        
        


class assetestimate(models.Model):
    asset = models.OneToOneField(asset, verbose_name=_("asset"))
    cost_purchase_product = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_purchase_product"),blank=True,null=True)
    cost_purchase_tax = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_purchase_tax"),blank=True,null=True)
    cost_purchase_shipping = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_purchase_shipping"),blank=True,null=True)
    cost_purchase_commision = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_purchase_commision"),blank=True,null=True)
    earn_product = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"earn_product"),blank=True,null=True)
    earn_tax = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"earn_tax"),blank=True,null=True)
    earn_shipping = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"earn_shipping"),blank=True,null=True)
    cost_sell_tax = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_sell_tax"),blank=True,null=True)
    cost_sell_shipping = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_sell_shipping"),blank=True,null=True)
    cost_sell_platform = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_sell_platform"),blank=True,null=True)
    cost_sell_financial = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_sell_financial"),blank=True,null=True)
    cost_sell_commission = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"cost_sell_commission"),blank=True,null=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"asset estimate")
        verbose_name_plural = _(u"asset estimates")
    
    def __unicode__(self):
        return "%(id)s" % {'id':self.id}
    
   
    def summary(self):

        res_dict = {
            'cost':self.cost_purchase_product + self.cost_purchase_tax + self.cost_purchase_shipping + self.cost_purchase_commision +
                   self.cost_sell_tax + self.cost_sell_shipping + self.cost_sell_platform +  self.cost_sell_financial + self.cost_sell_commission,
            'income':self.earn_product + self.earn_shipping + self.earn_tax}
        
        res_dict['profit'] = res_dict['income'] - res_dict['cost']
            
        return res_dict
    
