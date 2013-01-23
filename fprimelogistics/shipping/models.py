import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

CARRIER_NAME = (
    ('UPS','UPS'),
    ('USPS','USPS'),
    ('FEDEX','FEDEX'),
    ('DHL','DHL'),
    ('other','other'),
)

class ShippmentManager(models.Manager):
    def inquery_user(self,user):
        return self.filter(owner=user)


class shipments(models.Model):
    ''' The financial account model '''
    nickname = models.CharField(max_length=100,verbose_name=_(u"Nick name"))
    carrier = models.CharField(max_length=20,choices=CARRIER_NAME, verbose_name=_(u"Carrier"))
    tracking = models.CharField(max_length=50,verbose_name=_(u"tracking number"))
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)
    # advanced options for future integration
    #cost = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True,verbose_name=_(u"shipping cost"))
    #account = models.ForeignKey(accounts, verbose_name=_(u"shipping cost account"),related_name='debit')
    
    
    objects = ShippmentManager()
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"shipment")
        verbose_name_plural = _(u"shipment")
    
    def __unicode__(self):
        return "%s_by_%s" % (self.nickname,self.carrier)
        