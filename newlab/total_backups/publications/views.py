# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, render
from django.template import RequestContext
from models import book, stand, thes,rprt

#from forms import MeetingForm, TasksForm, TransactionForm, TransactionDocForm, TransactionReportForm, Transaction_Monthly_Form
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from settings import ROOT_URL


from contributor.models import authors   # import author
from publications.models import keywords

from django.db.models import Q
import pickle as pickle
from django.contrib.contenttypes.models import ContentType
from lreviews_2.models import singlereviews
from journal.models import *
from conference.models import *
from accounts.models import UserRefLib, UserRef

def journal_list(request):
    alljournal = journal.objects.all() #filter(Person=request.user)
    alljournalpaper = journalarticle.objects.all() #filter(Person=request.user)
    alljournalpaperfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="journal", model="journalarticle")) #filter(Person=request.user) 
    item_list = alljournalpaper
    
    
    fields = ['id','LB','get_title']
    return render_to_response('pub_generic_list.html',{'item_list':item_list,'fields':fields,
                                                    
                                                    },context_instance=RequestContext(request))

def publication_index(request):

    info = {}
    alljournal = journal.objects.all() #filter(Person=request.user)
    alljournalpaper = journalarticle.objects.all() #filter(Person=request.user)
    alljournalpaperfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="journal", model="journalarticle")) #filter(Person=request.user) 
    info['journal'] = {'journal':alljournal.count(),
                       'paper':alljournalpaper.count(),
                       'fulltext':alljournalpaperfulltext.count()}
    

    allconference = conference.objects.all() #filter(Person=request.user)
    allprocd = conferenceproceeding.objects.all() #filter(Person=request.user)
    
    allcpaper = conferencepaper.objects.all() #filter(Person=request.user)
    allcpaperfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="conference", model="conferencepaper")) #filter(Person=request.user) 
    info['conf'] = {'conf':allconference.count(),
                    'proc':allprocd.count(),
                       'cpaper':allcpaper.count(),
                       'fulltext':allcpaperfulltext.count()}

    allbook = book.objects.all() #filter(Person=request.user)
    allbookfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="book"))
    info['book'] = {'book':allbook.count(),
                       'fulltext':allbookfulltext.count()}
    
    allstand = stand.objects.all() #filter(Person=request.user)
    allstandfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="stand"))
    info['stand'] = {'stand':allstand.count(),
                       'fulltext':allstandfulltext.count()}  
  
    allthes = thes.objects.all() #filter(Person=request.user)
    allthesfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="thes"))
    info['thes'] = {'thes':allthes.count(),
                       'fulltext':allthesfulltext.count()}      

    allrprt = rprt.objects.all() #filter(Person=request.user)
    allrprtfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="rprt"))
    info['rprt'] = {'rprt':allrprt.count(),
                       'fulltext':allrprtfulltext.count()}     
    #stand, thes,rprt


    return render_to_response('publication_index.html',{'info':info,
                                                    
                                                    },context_instance=RequestContext(request))


def publication_lb_index(request,label):
    
    res = publication_get_html(request,label)
    
    # get involved userlib
    libinvolve = UserRef.objects.filter(object_LB=label)
    
    
    
    if len(res) > 0:
        pub,ptype = res

 
        return render_to_response('publication_details.html',{'pub':pub,
                                                              'libinvolve':libinvolve,
                                                        },context_instance=RequestContext(request))    
    else:
        return render_to_response('no_label_found.html',{
                                                      'label2':label,
                                                    },context_instance=RequestContext(request))         
 
def publication_get_html(request,label):
    pub = journal_by_label(request,label)
    if pub != None:
        return pub,'journal'         
    
    pub = conference_by_label(request,label)
    if pub != None:
        return pub,'conference'
    
    pub = thesis_by_label(request,label)
    if pub != None:
        return pub,'thesis'    
    
    else:
        return ''      
    

def journal_by_label(request,label):
    try:
        p1 = journalarticle.objects.get(label=label) #filter(Person=request.user)
        
        
    except:
        return None
    
    try:
        authors = p1.AUs.all()
        #authorshtml = ''
        #for author in authors:
        #    authorshtml += 'author/%s/"> %s </a> <br> ' % (author.id, author.firstname+' ' + author.lastname )
        
    except:
        authorshtml = ''
    
    try:
        KWs = p1.KWS.all()
    except:
        KWs = None    

        
    reviews = singlereviews.objects.filter(object_LB=p1.label)
    
    return render(request,'paper_details.html',{'paper':p1,
                                                    'authors':authors,
                                                    'KWs':KWs,
                                                    },context_instance=RequestContext(request))    


def conference_by_label(request,label):
    try:
        p1 = conferencepaper.objects.get(LB=label) #filter(Person=request.user)
    except:
        return None
    
    try:
        authors = p1.AUs.all()
    except:
        authors = None
    
    try:
        content = p1.get_content()
    except:
        content = None    
    try:
        placement = p1.get_placement()
    except:
        placement = None    
    
    try:
        KWs = p1.get_KW()
    except:
        KWs = None    
    try:
        jfulltext = fulltext.objects.get(content_type=ContentType.objects.get(app_label="conference", model="conferencepaper"),object_id=p1.id) #filter(Person=request.user)
    except:
        jfulltext = None
        
    reviews = singlereviews.objects.filter(object_LB=p1.LB)
    return render(request,'cpaper_details.html',{'paper':p1,
                                                    'authors':authors,
                                                    'content':content,
                                                    'placement':placement,
                                                    'KWs':KWs,
                                                    'reviews':reviews,
                                                    'fulltext':jfulltext,
                                                    },context_instance=RequestContext(request))    



def thesis_by_label(request,label):
    try:
        p1 = thes.objects.get(LB=label) #filter(Person=request.user)
    except:
        return None
    
    reviews = singlereviews.objects.filter(object_LB=p1.LB)
    try:
        jfulltext = fulltext.objects.get(content_type=ContentType.objects.get(app_label="publications", model="thes"),object_id=p1.id) #filter(Person=request.user)
    except:
        jfulltext = None
        
    return render_to_response('thes_details.html',{'paper':p1,
                                                    'reviews':reviews,
                                                    'fulltext':jfulltext,
                                                    },context_instance=RequestContext(request))    

def book_by_label(request,label):
    try:
        p1 = thes.objects.get(LB=label) #filter(Person=request.user)
    except:
        return None
    reviews = singlereviews.objects.filter(object_LB=p1.LB)
    try:
        jfulltext = fulltext.objects.get(content_type=ContentType.objects.get(app_label="publications", model="thes"),object_id=p1.id) #filter(Person=request.user)
    except:
        jfulltext = None
        
    return render_to_response('paper_details.html',{'paper':p1,
                                                    'reviews':reviews,
                                                    'fulltext':jfulltext,
                                                    },context_instance=RequestContext(request))

def standard_by_label(request,label):
    p1 = thes.objects.get(LB=label) #filter(Person=request.user)

    reviews = singlereviews.objects.filter(object_LB=p1.LB)
    try:
        jfulltext = fulltext.objects.get(content_type=ContentType.objects.get(app_label="publications", model="thes"),object_id=p1.id) #filter(Person=request.user)
    except:
        jfulltext = None
        
    return render_to_response('paper_details.html',{'paper':p1,
                                                    'reviews':reviews,
                                                    'fulltext':jfulltext,
                                                    },context_instance=RequestContext(request))    