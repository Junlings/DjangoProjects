from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from contributor.models import authors,publisher
PUBLICATION_TYPE = (
    ('book','book'),
    ('thes','thes'),
    ('journalarticle','journalarticle'),
    ('conferencepaper','conferencepaper'),
    ('rprt','rprt'),
    ('stand','stand')
    
    
)

class keywords(models.Model):
    KW = models.CharField(verbose_name="Keywords",max_length=50,null=True,blank=True)
    
    def __unicode__(self):
        return '%s %s' % (self.id,self.KW)


class publication(models.Model):
    
    RIS = models.TextField(verbose_name=_(u"RIS"),max_length=2000,null=True,blank=True)    
    AUs = models.ManyToManyField(authors,verbose_name="Authors",null=True,blank=True, through='Authorship')
    KWS = models.ManyToManyField(keywords,verbose_name="Keywords",null=True,blank=True)
    
    label = models.CharField(verbose_name=_(u"label"),max_length=100,unique=True)
    doc = models.FileField(upload_to='doc/fulltext',verbose_name=_(u"document"),null=True,blank=True)
    doclink = models.URLField(max_length=200,null=True,blank=True)
    
    #Audit field
    created_by = models.ForeignKey(User,verbose_name=_(u"User added"),related_name='create_user',null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add = True)
    modified_by = models.ForeignKey(User,verbose_name=_(u"User last modified"),related_name='modify_user',null=True,blank=True)
    updated_on = models.DateTimeField(auto_now = True)
    
    
class Authorship(models.Model):
    author = models.ForeignKey(authors,verbose_name='authors')
    publication = models.ForeignKey(publication,verbose_name='publication')
    sequence = models.PositiveIntegerField()
    communication = models.NullBooleanField(verbose_name='communication author')

    def __unicode__(self):
        return '%s' % self.sequence
    
  
    
class book(publication):
    
    PB = models.ForeignKey(publisher,verbose_name="publisher",null=True,blank=True)
    A3 = models.ManyToManyField(authors,verbose_name="Editors",related_name='Editors',null=True,blank=True)
    C4 = models.ManyToManyField(authors,verbose_name="Reviewers",related_name='Reviewers',null=True,blank=True)
    A2 = models.ManyToManyField(authors,verbose_name="Series Editors",related_name='Series_Editors',null=True,blank=True)
    A4 = models.ManyToManyField(authors,verbose_name="Translators",related_name='Translators',null=True,blank=True)
    TA = models.ManyToManyField(authors,verbose_name="Translator authors",related_name='Translator authors',null=True,blank=True)
    
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    M1 = models.CharField(verbose_name="Series Volume",max_length=20,null=True,blank=True)

    TI = models.CharField(verbose_name="Title",max_length=400,null=True,blank=True)
    C3 = models.CharField(verbose_name="Title Prefix",max_length=20,null=True,blank=True)
    SP = models.CharField(verbose_name="Number of Pages",max_length=20,null=True,blank=True)
    ST = models.CharField(verbose_name="Short Title",max_length=20,null=True,blank=True)

    RP = models.CharField(verbose_name="Reprint Edition",max_length=20,null=True,blank=True)

    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    NV = models.CharField(verbose_name="Number of Volumes",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)

    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="City",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    J2 = models.CharField(verbose_name="Abbreviation",max_length=20,null=True,blank=True)
    SN = models.CharField(verbose_name="ISBN",max_length=20,null=True,blank=True)
    SE = models.CharField(verbose_name="Pages",max_length=20,null=True,blank=True)
    OP = models.CharField(verbose_name="Original Publication",max_length=20,null=True,blank=True)

    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)

    M3 = models.CharField(verbose_name="Type of Work",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=400,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=20,null=True,blank=True)
    VL = models.CharField(verbose_name="Volume",max_length=20,null=True,blank=True)
    T2 = models.CharField(verbose_name="Series Title",max_length=20,null=True,blank=True)
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    ET = models.CharField(verbose_name="Edition",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return '%s' % self.id

  

    
class thes(publication):

    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=400,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=20,null=True,blank=True)
    T2 = models.CharField(verbose_name="Academic Department",max_length=20,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="City",max_length=20,null=True,blank=True)
    
    M3 = models.CharField(verbose_name="Thesis Type",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    VL = models.CharField(verbose_name="Degree",max_length=20,null=True,blank=True)
    SP = models.CharField(verbose_name="Number of Pages",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)
    LB = models.CharField(verbose_name="Label",max_length=20,null=True,blank=True)
    #TY = models.CharField(verbose_name="`THES`",max_length=20,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    ST = models.CharField(verbose_name="Short Title",max_length=400,null=True,blank=True)
    PB = models.CharField(verbose_name="University",max_length=200,null=True,blank=True)
    A3 = models.CharField(verbose_name="Advisor",max_length=20,null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=4,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=400,null=True,blank=True)
    M1 = models.CharField(verbose_name="Document Number",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return '%s' % self.id

    def get_AU(self):
        if len(self.AU.all()) > 0:
            return self.AU.all()[0]
        else:
            return None


        
class stand(publication):

    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=4000,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=20,null=True,blank=True)
    T2 = models.CharField(verbose_name="Section Title",max_length=20,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    T3 = models.CharField(verbose_name="Paper Number",max_length=20,null=True,blank=True)
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="Place Published",max_length=20,null=True,blank=True)
    AU = models.CharField(verbose_name="Institution",max_length=20,null=True,blank=True)
    SE = models.CharField(verbose_name="Section Number",max_length=20,null=True,blank=True)
    M3 = models.CharField(verbose_name="Type of Work",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    VL = models.CharField(verbose_name="Rule Number",max_length=20,null=True,blank=True)
    SP = models.CharField(verbose_name="Pages",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    LB = models.CharField(verbose_name="Label",max_length=20,null=True,blank=True)
    #TY = models.CharField(verbose_name="`STAND`",max_length=20,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    J2 = models.CharField(verbose_name="Abbreviation",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    PB = models.ForeignKey(publisher,verbose_name="publisher",null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=20,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=400,null=True,blank=True)
    M1 = models.CharField(verbose_name="Start Page",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)
    NV = models.CharField(verbose_name="Session Number",max_length=20,null=True,blank=True)
    SN = models.CharField(verbose_name="Document Number",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return '%s' % self.id






    
class rprt(publication):
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=4000,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=100,null=True,blank=True)
    T2 = models.CharField(verbose_name="Series Title",max_length=100,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="City",max_length=20,null=True,blank=True)
    C6 = models.CharField(verbose_name="issue",max_length=20,null=True,blank=True)

    ET = models.CharField(verbose_name="Edition",max_length=20,null=True,blank=True)
    
    M3 = models.CharField(verbose_name="Type",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    VL = models.CharField(verbose_name="Volume",max_length=20,null=True,blank=True)
    SP = models.CharField(verbose_name="Pages",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    LB = models.CharField(verbose_name="Label",max_length=20,null=True,blank=True)

    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    J2 = models.CharField(verbose_name="Alternate Title",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    PB = models.ForeignKey(publisher,verbose_name="publisher",null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=20,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=400,null=True,blank=True)
    M1 = models.CharField(verbose_name="Document Number",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)
    NV = models.CharField(verbose_name="Series Volume",max_length=20,null=True,blank=True)
    SN = models.CharField(verbose_name="Report Number",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return '%s' % self.id





