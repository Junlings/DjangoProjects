from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class figures(models.Model):
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)
  
    
class equas(models.Model):
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)


class charts(models.Model):
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)



class data(models.Model):
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)



class figurerefer(models.Model):
    figure = models.OneToOneField(figures,verbose_name="figure")
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=400,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=20,null=True,blank=True)
    T2 = models.CharField(verbose_name="Image Source Program",max_length=20,null=True,blank=True)
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="City",max_length=20,null=True,blank=True)
    AU = models.CharField(verbose_name="Created By",max_length=20,null=True,blank=True)
    M3 = models.CharField(verbose_name="Type of Image",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    ET = models.CharField(verbose_name="Version",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    VL = models.CharField(verbose_name="Image Size",max_length=20,null=True,blank=True)
    SP = models.CharField(verbose_name="Description",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    LB = models.CharField(verbose_name="Label",max_length=20,null=True,blank=True)
    TY = models.CharField(verbose_name="`FIGURE`",max_length=20,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    PB = models.CharField(verbose_name="Publisher",max_length=20,null=True,blank=True)
    A2 = models.CharField(verbose_name="Name of File",max_length=20,null=True,blank=True)
    KW = models.CharField(verbose_name="Keywords",max_length=20,null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=20,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=20,null=True,blank=True)
    M1 = models.CharField(verbose_name="Number",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    CT = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    ER = models.CharField(verbose_name="{IGNORE}",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return self.index





class equarefer(models.Model):
    equa = models.OneToOneField(equas,verbose_name="Equation")
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=400,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=20,null=True,blank=True)
    T2 = models.CharField(verbose_name="Image Source Program",max_length=20,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="City",max_length=20,null=True,blank=True)
    AU = models.CharField(verbose_name="Created By",max_length=20,null=True,blank=True)
    M3 = models.CharField(verbose_name="Type of Image",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    ET = models.CharField(verbose_name="Version",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    VL = models.CharField(verbose_name="Image Size",max_length=20,null=True,blank=True)
    SP = models.CharField(verbose_name="Description",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)
    LB = models.CharField(verbose_name="Label",max_length=20,null=True,blank=True)
    TY = models.CharField(verbose_name="`EQUA`",max_length=20,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    PB = models.CharField(verbose_name="Publisher",max_length=20,null=True,blank=True)
    A2 = models.CharField(verbose_name="Name of File",max_length=20,null=True,blank=True)
    KW = models.CharField(verbose_name="Keywords",max_length=20,null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=20,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=20,null=True,blank=True)
    M1 = models.CharField(verbose_name="Number",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    ER = models.CharField(verbose_name="{IGNORE}",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return self.index

class datarefer(models.Model):
    data = models.OneToOneField(data,verbose_name="Data")
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=400,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=20,null=True,blank=True)
    SN = models.CharField(verbose_name="ISSN",max_length=20,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    T3 = models.CharField(verbose_name="Series Title",max_length=20,null=True,blank=True)
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="City",max_length=20,null=True,blank=True)
    AU = models.CharField(verbose_name="Investigators",max_length=20,null=True,blank=True)
    SE = models.CharField(verbose_name="Original Release Date",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    ET = models.CharField(verbose_name="Version",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date of Collection",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    LB = models.CharField(verbose_name="Label",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)
    TY = models.CharField(verbose_name="DATA",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    J2 = models.CharField(verbose_name="Abbreviation",max_length=20,null=True,blank=True)
    ST = models.CharField(verbose_name="Short Title",max_length=20,null=True,blank=True)
    PB = models.CharField(verbose_name="Distributor",max_length=20,null=True,blank=True)
    A2 = models.CharField(verbose_name="Producer",max_length=20,null=True,blank=True)
    KW = models.CharField(verbose_name="Keywords",max_length=20,null=True,blank=True)
    A4 = models.CharField(verbose_name="Funding Agency",max_length=20,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=20,null=True,blank=True)
    C3 = models.CharField(verbose_name="Data Type",max_length=20,null=True,blank=True)
    C2 = models.CharField(verbose_name="Unit of Observation",max_length=20,null=True,blank=True)
    C1 = models.CharField(verbose_name="Time Period",max_length=20,null=True,blank=True)
    OP = models.CharField(verbose_name="Version History",max_length=20,null=True,blank=True)
    RI = models.CharField(verbose_name="Geographic Coverage",max_length=20,null=True,blank=True)
    NV = models.CharField(verbose_name="Study Number",max_length=20,null=True,blank=True)
    C4 = models.CharField(verbose_name="Dataset(s)",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return self.index



class chartrefer(models.Model):
    chart = models.OneToOneField(charts,verbose_name="Chart")
    DO = models.CharField(verbose_name="DOI",max_length=20,null=True,blank=True)
    AB = models.TextField(verbose_name="Abstract",max_length=400,null=True,blank=True)
    AD = models.CharField(verbose_name="Author Address",max_length=20,null=True,blank=True)
    T2 = models.CharField(verbose_name="Image Source Program",max_length=20,null=True,blank=True)
    CA = models.CharField(verbose_name="Caption",max_length=20,null=True,blank=True)
    DB = models.CharField(verbose_name="Name of Database",max_length=20,null=True,blank=True)
    AN = models.CharField(verbose_name="Accession Number",max_length=20,null=True,blank=True)
    CY = models.CharField(verbose_name="City",max_length=20,null=True,blank=True)
    AU = models.CharField(verbose_name="Created By",max_length=20,null=True,blank=True)
    M3 = models.CharField(verbose_name="Type of Image",max_length=20,null=True,blank=True)
    L1 = models.CharField(verbose_name="File Attachments",max_length=20,null=True,blank=True)
    ET = models.CharField(verbose_name="Version",max_length=20,null=True,blank=True)
    DA = models.CharField(verbose_name="Date",max_length=20,null=True,blank=True)
    VL = models.CharField(verbose_name="Image Size",max_length=20,null=True,blank=True)
    SP = models.CharField(verbose_name="Description",max_length=20,null=True,blank=True)
    DP = models.CharField(verbose_name="Database Provider",max_length=20,null=True,blank=True)
    CN = models.CharField(verbose_name="Call Number",max_length=20,null=True,blank=True)
    index = models.CharField(verbose_name="Custom identification",max_length=20,null=True,blank=True)
    LB = models.CharField(verbose_name="Label",max_length=20,null=True,blank=True)
    TY = models.CharField(verbose_name="`CHART`",max_length=20,null=True,blank=True)
    TT = models.CharField(verbose_name="Translated Title",max_length=20,null=True,blank=True)
    LA = models.CharField(verbose_name="Language",max_length=20,null=True,blank=True)
    L4 = models.CharField(verbose_name="Figure",max_length=20,null=True,blank=True)
    N1 = models.CharField(verbose_name="Notes",max_length=20,null=True,blank=True)
    UR = models.CharField(verbose_name="URL",max_length=20,null=True,blank=True)
    PB = models.CharField(verbose_name="Publisher",max_length=20,null=True,blank=True)
    A2 = models.CharField(verbose_name="Name of File",max_length=20,null=True,blank=True)
    KW = models.CharField(verbose_name="Keywords",max_length=20,null=True,blank=True)
    PY = models.CharField(verbose_name="Year",max_length=20,null=True,blank=True)
    TI = models.CharField(verbose_name="Title",max_length=20,null=True,blank=True)
    M1 = models.CharField(verbose_name="Number",max_length=20,null=True,blank=True)
    RN = models.CharField(verbose_name="Research Notes",max_length=20,null=True,blank=True)
    Y2 = models.CharField(verbose_name="Access Date",max_length=20,null=True,blank=True)
    ER = models.CharField(verbose_name="{IGNORE}",max_length=20,null=True,blank=True)
    TA = models.CharField(verbose_name="Translated Author",max_length=20,null=True,blank=True)

    def __unicode__(self):
        return self.index
