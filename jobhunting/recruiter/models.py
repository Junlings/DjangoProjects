from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social

        
class recruitercompanys(models.Model):
    abbrname = models.CharField(max_length=100,verbose_name=_(u"abbr. name"))
    fullname = models.CharField(max_length=200,verbose_name=_(u"full name"),blank=True,null=True)
    type = models.CharField(max_length=100,verbose_name=_(u"company type"))
    address = models.ForeignKey(address,verbose_name=_(u"address"),blank=True,null=True)
    contact = models.ForeignKey(social,verbose_name=_(u"contacts"),blank=True,null=True)
    notes = models.TextField(max_length=2000,verbose_name=_(u"notes"),blank=True,null=True)

    class Meta:
        verbose_name = _(u"Recruiter Company")
        verbose_name_plural = _(u"Recruiter Companies")
        
    def __unicode__(self):
        return _(u"%(abbrname)s") % {'abbrname':self.abbrname}
        
class Recruiter(models.Model):
    company = models.ForeignKey(recruitercompanys,verbose_name=_(u"Compnay"),blank=True,null=True,related_name='company')
    firstname = models.CharField(max_length=200,verbose_name=_(u"firstname"))
    lastname = models.CharField(max_length=200,verbose_name=_(u"lastname"))
    title = models.CharField(max_length=300,verbose_name=_(u"title"))
    contact = models.ForeignKey(social,verbose_name=_(u"contacts"),blank=True,null=True)
    notes = models.TextField(max_length=2000,verbose_name=_(u"notes"),blank=True,null=True)
    
    class Meta:
        verbose_name = _(u"Recruiter")
        verbose_name_plural = _(u"Recruiters")
        
    def __unicode__(self):
        return _(u"%(company)s_%(firstname)s_%(lastname)s") % {'company':self.company,'firstname':self.firstname,'lastname':self.lastname}
            