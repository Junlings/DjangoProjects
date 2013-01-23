from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from affiliation.models import organizations

        
class skills(models.Model):
    name = models.CharField(max_length=100,verbose_name=_(u"name"))
    type = models.CharField(max_length=100,verbose_name=_(u"type"))
    level = models.CharField(max_length=100,verbose_name=_(u"skill level"))
    notes = models.TextField(max_length=2000,verbose_name=_(u"notes"))
    
    
    class Meta:
        verbose_name = _(u"skill")
        verbose_name_plural = _(u"skills")
        
    def __unicode__(self):
        return _(u"%(name)s_%(level)s") % {'name':self.name,'level':self.level}
        


class certifications(models.Model):
    name = models.CharField(max_length=100,verbose_name=_(u"name"))
    skills = models.ForeignKey(skills,verbose_name=_(u"skills"))
    organization = models.ForeignKey(organizations,verbose_name=_(u"organizations"))
    type = models.CharField(max_length=100,verbose_name=_(u"type"))
    level = models.CharField(max_length=100,verbose_name=_(u"qualification level"))
    notes = models.TextField(max_length=2000,verbose_name=_(u"notes"))    

    class Meta:
        verbose_name = _(u"certification")
        verbose_name_plural = _(u"certifications")
        
    def __unicode__(self):
        return _(u"%(name)s_%(level)s") % {'name':self.name,'level':self.level}