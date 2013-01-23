import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from djangoextension.action.models import crequests, cresponses
from supply.models import Supplier
from contacts.models import address
from financial.models import accounts
class onlineaccounts(models.Model):
    ''' The online account model '''
    owner = models.ForeignKey(User, verbose_name=_(u"owner"))
    nickname = models.CharField(max_length=100,verbose_name=_(u"nickname"))
    
    username = models.CharField(max_length=40,verbose_name=_(u"online account user name"))
    password = models.CharField(max_length=40,verbose_name=_(u"online account password"))
    supplier = models.ForeignKey(Supplier, verbose_name=_(u"supplier"))
    shipping_address = models.ForeignKey(address, verbose_name=_(u"Shipment address"))
    financialaccount = models.ForeignKey(accounts, verbose_name=_(u"financial account"))
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"Online account")
        verbose_name_plural = _(u"Online accounts")
    
    def __unicode__(self):
        return "%(nickname)s_%(owner)s_%(supplier)s" % {'nickname':self.nickname,'owner':self.owner,'supplier':self.supplier.name}        

    def get_owner(self):
        return self.owner.username
