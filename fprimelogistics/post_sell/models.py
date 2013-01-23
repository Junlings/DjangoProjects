import datetime

from django.db import models
from djangoextension.financial.models import accounts
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager
from assets.models import assetgroup
from shipping.models import shipments
from inventory.models import storage
POSTSELL_STATES = (
    ('Reported', 'Post sell case reported'),
    ('Decided', 'Financial decision decided'),
    ('Return Shipped', 'custom shipped the return item'),
    ('Return arrived', 'return arrived'),
    ('Refund issued', 'refund issued'),
    ('Refund received', 'refund received'),
    ('settled', 'case closed'),
)

POSTSELL_DOC_TYPES =(
    ('Order slip', 'Order details send to customer'),
    ('Other', 'Other'),
)


class PostSellRequest(models.Model):
    ''' the location of the products'''
    items = models.ForeignKey(assetgroup, verbose_name=_(u"Items Selling"))
    fullfilled = models.BooleanField(verbose_name=_("Fullfilled?"),default=False)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Postsell Request")
        verbose_name_plural = _(u"Postsells Request")
        
    def __unicode__(self):
        return _(u"Sell Request: %(quantity)s of %(item)s") % {'quantity':self.quantity, 'item':self.item.shortname}


class postsell_cost(models.Model):
    ''' This is the model to quantify the cost of certain purchase'''
    postrequest = models.OneToOneField(PostSellRequest, verbose_name=_(u"Selling Request"))
    restockingfee = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"restocking fee"))
    tax_chargedback = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Tax charged"))
    account_product_tax = models.ForeignKey(accounts, verbose_name=_(u"postsell account"),related_name='postsell')
    
    shipping = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"total shipping cost"),blank=True,null=True)
    account_shipping = models.ForeignKey(accounts, verbose_name=_(u"shipping account"),related_name='postsell_shipping',blank=True,null=True)
    shippment = models.ForeignKey(shipments, verbose_name=_(u"shipments"),blank=True,null=True)
     
    commission = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"Purchase commission cost"),blank=True,null=True)
    account_commission = models.ForeignKey(accounts, verbose_name=_(u"Commision account"),related_name='postsell_comission',blank=True,null=True)
    
    net_income = models.DecimalField(max_digits=10,decimal_places=2, verbose_name=_(u"net income"),editable=False)
    
    
    class Meta:
        verbose_name = _(u"Postsell cost")
        verbose_name_plural = _(u"Postsell costs")
        
    def __unicode__(self):
        return _(u"%(id)s") % {'id':self.id}


class PostsellDoc(models.Model):
    postrequest = models.OneToOneField(PostSellRequest, verbose_name=_(u"Selling Request"))
    type = models.CharField(max_length=50, choices=POSTSELL_DOC_TYPES,verbose_name=_(u'type'),blank=True)
    date = models.DateTimeField(verbose_name=_(u"date"), auto_now_add=True)
    doc = models.FileField(upload_to='doc/%Y/%m/%d',verbose_name=_(u"document"),blank=True)
    
    class Meta:
        verbose_name = _(u"PostSell Document")
        verbose_name_plural = _(u"PostSell Documents")
        
    def __unicode__(self):
        return _(u"Docs id=%(id)s, upload on %(date)s, by %(user)s ") % {'id':self.id, 'date':self.date,'user':self.person}





