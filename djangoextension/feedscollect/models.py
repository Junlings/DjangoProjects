from django.db import models
from action.models import crequests
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from parse import process
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, smart_str


class MessageManager(models.Manager):

    def process(self):
        update_obj = []
        
        entries = process("http://www.mitbbs.com/board_rss/FleaMarket.xml")
        for key,entry in entries.items():
            obj = self.parse_rss(key,entry)
        
            if obj != None:
                update_obj.append(obj)


        return update_obj

    def DoUpdate(self,obj,entry):
        if obj.updated != entry['updated'] and obj.title != entry['title']:
            obj = Messages.object.get(key=entry['key'])
            obj.title = entry['title']
            obj.save()
            return Obj

        else:
            return None
        
    
    def DoCreate(self,key,entry):
        obj = Messages()
        obj = Messages(**entry)
        obj.save()
        return obj
        
    def parse_rss(self,key,entry):  # parse the entry      
        #obj = self.DoCreate(key,entry)
        #obj = Messages.objects.get(key=key)
        #self.DoUpdate(obj,entry)
        
        #'''
        try:
            obj = Messages.objects.get(key=key)
            #obj = self.DoUpdate(obj,entry)
            try:
                obj = self.DoUpdate(obj,entry)
                
            except:
                pass
                #print "update failed"    
        except:
            obj = self.DoCreate(key,entry)
        

            
        return obj


class Messages(models.Model):
    key = models.CharField(max_length=100,verbose_name=_(u"Message Key"),unique=True)
    title = models.CharField(max_length=100,verbose_name=_(u"Title"))
    author = models.CharField(max_length=100,verbose_name=_(u"Author"))
    link = models.URLField(max_length=200,verbose_name=_(u"Detail URL"))
    updated = models.DateTimeField(verbose_name=_(u"Update Time"), auto_now_add=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(verbose_name=_(u"Object Id"),null=True, blank=True)    
    
    objects = MessageManager()
    
    class Meta:
        verbose_name = _(u"Message")
        verbose_name_plural = _(u"Messages")

    def __unicode__(self):
        return self.title  #u"%(title)s" % {'title':smart_str(self.title, encoding='utf-8')}
    
class PurchaseRequest(crequests):
    link = models.URLField(max_length=200,verbose_name=_(u"Detail URL"))
    product = models.CharField(max_length=500,verbose_name=_(u"Product"))
    price = models.CharField(max_length=500,verbose_name=_(u"Price"))
    unit = models.CharField(max_length=500,verbose_name=_(u"Unit"))
    shipping = models.CharField(max_length=500,verbose_name=_(u"Unit"), null=True, blank=True)
    payment = models.CharField(max_length=500,verbose_name=_(u"Unit"), null=True, blank=True)
    def __unicode__(self):
        return 'Purchase request'
    
class SellRequest(crequests):
    link = models.URLField(max_length=200,verbose_name=_(u"Detail URL"))
    product = models.CharField(max_length=500,verbose_name=_(u"Product"))
    price = models.CharField(max_length=500,verbose_name=_(u"Price"))
    unit = models.CharField(max_length=500,verbose_name=_(u"Unit"))
    shipping = models.CharField(max_length=500,verbose_name=_(u"Unit"), null=True, blank=True)
    payment = models.CharField(max_length=500,verbose_name=_(u"Unit"), null=True, blank=True)
    
    def __unicode__(self):
        return 'Sell request'    