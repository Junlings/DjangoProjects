import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse
#from django.db.models.signals import post_save, pre_save
#from django.dispatch import receiver
from django.contrib.localflavor.us.models import USStateField, USPostalCodeField, PhoneNumberField
#from django.contrib.auth.models import User, UserManager
#from purchases.models import ItemTemplate
from datetime import datetime, timedelta
from utility.latlng_distance import distance, get_geocode
from django.conf import settings

Debug = settings.DEBUG
def stlog(msg):
    if Debug:
        print msg
    else:
        pass
    
class StoreManager(models.Manager):
    
    def by_filter(self,LOCALSTOREMODEL,**kargs):
        
        do_zip = 0
        if 'zipcode_distance' in kargs.keys():
            req_zipcode,req_distance = kargs['zipcode_distance']
            del kargs['zipcode_distance']
            do_zip = 1
            
        if len(kargs.keys()) > 0:
            objs = LOCALSTOREMODEL.objects.filter(**{'state':"Florida"})
            stlog({'query as':kargs,'return':objs})
        else:
            objs = LOCALSTOREMODEL.objects.all()
            
        if do_zip:
            objs = self.by_zip_distance(objs,req_zipcode,req_distance)
        
        
        
        return objs
        
        
    
    
    def by_state(self, state):
        return self.filter(state=state)
    
    def by_zip_distance(self,queryset,zipcode,dis = 20):
        disquery = []
        
        latlng = get_geocode(str(zipcode))
        
        for store in queryset:
            if distance(latlng,[store.lat,store.lng]) < float(dis):
                disquery.append(store)
        
        return disquery
        
        '''
        try:
            latlan = get_geocode(str(zipcode))
            
            for store in Local_stores.objects.all():
                if distance(latlng,[store.lat,store.lng]) < float(dis):
                    disquery.append(store)
        except:
            pass
        '''
        return disquery
        

    def latest_states_for_item(self, item):
    
        objs = self.filter(item=item)
        
        count = {}
        for ob in objs:
            count[ob.state] = 1    
        return count


class Local_stores(models.Model):
    ''' This is local staple model '''
    name = models.CharField(max_length=80,verbose_name=_("Store Name"))
    num = models.CharField(max_length=32,verbose_name=_("Store number"))
    address = models.CharField(max_length=200,verbose_name=_("Store Address"))
    city = models.CharField(max_length=50,verbose_name=_("Store City"))
    state = USStateField(verbose_name=_("Store state"))
    zipcode = models.CharField(max_length=5,verbose_name=_("Store zipcode"))
    phone = PhoneNumberField(verbose_name=_("Store phone number"))
    lat = models.CharField(max_length=25,verbose_name=_("Store lat"))
    lng = models.CharField(max_length=25,verbose_name=_("Store lng"))
    notes = models.TextField(null=True, blank=True, verbose_name=(u'notes'))
    hours = models.TextField(null=True, blank=True, verbose_name=(u'hours'))
    
    objects = StoreManager()
    class Meta:
        abstract = True

class Local_Stores_Staples(Local_stores):
    ''' This is local staple model '''
   
    class Meta:
        ordering = ['name']
        verbose_name = _(u"Staples store")
        verbose_name_plural = _(u"Staples stores")
        
    def __unicode__(self):
        return '%s_%s_%s' %(self.name,self.zipcode,self.num)
    
    def check_local_avail(self):
        return check_staples_instore
    
    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])


class Local_Stores_Bestbuy(Local_stores):
    ''' This is local bestbuy model '''
    class Meta:
        ordering = ['name']
        verbose_name = _(u"Bestbuy store")
        verbose_name_plural = _(u"Bestbuy stores")
        
    def __unicode__(self):
        return '%s_%s_%s' %(self.name,self.zipcode,self.num)

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])

class Local_Stores_Target(Local_stores):
    ''' This is local staple model '''
    class Meta:
        ordering = ['name']
        verbose_name = _(u"Target store")
        verbose_name_plural = _(u"Target stores")
        
    def __unicode__(self):
        return '%s_%s_%s' %(self.name,self.zipcode,self.num)

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])

class Local_Stores_Walmart(Local_stores):
    ''' This is local staple model '''
    class Meta:
        ordering = ['name']
        verbose_name = _(u"Walmart store")
        verbose_name_plural = _(u"Walmart stores")
        
    def __unicode__(self):
        return '%s_%s_%s' %(self.name,self.zipcode,self.num)

    @models.permalink
    def get_absolute_url(self):
        return ('supplier_view', [str(self.id)])
