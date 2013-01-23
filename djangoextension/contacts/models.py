import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
#from django.contrib.localflavor.us.models import USStateField, USPostalCodeField, PhoneNumberField

class test(models.Model):
    nickname = models.CharField(max_length=100,verbose_name=_(u"nickname"))
    def __unicode__(self):
        return "%(nickname)s" % {'nickname':self.nickname}    
    
class address(models.Model):
    ''' The generic address model '''
    nickname = models.CharField(max_length=100,verbose_name=_(u"nickname"))
    country = models.CharField(max_length=100,verbose_name=_(u"country"))
    state = models.CharField(max_length=100,verbose_name=_(u"state"))
    city = models.CharField(max_length=100,verbose_name=_(u"city"))
    address_line1 = models.CharField(max_length=100,verbose_name=_(u"address_1"))
    address_line2 = models.CharField(max_length=100,verbose_name=_(u"address_2"), null=True, blank=True)
    zipcode = models.CharField(max_length=100,verbose_name=_(u"zipcode"))
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"address")
        verbose_name_plural = _(u"addresses")
    
    def __unicode__(self):
        return "%(nickname)s" % {'nickname':self.nickname}
        

class social(models.Model):
    nickname = models.CharField(max_length=100,verbose_name=_(u"nickname"))
    homephone = models.CharField(max_length=100,verbose_name=_(u"home Phone number"), null=True, blank=True)
    cellphone = models.CharField(max_length=100,verbose_name=_(u"cell Phone number"), null=True, blank=True)
    businessphone = models.CharField(max_length=100,verbose_name=_(u"business Phone number"), null=True, blank=True)
    fax = models.CharField(max_length=100,verbose_name=_(u"fax number"), null=True, blank=True)
    
    email = models.EmailField(max_length=75,verbose_name=_(u"email address"), null=True, blank=True)
    website = models.CharField(max_length=100,verbose_name=_(u"website"), null=True, blank=True)
    
    facebook= models.CharField(max_length=100,verbose_name=_(u"facebook account"), null=True, blank=True)
    linkedin = models.CharField(max_length=100,verbose_name=_(u"linkedin account"), null=True, blank=True)
    twitter = models.CharField(max_length=100,verbose_name=_(u"twitter account"), null=True, blank=True)
    sina_weibo = models.CharField(max_length=100,verbose_name=_(u"sina weibo account"), null=True, blank=True)    
    qq = models.CharField(max_length=20,verbose_name=_(u"Tencent QQ"), null=True, blank=True)  
    mitbbs_id = models.CharField(max_length=100,verbose_name=_(u"Mitbbs_id"), null=True, blank=True) 
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Contact Info")
        verbose_name_plural = _(u"Contacts Info")
    
    def __unicode__(self):
        return "%(nickname)s" % {'nickname':self.nickname}