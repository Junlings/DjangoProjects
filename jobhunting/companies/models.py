from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social

        
class companys(models.Model):
    abbrname = models.CharField(max_length=100,verbose_name=_(u"abbr. name"))
    fullname = models.CharField(max_length=200,verbose_name=_(u"full name"),blank=True,null=True)
    type = models.CharField(max_length=100,verbose_name=_(u"company type"))
    address = models.ForeignKey(address,verbose_name=_(u"address"),blank=True,null=True)
    contact = models.ForeignKey(social,verbose_name=_(u"contacts"),blank=True,null=True)

    class Meta:
        verbose_name = _(u"company")
        verbose_name_plural = _(u"companies")
        
    def __unicode__(self):
        return _(u"%(id)s_%(abbrname)s") % {'id':self.id,'abbrname':self.abbrname}
        
class company_rank(models.Model):
    company = models.ForeignKey(companys,verbose_name=_(u"Compnay"),blank=True,null=True)
    rank_agency = models.CharField(max_length=200,verbose_name=_(u"Rank Agency"))
    rank_year = models.IntegerField(max_length=4,verbose_name=_(u"Rank Year"))
    rank = models.IntegerField(max_length=5,verbose_name=_(u"Rank"))

    class Meta:
        verbose_name = _(u"Company Rank")
        verbose_name_plural = _(u"Company Ranks")
        
    def __unicode__(self):
        return _(u"%(company)s_%(year)s_%(rank)s") % {'company':self.company,'year':self.rank_year,'rank':self.rank}
            