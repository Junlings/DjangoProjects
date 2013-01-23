import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from artwork.models import charts, data, equas, figures
from contributor.models import authors, publisher

from django.contrib.contenttypes.models import ContentType

from publications.models import publication


PUBLISH_PERIOD = (
    ('Monthly','Monthly'),
    ('Bi-Monthly','Bi-Monthly'),
    ('Yearly','Yearly'),
)

class journal(models.Model):
    name = models.CharField(verbose_name="Journal name",max_length=200,null=True,blank=True)
    shortname = models.CharField(verbose_name="Journal Shortname",max_length=100,null=True,blank=True)
    impact = models.CharField(verbose_name="Impact Rate",max_length=20,null=True,blank=True)
    peroidic = models.CharField(verbose_name="Publishing frequency",max_length=10,choices=PUBLISH_PERIOD,null=True,blank=True)
    nation = models.CharField(verbose_name="nation",max_length=30,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=30,null=True,blank=True)
    #publisher = models.CharField(verbose_name="publisher",max_length=30,null=True,blank=True)
    publisher = models.ForeignKey(publisher,verbose_name="publisher",null=True,blank=True)
    website = models.CharField(verbose_name="website",max_length=100,null=True,blank=True)
    notes = models.TextField(verbose_name="notes",max_length=500,null=True,blank=True)

    def __unicode__(self):
        return '%(id)s:%(name)s' % {'name':self.name,'id':str(self.id)}
    


class journalarticle(publication):
    M3 = models.CharField(verbose_name="Type of Article",max_length=20,null=True,blank=True)    
    T2 = models.ForeignKey(journal,verbose_name="Journal",null=True,blank=True)

    PY = models.CharField(verbose_name="Year",max_length=4,null=True,blank=True)
    VL = models.CharField(verbose_name="Volume",max_length=5,null=True,blank=True)
    IS = models.CharField(verbose_name="Issue",max_length=5,null=True,blank=True)
    SP = models.CharField(verbose_name="Pages",max_length=20,null=True,blank=True)
    M2 = models.CharField(verbose_name="Start Page",max_length=5,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=800,null=True,blank=True)
    ST = models.CharField(verbose_name="Short Title",max_length=800,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=800,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=200,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    ET = models.CharField(verbose_name="Epub Date",max_length=20,null=True,blank=True)
    SN = models.CharField(verbose_name="ISSN",max_length=20,null=True,blank=True)
    C2 = models.CharField(verbose_name="PMCID",max_length=20,null=True,blank=True)
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    C7 = models.CharField(verbose_name="Article Number",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    C6 = models.CharField(verbose_name="NIHMSID",max_length=20,null=True,blank=True)  
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)    
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    RI = models.CharField(verbose_name="Reviewed Item",max_length=20,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    C1 = models.CharField(verbose_name="Legal Note",max_length=20,null=True,blank=True)
    J2 = models.CharField(verbose_name="Alternate Journal",max_length=20,null=True,blank=True)
    OP = models.CharField(verbose_name="Original Publication",max_length=20,null=True,blank=True)
    RP = models.CharField(verbose_name="Reprint Edition",max_length=20,null=True,blank=True)    
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)    
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)  
    

    def get_keywords(self):
        
        return self.KWS.all()
        '''
        num = []
        for ke in content.KW.all():
            num.append(ke.id)    
        return num
        '''
        
    def get_authors(self):
        
        return self.AUs.all()
        
    class Meta:
        verbose_name = 'Journal Article'
 
