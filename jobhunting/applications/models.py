from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social
from openings.models import openings
import os
import datetime

from filer.fields.file import FilerFileField
        
class ApplicationStateManager(models.Manager):
    def states_for_opening(self, opening):
        return self.filter(opening=opening)
        
    def states_for_user(self, user):
        return self.filter(user=user)
    



def get_upload_path(instance, filename):
    try:
        ins = ApplicationState.objects.all().order_by("-id")[0].id + 1
    except:
        ins = 1
    
    return os.path.join(
      "doc/application_%s" % ins,filename)



class ApplicationState(models.Model):
    """ This is the job application model """
    opening = models.OneToOneField(openings, verbose_name=_(u"Job Openings"))
    applicant = models.ForeignKey(User, verbose_name=_(u"Applicant"))
    #coverletter = models.FileField(upload_to=get_upload_path,verbose_name=_(u"cover letter"),blank=True,null=True)
    # resume = models.FileField(upload_to=get_upload_path,verbose_name=_(u"resume"),blank=True,null=True)
    coverletter = FilerFileField(verbose_name="Cover letter",null=True, blank=True,related_name='cover letter')
    resume = FilerFileField(verbose_name="Resume",null=True, blank=True,related_name='resume')
    refer = models.CharField(max_length=200,verbose_name=_(u"Person Referred"),blank=True,null=True)
    app_platform = models.CharField(max_length=200,verbose_name=_(u"Application platform"),blank=True,null=True)
    app_id = models.CharField(max_length=200,verbose_name=_(u"Application id"),blank=True,null=True)
    
    notes = models.TextField(max_length=1000,verbose_name=_(u"notes"),blank=True,null=True)
    objects = ApplicationStateManager()

    class Meta:
        verbose_name = _(u"Application state")
        verbose_name_plural = _(u"Application states")
        
    def __unicode__(self):
        return _(u"%(opening)s_%(applicant)s") % {'opening':self.opening,'applicant':self.applicant}
        
    def status_set(self):
        #print States.objects.filter(application=self)
        return States.objects.filter(application=self)

class States(models.Model):
    application = models.ForeignKey(ApplicationState,verbose_name=_(u"application"))
    name =  models.CharField(max_length=1000,verbose_name=_(u"state name"))
    notes =  models.TextField(max_length=1000,verbose_name=_(u"state notes"))  
    date_add = models.DateTimeField(verbose_name=_(u"add date"),default=datetime.datetime.now())

    class Meta:
        verbose_name = _(u"State")
        verbose_name_plural = _(u"States")
        
    def __unicode__(self):
        return _(u"%(name)s||%(date)s") % {'app':self.application,'name':self.name,'date':self.date_add}       