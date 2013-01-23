import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse

from filer.fields.image import FilerImageField
from contacts.models import social, address
import supplier.staples as staples
import supplier.target as target
import supplier.amazon as amazon
import supplier.walmart as walmart
import supplier.bestbuy as bestbuy
from stores.models import Local_Stores_Staples, Local_Stores_Bestbuy, Local_Stores_Target, Local_Stores_Walmart





Debug = True

def stlog(msg):
    if Debug:
        print msg
    else:
        pass
    
from supplier.__init__ import suppliers_list
from manufacture.models import ItemProduct, Manufacturer
#from product_availbility.models import inventory_results

def supply_dispatch(supplier_name):
    if supplier_name == 'staples':
        #LOCAL_STORE_MODEL = Local_Stores_Staples
        staples.LOCAL_STORE_MODEL = Local_Stores_Staples
        return staples
    elif supplier_name == 'amazon':
        return amazon
    elif supplier_name == 'target':
        target.LOCAL_STORE_MODEL = Local_Stores_Target
        return target
    elif supplier_name == 'bestbuy':
        bestbuy.LOCAL_STORE_MODEL = Local_Stores_Bestbuy
        return bestbuy
    elif supplier_name == 'walmart':
        walmart.LOCAL_STORE_MODEL = Local_Stores_Walmart
        return walmart 
    
    else:
        return None


class SupplierManager(models.Manager):
    def get_or_create(*args,**kargs):
        instance = None

        # try match and get
        for key in ['name']:
            try:
                query = {key:kargs[key]}
                instance = Supplier.objects.get(**query)
                stlog('Found the supplier instance')
                break
            except:
                continue
            
        if instance != None:
            return instance

        else:
            stlog('Do not find Supplier instance')
            instance = Supplier(**kargs)           # create new 
            instance.save()
            stlog('create the supplier instance')

            return instance    


class Supplier(models.Model):
    ''' This is the person who sell the products '''
    name = models.CharField(max_length=80,verbose_name=_("name"),unique=True)
    local_store = models.BooleanField(verbose_name=_("has local stores?"))
    online_store = models.BooleanField(verbose_name=_("has online stores?"))
    platform = models.CharField(verbose_name=_(u"Supplier Selling platform"), max_length=30,null=True, blank=True)
    address = models.ForeignKey(address, verbose_name=_(u"Address"),null=True, blank=True)
    contact = models.ForeignKey(social, verbose_name=_(u"Contact information"),null=True, blank=True)
    notes = models.TextField(max_length=500,null=True, blank=True, verbose_name=(u'notes'))
    created_on = models.DateField(verbose_name=_(u"Created Date"),blank=True,auto_now_add=True)
    
    objects = SupplierManager()
    
    class Meta:
        ordering = ['name']
        verbose_name = _(u"supplier")
        verbose_name_plural = _(u"suppliers")
        
    def __unicode__(self):
        return "%s_%s" % (self.name,self.id)
    
    def get_cls(self):
        supplier_name = self.name
        return supply_dispatch(supplier_name)
        
    def get_localstore(self):
        return self.get_cls(self.name).LOCAL_STORE_MODEL
    
    @staticmethod    
    def get_cls(supplier_name):
        return supply_dispatch(supplier_name)
    
    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])
          



class ItemTemplateManager(models.Manager): 
    def get_localstore(self):
        return self.suppliers.get_cls().LOCAL_STORE_MODEL
        
    def get_or_create(*args,**kargs):
        # first to check supplier
        suppliers_instance = Supplier.objects.get_or_create(**kargs['suppliers'])
        kargs['suppliers'] = suppliers_instance
        
        
        ItemTemplate_instance = None
        # check ItemTemplate 
        for key in ['suppliers_PID']:
            try:
                query = {key:kargs[key],'suppliers':suppliers_instance}
                ItemTemplate_instance = ItemTemplate.objects.get(**query)
                stlog('Found the ItemTemplate instance')
                break
            except:
                continue
            
        if ItemTemplate_instance != None:
            return ItemTemplate_instance
        
        else:           
            stlog('Do not find ItemTemplate instance') 
            stlog('Do the online search for supply information')
            
            storemodule = suppliers_instance.get_cls(suppliers_instance.name)
            #print storemodule
            search_dict = storemodule.obtain_supply(kargs['suppliers_PID'])
            #print search_dict
            kargs.update(search_dict) 
            itemproduct_instance = ItemProduct.objects.get_or_create(**kargs['itemproduct'])
            
            kargs['itemproduct'] = itemproduct_instance
            kargs['suppliers'] = suppliers_instance

            ItemTemplate_instance = ItemTemplate(**kargs)
            ItemTemplate_instance.save()
            stlog('create the ItemTemplate instance')
            return ItemTemplate_instance
                
class ItemTemplate(models.Model):
    ''' this is the template of the product item '''
    itemproduct = models.ForeignKey(ItemProduct,verbose_name=_(u"ItemProduct"))
    suppliers = models.ForeignKey(Supplier,verbose_name=_(u"Supplier"))
    suppliers_PID = models.CharField(verbose_name=_(u"Supplier Online PID"), max_length=30)
    local_PID = models.CharField(verbose_name=_(u"Supplier Local PID"), max_length=30, null=True,blank=True)
    price_base = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Base Supply Price"), null=True,blank=True)
    online_avail = models.BooleanField(verbose_name=_("Available online?"),default=False)
    local_avail = models.BooleanField(verbose_name=_("Available at local stores?"),default=False)
    notes = models.TextField(max_length=500,verbose_name=_(u"notes"), null=True, blank=True)
    
    objects = ItemTemplateManager()
    class Meta:
        ordering = ['id']	
        verbose_name = _(u"item template")
        verbose_name_plural = _(u"item templates")        
    
    @models.permalink
    def get_absolute_url(self):
        return ('template_view', [str(self.id)])

    def __unicode__(self):
        return "%(name)s|%(manu)s|%(prodname)s" % {'name':self.suppliers.name,
                                                  'pid':self.suppliers_PID,
                                                  'prodname':self.itemproduct.shortname,
                                                  'manu':self.itemproduct.manufacturer.name}
    
    def get_product(self):
        """ function for restful service"""
        return self.itemproduct.longname
        
    def get_manufacturer(self):
        return self.itemproduct.manufacturer.name
    
    def get_suppliers(self):
        return self.suppliers.name


class ItemTemplateStatus(models.Model):
    item = models.ForeignKey(ItemTemplate,verbose_name=_(u"Supply Item"))    
    source_date = models.DateTimeField(verbose_name=_(u"Check On"),blank=True,default=datetime.datetime.now())
    check_date = models.DateTimeField(verbose_name=_(u"Check On"),blank=True,default=datetime.datetime.now())
    
    class Meta:
        abstract = True
        
class ItemTemplateStockOnline(ItemTemplateStatus):
    """ This is the supply online status """  
    online_inventory = models.CharField(verbose_name=_(u"Online Inventory status"), max_length=30, null=True, blank=True)
    
    
#class ItemTemplateStockLocal(ItemTemplateStatus):
#    local_inventory = models.OneToOneField(inventory_results,verbose_name=_(u"Local avbility conditions"))    

class ItemTemplatePriceOnline(ItemTemplateStatus):
    """ This is the supply local status, which will have foreignkey to local availbility """
    online_sale = models.CharField(verbose_name=_(u"Online Sale Format"), max_length=30, null=True, blank=True)
    online_price = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Online Sale Price"), null=True, blank=True)

class ItemTemplatePriceLocal(ItemTemplateStatus):
    local_sale = models.CharField(verbose_name=_(u"Local Sale Format"), max_length=30, null=True, blank=True)
    local_price = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Local Sale Price"), null=True, blank=True)   