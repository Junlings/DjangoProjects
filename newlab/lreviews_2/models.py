import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from journal.models import journalarticle
from drafts.models import plaintext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from accounts.models import UserRefLib
import json

TEXT_CATE = (
    ('Purpose','Purpose'),
    ('Existing Work','Existing Work'),
    ('Methods','Methods'),
    ('results','results'),
    ('Issues','Issues'),
)

LIT_TYPE = (
    ('journal','journal'),
    ('conference','conference'),
    ('book','book'),
    ('regulation','regulation'),
    ('standard','standard'),
    ('thesis','thesis'),
)

QTYPE_CHOICES = (
    ('I', 'Text Input'),
    ('T', 'True/False'),
    ('M', 'Select One Choice'),
    ('C', 'Checkbox List'),
)


class reviewproj(models.Model):
    shortname = models.CharField(verbose_name='Title',max_length=100)
    slug    = models.SlugField(_('slug'), max_length=255, unique=True)
    
    topics = models.TextField(verbose_name='Topics',max_length=2000)
    associateLab = models.ForeignKey(UserRefLib,verbose_name='Literature Lab',null=True,blank=True)
    managers = models.ManyToManyField(User,verbose_name='Manager')
    contributors = models.ManyToManyField(User,verbose_name='Contributor',null=True,blank=True,related_name='contributor')

    visible = models.BooleanField(_('Review project is visible'))

    image = models.ImageField(verbose_name = _("image"),
                              upload_to= "media/images/questions" + "/%Y/%m/%d/",
                              null=True ,blank= True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Review Project")
        verbose_name_plural = _(u"Review Projects")
    
    def __unicode__(self):
        return 'Review project on %s ' % (self.shortname) #,self.creator.username)
    
    def get_questions(self):
        return reviewquestion.objects.filter(project=self)

    def get_question_order(self,order):
        return reviewquestion.objects.get(project=self,order=order)
        
    def get_allref_userlib_progress(self,request):
        if self.associateLab == None:
            return None
        else:
            reviewlib = {}
            for paper in self.associateLab.get_refs():
                reviewlib[paper] = {}
                reviewlib[paper] = 0
                allquestions = self.get_questions()
                for question in allquestions:
                    
                    answer = question.get_answer(paper.object_LB,request.user)
                    if answer != None:
                        reviewlib[paper] += 1
                    
                reviewlib[paper] = '%s/%s' % (reviewlib[paper],allquestions.count())    
            return reviewlib
    
    def get_allref_userlib(self):
        if self.associateLab == None:
            return None
        else:
            reviewlib = {}
            for paper in self.associateLab.get_refs():
                reviewlib[paper] = {}    
                
                for user in self.contributors.all():
                    reviewcount = singlereviews.objects.filter(question__project=self,object_LB=paper.object_LB,reviewer=user).count()
                    reviewlib[paper][user.username] = reviewcount
            return reviewlib
        
    def get_allreferences(self):
        reviews = singlereviews.objects.filter(question__project=self)
        
        label_set = {}
        for review in reviews:
            key = review.object_LB
            if key in label_set.keys():
                label_set[key] += 1
            else:
                
                label_set[key] = 1
            
        return label_set


class reviewquestion(models.Model):
    project = models.ForeignKey(reviewproj,verbose_name=_(u"Project"))    
    question = models.CharField(verbose_name="question",max_length=500)
    qtype = models.CharField(_('question type'), max_length=2,
                                choices=QTYPE_CHOICES)
    order = models.IntegerField(verbose_name = _("order"),
                                null=True, blank=True)
    required = models.BooleanField(_('required'), default=True)
    image = models.ImageField(verbose_name=_("image"),
                              upload_to= "survey/images/questions" + "/%Y/%m/%d/",
                              null=True, blank= True)    
    choice_num_min = models.IntegerField(_("minimum number of choices"),
                                         null=True, blank=True,)
    choice_num_max = models.IntegerField(_("maximum number of choices"),
                                         null=True, blank=True,)
    
    def get_choices(self):
        
        if self.qtype == 'M' or self.qtype == 'C':
            choices = Choice.objects.filter(question=self)
            
        elif self.qtype == 'T':
            choices = ['True','False']
        else:
            choices = []
        return choices
    
    def get_choices_html(self,label=None,question=None,user=None):
        
        try:
            answer = singlereviews.objects.get(question=question,object_LB=label,reviewer=user)
        
        except:
            answer = None
        
        if self.qtype == 'M':
            choices = Choice.objects.filter(question=self)
            choiceshtml = ''
             
            
            for choice in choices:
                if answer != None and answer.reviews == choice.text:
                    choiceshtml += '<input type="radio" id="question_%s" name ="question_%s" value="%s" checked="True"/> %s<br>' % (self.order,self.order,choice.text,choice.text)
                else:
                    choiceshtml += '<input type="radio" id="question_%s" name ="question_%s" value="%s"/> %s<br>' % (self.order,self.order,choice.text,choice.text)
            
        elif self.qtype == 'C':
            choices = Choice.objects.filter(question=self)
            choiceshtml = ''
            if answer != None:
                bb = answer.reviews[1:-1].split(',')
                jsonanswer = {}
                for b in bb:
                    aa = b.strip().split(':')
                    jsonanswer[int(aa[0][2:-1])] = aa[1].strip()
            else:
                jsonanswer = {}
            for choice in choices:
                
                if choice.order in jsonanswer.keys():
                    if answer != None and jsonanswer[choice.order] == "True":
                        choiceshtml += '<input type="checkbox" id="question_%s_%s" value="%s" checked="True" /> %s<br>' % (self.order,choice.order,choice.text,choice.text)
                    else:
                        choiceshtml += '<input type="checkbox" id="question_%s_%s" value="%s"/> %s<br>' % (self.order,choice.order,choice.text,choice.text)
                else:
                    choiceshtml += '<input type="checkbox" id="question_%s_%s" value="%s"/> %s<br>' % (self.order,choice.order,choice.text,choice.text)
  
        elif self.qtype == 'T':
            choiceshtml = ''
            
            if answer == None:
                sel_True = 'False'
                sel_False = 'False'
            elif answer.reviews == 'True':
                sel_True = 'checked="True"'
                sel_False = ''
            elif answer.reviews == 'False':
                sel_True = ''
                sel_False = 'checked="True"'
                
            choiceshtml += '<input type="radio" id="question_%s" name ="question_%s" value="%s" %s /> %s<br>' % (self.order,self.order,'True',sel_True,'True')
            choiceshtml += '<input type="radio" id="question_%s" name ="question_%s" value="%s" %s /> %s' % (self.order,self.order,'False',sel_False,'False')

        else:
            if answer == None:
                choiceshtml = '<TEXTAREA id="question_%s" ROWS=6 COLS=80 ></TEXTAREA>' % self.order
            else:
                choiceshtml = '<TEXTAREA id="question_%s" ROWS=6 COLS=80 >%s</TEXTAREA>' % (self.order, answer.reviews)
                
        return choiceshtml 


    def get_choices_ajax(self):
        if self.qtype == 'I':
            ajaxexp = 'a[%s] = $("#question_%s").val();' % (self.order,self.order) 

        elif self.qtype == 'M' or self.qtype == 'T':
            ajaxexp = 'a[%s] = $("#question_%s:checked").val();' % (self.order,self.order)
            
        elif self.qtype == 'C':
            choices = Choice.objects.filter(question=self)
            ajaxexp = 'a[%s] = {};' % self.order
            
            for choice in choices:
                ajaxexp += 'a[%s][%s] = $("#question_%s_%s").is(":checked");' % (self.order,choice.order,self.order,choice.order)
        else:
            pass
            
        return ajaxexp
            
        
    
    def get_answer(self,label,user):
        try:
            return singlereviews.objects.get(question=self,object_LB=label,reviewer=user)
            
        except:
            return None 
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Review Question")
        verbose_name_plural = _(u"Review Questions")
    
    def __unicode__(self):
        return 'project "%s":"%s"' % (self.project.shortname,self.question) #,self.creator.username)

class Choice(models.Model):
    ## validate question is of proper qtype
    question = models.ForeignKey(reviewquestion, related_name='choices',
                                 verbose_name=_('question'))
    text = models.CharField(_('choice text'), max_length=500)
    order = models.IntegerField(verbose_name = _("order"),
                                null=True, blank=True)
    image = models.ImageField(verbose_name = _("image"),
                              upload_to= "survey/images/questions" + "/%Y/%m/%d/",
                              null=True ,blank= True)
    
    @models.permalink
    def get_update_url(self):
        return ('choice-update', (), {'question_id': self.question.id,'choice_id' :self.id  })

    @property
    def count(self):
        if hasattr(self, '_count'):
            return self._count
        self._count = Answer.objects.filter(question=self.question_id,
                                            text=self.text).count()
        return self._count

    def __unicode__(self):
        return self.text

    class Meta:
        #unique_together = (('question', 'text'),)
        order_with_respect_to='question'
        ordering = ('question', 'order')
        



class singlereviews(models.Model):
    object_type = models.CharField(verbose_name="Type",choices=LIT_TYPE,max_length=20)
    object_LB = models.CharField(verbose_name="Label",max_length=20)    
    type = models.CharField(verbose_name="type",max_length=50,null=True,blank=True)
    reviewer = models.ForeignKey(User,verbose_name='Reviewer')
    question = models.ForeignKey(reviewquestion,verbose_name="question",null=True,blank=True)
    
    reviews = models.TextField(verbose_name="Text",max_length=10000,null=True,blank=True)

    addon = models.DateTimeField(verbose_name="Add on", auto_now_add=True)
    modifiedon = models.DateTimeField(verbose_name="Last modified on",auto_now=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = _(u"Review Comment")
        verbose_name_plural = _(u"Review Comment")
    
    def first_100_comment(self):
        return self.reviews[:100] + '......'
    
    def __unicode__(self):
        return '%s by %s' % (self.id,self.reviewer.username)    
    

        