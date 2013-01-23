from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social
from companies.models import companys
from affiliation.models import organizations

class company_account(models.Model):
    company = models.ForeignKey(companys,verbose_name=_(u"company"))
    user = models.ForeignKey(User,verbose_name=_(u"user"))
    website = models.CharField(max_length=100,verbose_name=_(u"login link"))
    loginname = models.CharField(max_length=100,verbose_name=_(u"login name"))
    loginpass = models.CharField(max_length=100,verbose_name=_(u"login password"))
    loginemail = models.EmailField(max_length=100,verbose_name=_(u"contact email"),blank=True,null=True)
    
    class Meta:
        verbose_name = _(u"company login")
        verbose_name_plural = _(u"company logins")
        
    def __unicode__(self):
        return _(u"%(company)s_%(user)s") % {'company':self.company.abbrname,'user':self.user.username}   

class organization_account(models.Model):
    organization = models.ForeignKey(organizations,verbose_name=_(u"Organization"))
    user = models.ForeignKey(User,verbose_name=_(u"user"))
    website = models.CharField(max_length=100,verbose_name=_(u"login link"))
    loginname = models.CharField(max_length=100,verbose_name=_(u"login name"))
    loginpass = models.CharField(max_length=100,verbose_name=_(u"login password"))
    websitename = models.CharField(max_length=100,verbose_name=_(u"webiste name"))
    websitepass = models.CharField(max_length=100,verbose_name=_(u"website password"))
    loginemail = models.EmailField(max_length=100,verbose_name=_(u"contact email"),blank=True,null=True)
    
    class Meta:
        verbose_name = _(u"Organization login")
        verbose_name_plural = _(u"Organization logins")
        
    def __unicode__(self):
        return _(u"%(organization)s_%(user)s") % {'organization':self.organization.abbrname,'user':self.user.username}   