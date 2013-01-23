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

from  django.template.loader import get_template
from django.template import Context, Template

from forms import journalarticleForm
def publication_keyword_detail(request,id):
    ''' provide keyword and related publication list table'''
    kw = keywords.objects.get(pk=id)
    pubs = publication.objects.filter(KWS__in=[kw])
    objs = []
    
    for pub in pubs:
        objs.append(get_child_by_label(pub.label))
        
    
    return render_to_response('keywords_details.html',{'kw':kw,
                                                       'pubs':objs
                                                    },context_instance=RequestContext(request))    

   
def journal_paper_list(request):
    alljournalpaper = journalarticle.objects.all() #filter(Person=request.user)
    item_list = alljournalpaper
    fields = ['id','label','TI','T2','doc']

    return render_to_response('pub_generic_list.html',{'item_list':item_list, 'fields':fields                                
                                                    },context_instance=RequestContext(request))

def conference_paper_list(request):

    allcpaper = conferencepaper.objects.all() #filter(Person=request.user)
    item_list = allcpaper
    
    
    fields = ['id','label','TI','conference','doc']
    return render_to_response('pub_generic_list.html',{'item_list':item_list,'fields':fields,                                 
                                                    },context_instance=RequestContext(request))
 
def report_paper_list(request):

    allpaper = rprt.objects.all() #filter(Person=request.user)
    item_list = allpaper
    fields = ['id','label','TI','SN','doc']
    return render_to_response('pub_generic_list.html',{'item_list':item_list,'fields':fields,                                 
                                                    },context_instance=RequestContext(request))

def thesis_paper_list(request):

    allpaper = thes.objects.all() #filter(Person=request.user)
    item_list = allpaper
    fields = ['id','label','TI','PB','doc']
    return render_to_response('pub_generic_list.html',{'item_list':item_list,'fields':fields,                                 
                                                    },context_instance=RequestContext(request))
def books_paper_list(request):

    allpaper = book.objects.all() #filter(Person=request.user)
    item_list = allpaper
    fields = ['id','label','TI','PB','doc']
    return render_to_response('pub_generic_list.html',{'item_list':item_list,'fields':fields,                                 
                                                    },context_instance=RequestContext(request))    

def stands_paper_list(request):

    allpaper = stand.objects.all() #filter(Person=request.user)
    item_list = allpaper
    fields = ['id','label','TI','PB','doc']
    return render_to_response('pub_generic_list.html',{'item_list':item_list,'fields':fields,                                 
                                                    },context_instance=RequestContext(request))
    
def publication_index(request):

    info = {}
    alljournal = journal.objects.all() #filter(Person=request.user)
    alljournalpaper = journalarticle.objects.all() #filter(Person=request.user)
    #alljournalpaperfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="journal", model="journalarticle")) #filter(Person=request.user) 
    info['journal'] = {'journal':alljournal.count(),
                       'paper':alljournalpaper.count()}
    

    allconference = conference.objects.all() #filter(Person=request.user)
    allprocd = conferenceproceeding.objects.all() #filter(Person=request.user)
    
    allcpaper = conferencepaper.objects.all() #filter(Person=request.user)
    #allcpaperfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="conference", model="conferencepaper")) #filter(Person=request.user) 
    info['conf'] = {'conf':allconference.count(),
                    'proc':allprocd.count(),
                       'cpaper':allcpaper.count()}

    allbook = book.objects.all() #filter(Person=request.user)
    #allbookfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="book"))
    info['book'] = {'book':allbook.count()}
    
    allstand = stand.objects.all() #filter(Person=request.user)
    #allstandfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="stand"))
    info['stand'] = {'stand':allstand.count()}  
  
    allthes = thes.objects.all() #filter(Person=request.user)
    #allthesfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="thes"))
    info['thes'] = {'thes':allthes.count()}      

    allrprt = rprt.objects.all() #filter(Person=request.user)
    #allrprtfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="publications", model="rprt"))
    info['rprt'] = {'rprt':allrprt.count()}     
    #stand, thes,rprt


    return render_to_response('publication_index.html',{'info':info,
                                                    
                                                    },context_instance=RequestContext(request))

def get_child_by_label(label):
    try:
        obj = journalarticle.objects.get(label=label)
        return obj
    except:
        pass

    try:
        obj = conferencepaper.objects.get(label=label)
        return obj
    except:
        pass    
    
    try:
        obj = thes.objects.get(label=label)
        return obj
    except:
        pass
    
    try:
        obj = stand.objects.get(label=label)
        return obj
    except:
        pass

    try:
        obj = rprt.objects.get(label=label)
        return obj
    except:
        pass
    
    try:
        obj = book.objects.get(label=label)
        return obj
    except:
        pass
    
    return None


def publication_obj_html(childobj):
    #obj = publication.objects.get(label=label)
    #childobj = get_child_by_label(label)
    
    if childobj == None:
        return render_to_response('no_label_found.html',{
                                                    })          
    
    t1 = get_template('pub_generic_details.html')
    
    if isinstance(childobj, journalarticle):
        fields = ['id','label','TI','T2','doc','get_authors_html','get_keywords_html']
        
    elif isinstance(childobj, conferencepaper):
        fields = ['id','label','TI','conference','doc','get_authors_html','get_keywords_html']

    elif isinstance(childobj, thes):
        fields = ['id','label','PY','TI','PB','get_authors_html','get_keywords_html']
        
    elif isinstance(childobj, book):
        fields = ['id','label','PY','TI','PB','get_authors_html','get_keywords_html']

    elif isinstance(childobj, stand):
        fields = ['id','label','PY','TI','PB','get_authors_html','get_keywords_html']

    elif isinstance(childobj, rprt):
        fields = ['id','label','PY','TI','SN','get_authors_html','get_keywords_html']
        
        
    html = t1.render(Context({'obj':childobj,'fields':fields}))    
    
    return html


def publication_label_html(label):
    obj = get_child_by_label(label)
    if obj != None:
        html = publication_obj_html(obj)    
    else:
        html = ''
    return html

def publication_lb_index(request,label):
    obj = get_child_by_label(label)
    html = publication_obj_html(obj)   
    # get involved userlib
    libinvolve = UserRef.objects.filter(object_LB=label)

    return render_to_response('publication_details.html',{'pub':html,
                                                              'obj':obj,
                                                              'libinvolve':libinvolve,
                                            },context_instance=RequestContext(request))    

 
#=======creation

def publication_create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = journalarticleForm(data=request.POST)#,Person=request.user) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            new_template = form.save(request)
            notice_title = 'Journal Create success'
            return render_to_response('pub_generic_create_confirm.html', {
                                                              'create_success':True,
                                                              'notice_title':notice_title,
                                                               'name':'Journal Article'},
                                                             context_instance=RequestContext(request))

    else:
        #item = get_object_or_404(journalarticleForm, pk=1)
        form = journalarticleForm() # An unbound form

    return render_to_response('pub_generic_create_form.html', {'form_list':[form],
                                                               'form_display_mode_table':True,
                                                               'form_is_multipart':True},
             context_instance=RequestContext(request)) 
