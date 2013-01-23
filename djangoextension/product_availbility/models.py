import datetime
import os
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.core.urlresolvers import reverse
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.localflavor.us.models import USStateField, USPostalCodeField, PhoneNumberField
from django.contrib.auth.models import User, UserManager
#from models import ItemTemplate
from datetime import datetime, timedelta
from uti.dumpload import dump_data, load_data
from stores.models import Local_Stores_Bestbuy, Local_Stores_Staples, Local_Stores_Target, Local_Stores_Walmart
from supply.models import ItemTemplate
#from checker import checker_bestbuy, checker_staples, checker_target, checker_walmart
from django.conf import settings

REQUEST_Availability = (
    ('Now', 'Available now'),
    ('1-2 days', 'Available in 1-2 days'),
    ('3-5 days', 'Available in 3-5 days'),
    ('6-10 days', 'Available in 6-10 days'),
    ('More than 10 days', 'More than 10 days'),
)


SEARCH_INTERVAL = (
    ('Now', 'everytime submit request'),
    ('10 days', 'every 10 days'),
    ('1 day', 'every 1 day'),
    ('1 hour', 'every one hour'),
    ('10 minutes', 'every 10 minutes'),
    ('10 seconds', 'every 10 seconds'),
)

AVAIL_SUPPLIERS = (
    ('staples', 'staples'),
    ('bestbuy', 'bestbuy'),
    ('target', 'target'),
    ('walmart', 'walmart'),
)

SEARCH_STORAGE = os.path.join(settings.MEDIA_ROOT,'inventory_results')

class inventoryresultsManager(models.Manager):
    def get_or_create(*args,**kargs):
        instance = None
        
        # try match and get:
        try:
            query = {'item__suppliers_PID':kargs['item']['suppliers_PID'],'item__suppliers__name':kargs['item']['suppliers']['name']}
            instance = inventory_results.objects.get(**query)
        except:
            pass
            
        if instance != None:
            return instance
        
        # then need to create new ones
        else:
            #print kargs
            item_instance = ItemTemplate.objects.get_or_create(**kargs['item'])
            
            kargs['item'] = item_instance
            instance = inventory_results(**kargs)
            instance.save()
            return instance

class inventory_results(models.Model):
    name = models.CharField(max_length=80,verbose_name=_("Result name"))
    item = models.ForeignKey(ItemTemplate, verbose_name=_(u"Item Template"))
    latest_file = models.FilePathField(path='doc',max_length=100,null=True, blank=True)
    last_commit  = models.DateTimeField(verbose_name=_("latest search result file"),null=True, blank=True)
    search_interval = models.CharField(max_length=20,choices=SEARCH_INTERVAL,verbose_name=_("Search interval"))
    
    objects = inventoryresultsManager()
    
    def __unicode__(self):
        return u'%s_%s_%s_every_%s' %(self.name,self.item.suppliers.name,self.item.suppliers_PID,self.search_interval)
        
    class Meta:
        ordering = ['name']
        verbose_name = _(u"Inventory Search Result")
        verbose_name_plural = _(u"Inventory search Results")
     
    def by_state(self,state):
        localstore = self.item.suppliers.get_localstore()
        return localstore.objects.by_state(state)
        #localstore.
    
    def if_search(self,storequery):
        ''' check if need to search based on the complete of the queryset'''
        update_query = []  # the store results that need update
        
        try:
            total_results = self.load_latest(storequery)
            
            key_list = []
            for i in total_results:
                key_list.append(i['id'])
                
            storelist = list(storequery)
            for i in range(0,len(storelist)):
                store = storelist[i]
                if store.id not in key_list:
                    print store.id
                    return 3                   # if missing certain results
        except:
            return 2  # if read latest file fail, then definitely redo search
        
        ''' check if need to research based on the search_interval settings '''
        try:
            interval = datetime.now() - self.last_commit 
            if self.search_interval == '1 day' and interval > timedelta(days=1):
                return 4
            elif self.search_interval == 'Now':
                return 4
            elif self.search_interval == '10 days' and interval > timedelta(days=10):
                return 4 
            elif self.search_interval == '10 minutes' and interval > timedelta(minutes=10):
                return 4     
            elif self.search_interval == '10 seconds' and interval > timedelta(seconds=10):
                return 4
            else:
                return 0
        except:
            return 5          # check time frequency fail
    
    def commit(self):
        ''' commit search results '''
        self.last_commit = datetime.now()

        foutname = '%(id)s_%(itemid)s_%(datetime)s' % {'id':self.id,
                                                       'itemid':self.supplier_PID,
                                                       'datetime':self.last_commit.strftime('%y_%m_%d_%H')}
        #folder = 'product_availbility/doc/commit/%s' % self.id
        
        folder = SEARCH_STORAGE
        dump_data(foutname,search_results,folder=folder)     
        self.save()
        
    def load_latest(self,storequery=None):
        foutname = '%s_latest' %(self.id)
        folder = SEARCH_STORAGE
        results = load_data(foutname,folder=folder)
        
        new_results = []
        if storequery != None:   # partial results based on the store queryset
            for store in storequery:
                if store.id in results.keys():
                    new_results.append(results[store.id])
                else:
                    pass

            return new_results
        else:
            return results   # all results 
    
    def dump_latest(self,results):
        
        # load latest file
        try:
            total_results = self.load_latest()
        except:
            total_results = {}
        
        time_stamp = datetime.now()
        # cleanup the results
        for item in results:  # avail results is a list of dictionary
            item['last_update'] = time_stamp.strftime("%A, %d. %B %Y %I:%M%p")
            total_results.update({item['id']:item})
        
        
        folder = SEARCH_STORAGE
        foutname = '%s_latest' %(self.id)
        dump_data(foutname,total_results,folder=folder)
        
        #update timestamp
        self.last_commit = datetime.now()
        self.save()
        
    def update(self,results):
        ''' update results, two step process'''
        #
        self.dump_latest(results)
        #self.commit()


    def get_localstore(self):
        LOCAL_STORE = self.item.suppliers.get_localstore()
        return LOCAL_STORE
    
    def inventory_search(self,storename,storequery):
        
        availdata = []
        # get local pid
        pid = self.item.local_PID
        
        # check if the local avaability is valid
        #if not self.item.local_avail:
        #    return []
        #try:
        checkmodule = self.item.suppliers.get_cls(self.item.suppliers.name)
        storelist,availdata = checkmodule.check_local_avail_queryset(pid,storequery)
        #except:
        #    availdata = []
            

        if len(list(storequery)) != len(availdata):
            storequery_list = list(storequery)
            print len(storequery_list),len(availdata)
            req_keys = []
            res_keys = []
            for item in storequery_list:
                req_keys.append(item.id)
            for item in availdata:
                res_keys.append(item['id'])
            ps = set(req_keys).difference(set(res_keys))
            print len(ps)
            print ps
            
            #raise Error
        
        # here generate new availdata
        
        for i in range(0,len(storelist)):
            for j  in  range(0,len(availdata)):
                if availdata[j]['id'] == storelist[i].id:
                    availdata[j].update({'lat':storelist[i].lat,
                                         'lng':storelist[i].lng,
                                         'name':storelist[i].name,
                                         'address':storelist[i].address,
                                         'city':storelist[i].city,
                                         'state':storelist[i].state,
                                         'phone':storelist[i].phone,})
        if len(availdata) > 0:
            self.update(availdata)  # update saved results
        return availdata
    