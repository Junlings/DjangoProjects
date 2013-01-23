import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from publications.models import keywords
TEXT_CATE = (
    ('Purpose','Purpose'),
    ('Existing Work','Existing Work'),
    ('Methods','Methods'),
    ('results','results'),
    ('Issues','Issues'),
)

TEXT_TYPE = (
    ('LIT REVIEW','LIT REVIEW'),
    ('WRITE DRAFT','WRITE DRAFT'),
    ('WRITE Comments','WRITE Comments'),
    ('WRITE submission','WRITE submission'),
)

class images(models.Model):
    owner = models.ForeignKey(User, verbose_name=_("Owner")) 
    file = models.FileField(upload_to='doc/images/%Y/%m/%d',verbose_name=_(u"image"),blank=True)
    
class tables(models.Model):
    owner = models.ForeignKey(User, verbose_name=_("Owner")) 
    file = models.FileField(upload_to='doc/table/%Y/%m/%d',verbose_name=_(u"table"),blank=True)
    
class equations(models.Model):
    owner = models.ForeignKey(User, verbose_name=_("Owner")) 
    file = models.FileField(upload_to='doc/data/%Y/%m/%d',verbose_name=_(u"equation"),blank=True)

class plaintext(models.Model):
    context = models.TextField(verbose_name="Text",max_length=10000,null=True,blank=True)   
# the following are aggregration models

class plainparagraph(models.Model):
    texts = models.ManyToManyField(plaintext,verbose_name="Text",through='seqtext')
    tables = models.ManyToManyField(tables,verbose_name="Table",through='seqtable')
    images = models.ManyToManyField(images,verbose_name="Images",through='seqimage')
    equation = models.ManyToManyField(equations,verbose_name="Equations",through='seqequation')
    
class seqtext(models.Model):
    text = models.ForeignKey(plaintext)
    paragraph = models.ForeignKey(plainparagraph)
    seq = models.PositiveIntegerField()
  
  

    



class sections(models.Model):
    paragraph = models.ManyToManyField(plainparagraph,verbose_name=_(u"paragraphs"),through='seqparagraph')    
    
class seqparagraph(models.Model):
    paragraphs = models.ForeignKey(plainparagraph)
    section = models.ForeignKey(sections)
    seq = models.PositiveIntegerField()
 


    
class seqimage(models.Model):
    image = models.ForeignKey(images)
    paragraph = models.ForeignKey(plainparagraph)
    seq_local = models.PositiveIntegerField(null=True,blank=True)
    seq_global = models.PositiveIntegerField(null=True,blank=True)
    caption = models.CharField(verbose_name='Caption',max_length=200,null=True,blank=True)
    
class seqtable(models.Model):
    table = models.ForeignKey(tables)
    paragraph = models.ForeignKey(plainparagraph)
    seq_local = models.PositiveIntegerField(null=True,blank=True)
    seq_global = models.PositiveIntegerField(null=True,blank=True)
    caption = models.CharField(verbose_name='Caption',max_length=200,null=True,blank=True)

class seqequation(models.Model):
    equation = models.ForeignKey(equations)
    paragraph = models.ForeignKey(plainparagraph)
    seq_local = models.PositiveIntegerField(null=True,blank=True)
    seq_global = models.PositiveIntegerField(null=True,blank=True)
    caption = models.CharField(verbose_name='Caption',max_length=200,null=True,blank=True)


    

class document(models.Model):
    owner = models.ForeignKey(User, verbose_name=_("Owner"))
    title = models.CharField(verbose_name="Document Title",max_length=100,null=True,blank=True)
    KW = models.ManyToManyField(keywords,verbose_name="Keywords",null=True,blank=True)
    sections = models.ManyToManyField(sections,verbose_name="Sections",null=True,blank=True,through='seqsection')
  
class seqsection(models.Model):
    section = models.ForeignKey(sections)
    document = models.ForeignKey(document)
    seq1 = models.PositiveIntegerField(verbose_name='level 1 Seq',null=True,blank=True)
    seq2 = models.PositiveIntegerField(verbose_name='level 2 Seq',null=True,blank=True)
    seq3 = models.PositiveIntegerField(verbose_name='level 3 Seq',null=True,blank=True)
    seq4 = models.PositiveIntegerField(verbose_name='level 4 Seq',null=True,blank=True)
    caption = models.CharField(verbose_name='Caption',max_length=200,null=True,blank=True)
    
  
    
    



