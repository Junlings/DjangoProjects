import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, UserManager

""" This module suppose to be a request-response

Rules:
1. One request can/will answered by multiple response
2. Only the user within target_response_group can receive request and provide response
3. Only the user within allowed_request_group can send request
4. Only the user who send the specific response and view the corresponding response
5. request will be void after expiration date, or deactivated by the creator
"""

class crequests(models.Model):
    ''' The payment model '''
    initiator = models.ForeignKey(User, verbose_name=_(u"Initiator"))
    initiate_on = models.DateTimeField(verbose_name=_(u"Start Effective Date"),blank=True,default=datetime.datetime.now())
    expire_on = models.DateTimeField(verbose_name=_(u"Expire Date"),blank=True,default=datetime.datetime.now())
    active_state = models.BooleanField(verbose_name=_(u"Is Active?"), default=False, blank=True)
    response_state = models.IntegerField(verbose_name=_(u"Number of responses?"), default=0, blank=True)
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return "By_%(user)s_on_%(data_on)s" % {'user':self.initiator.username,'data_on':self.initiate_on}
        
    def group_target(self):
        self.group_target = 'default'
        
    def group_self(self):
        self.group_self = 'default'
        
class cresponses(models.Model):

    responser = models.ForeignKey(User, verbose_name=_(u"Responser"))
    response_on = models.DateTimeField(verbose_name=_(u"Response Effective Date"),blank=True,default=datetime.datetime.now())
    expire_on = models.DateTimeField(verbose_name=_(u"Expire Date"),blank=True,default=datetime.datetime.now())
    active_state = models.BooleanField(verbose_name=_(u"Is Active?"), default=False, blank=True)
    confirm_state = models.BooleanField(verbose_name=_(u"Is COnfirmed?"), default=False, blank=True) 
    notes = models.TextField(max_length=200,verbose_name=_(u"notes"), null=True, blank=True)
    
    class Meta:
        abstract = True

    def __unicode__(self):
        return "By_%(user)s_on_%(data_on)s" % {'user':self.responser.username,'data_on':self.response_on}

    def group_target(self):
        self.group_target = 'default'
        
    def group_self(self):
        self.group_self = 'default'
