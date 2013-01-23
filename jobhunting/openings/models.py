from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from qualifications.models import skills, certifications
from companies.models import companys
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


EDUCATION_LEVEL = (
    ('Ph.D','Ph.D'),
    ('M.S.','M.S.'),
    ('B.S.','B.S.'),
    ('B.A.','B.A.'),
    ('High school','High school'),
    ('MBA','MBA'),   
    
)

OPENNING_TYPE = (
    ('Intern','Intern'),
    ('Full Time','Full Time'),
    ('Contract','Contract'),
    ('Part Time','Part Time'),
)



        
class openings(models.Model):
    company = models.ForeignKey(companys,verbose_name=_(u"company"))
    title = models.CharField(max_length=200,verbose_name=_(u"title"))
    type = models.CharField(max_length=100,choices=OPENNING_TYPE, verbose_name=_(u"Openning type"))
    date_add = models.DateField(verbose_name=_(u"add date"),auto_now_add=True)
    date_expire = models.DateField(verbose_name=_(u"expire date"),blank=True,null=True)
    location_state = models.CharField(max_length=100,verbose_name=_(u"State"))
    location_city = models.CharField(max_length=100,verbose_name=_(u"City"))
    
    description = models.TextField(max_length=2000,verbose_name=_(u"description"),blank=True,null=True)
    #accept_skillset = models.ManyToManyField(skills,verbose_name=_(u"Required skills"),blank=True,null=True,related_name='accept_skill')
    #accept_certifications = models.ManyToManyField(certifications,verbose_name=_(u"Required certifications"),blank=True,null=True,related_name='accept_cerification')
    #accept_education = models.CharField(max_length=100,choices=EDUCATION_LEVEL, verbose_name=_(u"accept education"),blank=True,null=True)
    #accept_experience = models.CharField(max_length=300,verbose_name=_(u"accept experience"),blank=True,null=True)
    
    #pre_skillset = models.ManyToManyField(skills,verbose_name=_(u"Preferred skills"),blank=True,null=True,related_name='pre_skill')
    #pre_certification = models.ManyToManyField(certifications,verbose_name=_(u"Preferred certifications"),blank=True,null=True,related_name='pre_cerification')
    #pre_education = models.CharField(max_length=100,choices=EDUCATION_LEVEL,verbose_name=_(u"Preferred education"),blank=True,null=True)
    #pre_experience = models.CharField(max_length=300,verbose_name=_(u"Preferred experience"),blank=True,null=True)
    source = models.CharField(max_length=300,verbose_name=_(u"Openning Source"),blank=True,null=True)
    active = models.BooleanField(verbose_name=_(u"still active"),default=True)
    notes = models.TextField(max_length=3000,verbose_name=_(u"Openning Notes"),blank=True,null=True)
    
    class Meta:
        verbose_name = _(u"opening")
        verbose_name_plural = _(u"opennings")
        
    def __unicode__(self):
        return _(u"%(company)s_%(title)s") % {'company':self.company.abbrname,'title':self.title}
        

        

REQ_TYPE = (
    ('Eduction','Eduction'),
    ('Skills','Skills'),
    ('EXperience','Experience'),
    ('Certification','Certification'),
    ('Security','Security'),
    ('Physical condition','Physical condition'),
    ('Other','Other'),
)

REQ_PRE = (
    ('MUST','MUST'),
    ('ACCEPT','ACCEPT'),
    ('PREFERRED','PREFERRED'),
    ('OTHER','OTHER'),
)


class requirement(models.Model):
    type = models.CharField(max_length=50,verbose_name=_(u"Type"),choices=REQ_TYPE)
    openning = models.ForeignKey(openings,verbose_name=_(u"Openning"))
    desciption = models.CharField(max_length=300,verbose_name=_(u"description"))
    preference = models.CharField(max_length=50,verbose_name=_(u"preference"),choices=REQ_PRE)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType,blank=True,null=True)
    object_id = models.PositiveIntegerField(blank=True,null=True)      
    

    class Meta:
        verbose_name = _(u"requirement")
        verbose_name_plural = _(u"requirements")
        
    def __unicode__(self):
        return _(u"%(openning)s_%(type)s") % {'openning':self.openning,'type':self.type}