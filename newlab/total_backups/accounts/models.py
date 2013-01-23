from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from djangoextension.contacts.models import address, social
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


LIT_TYPE = (
    ('journal','journal'),
    ('conference','conference'),
    ('book','book'),
    ('regulation','regulation'),
    ('standard','standard'),
    ('thesis','thesis'),
)

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
        


    
    
class UserRefLib(models.Model):
    name = models.CharField(max_length=100,verbose_name='Lib. Name')
    Owner = models.ForeignKey(User,verbose_name='Lib. Owner')
    addon = models.DateTimeField(verbose_name="Add on", auto_now_add=True)
    Contributor = models.ManyToManyField(User,verbose_name='Lib. Contributor',null=True,blank=True,related_name='lib contributor')
    
    class Meta:
        verbose_name = _(u"user Library")
        verbose_name_plural = _(u"user Librarys")
        
    def __unicode__(self):
        return _(u"%(name)s by %(user)s") % {'user':self.Owner.username,'name':self.name}#_(u"%(name) by %(user)s") % {'user':self.Owner,'name':self.name}
        
    def count_ref(self):
        refs = UserRef.objects.filter(Lib=self)
        return refs.count()
        
    def get_refs(self):
        refs = UserRef.objects.filter(Lib=self)
        return refs
    


        
class UserRef(models.Model):
    object_type = models.CharField(verbose_name="Type",choices=LIT_TYPE,max_length=20)
    object_LB = models.CharField(verbose_name="Label",max_length=20)
    note = models.TextField(verbose_name="Note",max_length=500)
    addon = models.DateTimeField(verbose_name="Add on", auto_now_add=True)
    addby = models.ForeignKey(User,verbose_name='Add by',null=True,blank=True)
    Lib = models.ForeignKey(UserRefLib)    
    
        