import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager

    

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
        

class contacts(models.Model):
    category = models.CharField(max_length=20,verbose_name=_(u"contact category"), null=True, blank=True)
    phone = models.CharField(max_length=100,verbose_name=_(u"Phone number"), null=True, blank=True)
    fax = models.CharField(max_length=100,verbose_name=_(u"fax number"), null=True, blank=True)    
    email = models.EmailField(max_length=75,verbose_name=_(u"email address"), null=True, blank=True)
    website = models.CharField(max_length=100,verbose_name=_(u"website"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"contact")
        verbose_name_plural = _(u"contacts")
    

class socialmedia(models.Model):
    facebook= models.CharField(max_length=100,verbose_name=_(u"facebook account"), null=True, blank=True)
    linkedin = models.CharField(max_length=100,verbose_name=_(u"linkedin account"), null=True, blank=True)
    twitter = models.CharField(max_length=100,verbose_name=_(u"twitter account"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"Social Media")
        verbose_name_plural = _(u"Social Media")
    

class socialmedia_china(models.Model):
    sina_weibo = models.CharField(max_length=100,verbose_name=_(u"sina weibo account"), null=True, blank=True)    
    qq = models.CharField(max_length=20,verbose_name=_(u"Tencent QQ"), null=True, blank=True)  
    mitbbs_id = models.CharField(max_length=100,verbose_name=_(u"Mitbbs_id"), null=True, blank=True) 
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Social Media China")
        verbose_name_plural = _(u"Social Media China")
        


class authors(models.Model):
    firstname = models.CharField(max_length=200,verbose_name=_(u"first name"))
    lastname = models.CharField(max_length=200,verbose_name=_(u"last name"))
    middlename = models.CharField(max_length=200,verbose_name=_(u"middle name"), null=True, blank=True)
    
    address = models.ManyToManyField(address,verbose_name=_(u"Address"), null=True, blank=True)
    contacts = models.ManyToManyField(contacts,verbose_name=_(u"Contacts"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"author")
        verbose_name_plural = _(u"authors")
    
    def __unicode__(self):
        return "%(id)s %(firstname)s %(lastname)s" % {'firstname':self.firstname,'lastname':self.lastname,'id':self.id}




        
        
class publisher(models.Model):
    name = models.CharField(max_length=200,verbose_name=_(u"full name"))
    shortname = models.CharField(max_length=200,verbose_name=_(u"short name"), null=True, blank=True)
    address = models.ManyToManyField(address,verbose_name=_(u"Address"), null=True, blank=True)
    contacts = models.ManyToManyField(contacts,verbose_name=_(u"Contacts"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"publisher")
        verbose_name_plural = _(u"publishers")
    
    def __unicode__(self):
        return "%(name)s" % {'name':self.name}