import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from artwork.models import charts, data, equas, figures
from contributor.models import authors, publisher


from publications.models import publication


class conference(models.Model):
    T2 = models.CharField(verbose_name="Conference Name",max_length=400,null=True,blank=True)
    CY = models.CharField(verbose_name="Conference Location",max_length=200,null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=4,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    PB = models.ForeignKey(publisher,verbose_name="publisher",null=True,blank=True)
    #A2 = models.ManyToManyField(authors,verbose_name="Editor",null=True,blank=True)
    C1 = models.CharField(verbose_name="Place Published",max_length=200,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=100,null=True,blank=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"conference")
        verbose_name_plural = _(u"conferences")
    
    def __unicode__(self):
        return '%s %s' % (self.T2,self.PY)
    
class conferenceproceeding(models.Model):
    conference = models.ForeignKey(conference,verbose_name="Conference",null=True,blank=True)
    C3 = models.CharField(verbose_name="Proceedings Title",max_length=500,null=True,blank=True)
    C2 = models.CharField(verbose_name="Year Published",max_length=4,null=True,blank=True)
    NV = models.CharField(verbose_name="Number of Volumes",max_length=5,null=True,blank=True)
    ST = models.CharField(verbose_name="Short Title",max_length=200,null=True,blank=True)
    C5 = models.CharField(verbose_name="Packaging Method",max_length=20,null=True,blank=True)
    A3 = models.ManyToManyField(authors,verbose_name="Series Editor",null=True,blank=True,related_name='Series_Editor')
    A4 = models.ManyToManyField(authors,verbose_name="Sponsor",null=True,blank=True,related_name='Sponsor')
    T3 = models.CharField(verbose_name="Series Title",max_length=200,null=True,blank=True)
    ET = models.CharField(verbose_name="Edition",max_length=20,null=True,blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = _(u"conference proceeding")
        verbose_name_plural = _(u"conference proceedings")
    
    def __unicode__(self):
        return '%s' % self.C3

    def get_fulltext(self):
        fulltext1 = fulltext.objects.get(content_type=ContentType.objects.get(app_label="conference", model="conferenceproceeding"),object_id=self.id)
        if fulltext1:
            return True
        else:
            return False



    
class conferencepaper(publication):
    conference = models.ForeignKey(conference,verbose_name="Conference",null=True,blank=True)
    proceeding = models.ForeignKey(conferenceproceeding,verbose_name="Conference proceeding",null=True,blank=True)

    TAs = models.ManyToManyField(authors,verbose_name="Translated Author",null=True,blank=True,related_name='translation')
    TI = models.CharField(verbose_name="Title",max_length=400,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=400,null=True,blank=True)
    ST = models.CharField(verbose_name="Short Title",max_length=400,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=400,null=True,blank=True)
    VL = models.CharField(verbose_name="Volume",max_length=5,null=True,blank=True)
    SP = models.CharField(verbose_name="Pages",max_length=20,null=True,blank=True)
    M1 = models.CharField(verbose_name="Issue",max_length=20,null=True,blank=True)     
    UR = models.CharField(verbose_name="URL",max_length=200,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)    
    SN = models.CharField(verbose_name="ISSN",max_length=20,null=True,blank=True)
    #C2 = models.CharField(verbose_name="PMCID",max_length=20,null=True,blank=True)
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    #C7 = models.CharField(verbose_name="Article Number",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    #C6 = models.CharField(verbose_name="NIHMSID",max_length=20,null=True,blank=True)  
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    #RI = models.CharField(verbose_name="Reviewed Item",max_length=20,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)    
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    #DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)      

