from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social

        
class organizations(models.Model):
    abbrname = models.CharField(max_length=100,verbose_name=_(u"abbr. name"))
    fullname = models.CharField(max_length=200,verbose_name=_(u"full name"))
    type = models.CharField(max_length=100,verbose_name=_(u"organization type"))
    address = models.ForeignKey(address,verbose_name=_(u"address"),blank=True,null=True)
    contact = models.ForeignKey(social,verbose_name=_(u"contacts"),blank=True,null=True)

    class Meta:
        verbose_name = _(u"organization")
        verbose_name_plural = _(u"organizations")
        
    def __unicode__(self):
        return _(u"%(abbrname)s") % {'abbrname':self.abbrname}
        


    