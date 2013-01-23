from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social

CLIENT_TYPE = (
    ('Amazon_CSM','Amazon customer'),
    ('Ebay_CSM','Ebay customer'),
    ('Carglist_CSM','Carglist customer'),
    ('Taobao_CSM','Taobao customer'),
    ('US_Vender','US vender'),
    ('CN_Vender','China vender'),
    ('other','other'),
    
)


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    zipcode = models.CharField(max_length=5, default="00000")
    BOXNET_FolderID = models.CharField(max_length=60, default="00000")

    class Meta:
        verbose_name = _(u"user profile")
        verbose_name_plural = _(u"user preofiles")
        
    def __unicode__(self):
        return _(u"%(user)s") % {'user':self.user}
        
class clients(models.Model):
    user = models.OneToOneField(User)
    fullname = models.CharField(max_length=200,verbose_name=_(u"full name"))
    type = models.CharField(max_length=100,choices=CLIENT_TYPE,verbose_name=_(u"client type"))
    address = models.ForeignKey(address,verbose_name=_(u"address"))
    contact = models.ForeignKey(social,verbose_name=_(u"contacts"))

    class Meta:
        verbose_name = _(u"client")
        verbose_name_plural = _(u"clients")
        
    def __unicode__(self):
        return _(u"%(nickname)s") % {'nickname':self.nickname}   