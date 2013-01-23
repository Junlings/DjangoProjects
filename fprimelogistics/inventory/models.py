import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
  
from djangoextension.contacts.models import address as addressmodel
from django.contrib.auth.models import User

class storage(models.Model):
    ''' the location of the products'''
    nickname = models.CharField(max_length=32, verbose_name=_("nickname"))
    address = models.ForeignKey(addressmodel, verbose_name=_("Address"), null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name=_("Responsible party"), null=True, blank=True)
    #item = models.OneToOneField(asset, verbose_name=_("asset"), null=True, blank=True)
    #assetsgroup = models.ManyToManyField(assetgroup, verbose_name=_("asset group"), null=True, blank=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"storage")
        verbose_name_plural = _(u"storages")
        
    def __unicode__(self):
        return self.nickname
