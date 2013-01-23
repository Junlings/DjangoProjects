from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social

        
class customers(models.Model):
    firstname = models.CharField(max_length=100,verbose_name=_(u"first name"))
    middlename = models.CharField(max_length=100,verbose_name=_(u"middle name"),blank=True,null=True)
    lastname = models.CharField(max_length=100,verbose_name=_(u"last name"),blank=True,null=True)
    
    address = models.ForeignKey(address,verbose_name=_(u"address"),blank=True,null=True)
    contact = models.ForeignKey(social,verbose_name=_(u"contacts"),blank=True,null=True)

    class Meta:
        verbose_name = _(u"customer")
        verbose_name_plural = _(u"customers")
        
    def __unicode__(self):
        return _(u"%(firstname)s") % {'id':self.id,'firstname':self.firstname}
            