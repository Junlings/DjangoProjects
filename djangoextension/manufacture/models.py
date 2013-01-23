import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from django.core.urlresolvers import reverse

from filer.fields.image import FilerImageField
from contacts.models import social, address

Debug = True

def stlog(msg):
    if Debug:
        print msg
    else:
        pass
    
    
class ManufacturerManager(models.Manager):
    def get_or_create(*args,**kargs):
        instance = None
        
        # try match and get
        for key in ['name']:
            try:
                query = {key:kargs[key]}
                instance = Manufacturer.objects.get(**query)
                stlog('Found the Manufacturer instance')
                break
            except:
                continue
            
        if instance != None:
            return instance
        
        else:
            stlog('Do not find Manufacturer instance')
            instance = Manufacturer(**kargs)           # create new 
            instance.save()
            stlog('Created the Manufacturer instance')
            return instance
        
class Manufacturer(models.Model):
    ''' This is the person who product '''
    name = models.CharField(max_length=80,verbose_name=_("name"))
    local_store = models.BooleanField(verbose_name=_("has local stores?"),default=True)
    online_store = models.BooleanField(verbose_name=_("has online stores?"),default=True)
    address = models.ForeignKey(address, verbose_name=_(u"Address"),null=True, blank=True)
    contact = models.ForeignKey(social, verbose_name=_(u"Contact information"),null=True, blank=True)
    notes = models.TextField(max_length=500,null=True, blank=True, verbose_name=(u'notes'))
    
    objects = ManufacturerManager()
    class Meta:
        ordering = ['name']
        verbose_name = _(u"Manufacturer")
        verbose_name_plural = _(u"Manufacturers")
        
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])

class ItemProductmanager(models.Manager):
    
    def get_or_create(*args,**kargs):
        instance = None
        
        # try match and get
        for key in ['longname','shortname','modelid','upc']:
            try:
                query = {key:kargs[key],'manufacturer__name':kargs['manufacturer']['name']}
                instance = ItemProduct.objects.get(**query)
                stlog('Found the ItemProduct instance')
                break
            except:
                continue
            
        if instance != None:
            return instance
        
        # then need to create new ones
        else:
            stlog('Do not find ItemProduct instance')
            manufacturer_instance = Manufacturer.objects.get_or_create(**kargs['manufacturer'])
            
            kargs['manufacturer'] = manufacturer_instance
            instance = ItemProduct(**kargs)
            instance.save()
            stlog('Created the ItemProduct instance')
            return instance
            

class ItemProduct(models.Model):
    ''' This is the product model from manufacturer'''
    longname = models.CharField(max_length=300,verbose_name=_("Long Name"))
    shortname = models.CharField(max_length=80,verbose_name=_("Short Name"),null=True, blank=True)
    modelid = models.CharField(max_length=80,verbose_name=_("Model ID"),null=True, blank=True)
    upc = models.CharField(max_length=80,verbose_name=_("UPC"),null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_(u"Manufacturer"))
    brand = models.CharField(max_length=80,verbose_name=_("brand"),null=True, blank=True)
    # image of the product using the django-filer app
    mainimage = FilerImageField(verbose_name="Main image",null=True, blank=True)    
    mainimagepath = models.URLField(max_length=200,verbose_name="Main image Path",null=True, blank=True)
    created_on = models.DateField(verbose_name=_(u"Created Date"),blank=True,auto_now_add=True)
    objects = ItemProductmanager()
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"product")
        verbose_name_plural = _(u"products")
        
    def __unicode__(self):
        return self.longname
    
    def get_manufacturer(self):
        return self.manufacturer.name
    
    
    @staticmethod
    def batch_create(inputdict):

        # for now, do not know how to link to image
        if 'mainimage' in inputdict.keys():
            del inputdict['mainimage']

        # get manufacture for sure
        if 'manufacturer' in inputdict.keys():
            try:
                manufacturer_instance = Manufacturer.objects.get(name=inputdict['manufacturer'])
                inputdict['manufacturer'] = manufacturer_instance
                print 'find one'
            except:
                manufacturer_instance = Manufacturer(**{'name':inputdict['manufacturer']})
                manufacturer_instance.save()
                inputdict['manufacturer'] = manufacturer_instance
                print 'create one'
        #print inputdict
        
        try:
            new_item = ItemProduct.objects.get(shortname=inputdict['shortname'])
        except:
            new_item = ItemProduct(**inputdict)
            new_item.save()
        return new_item