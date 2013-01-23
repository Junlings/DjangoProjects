# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect
from django.template import RequestContext
from models import *

#from forms import MeetingForm, TasksForm, TransactionForm, TransactionDocForm, TransactionReportForm, Transaction_Monthly_Form
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from settings import ROOT_URL


from contributor.models import authors   # import author
from publications.models import keywords


from django.db.models import Q
import pickle as pickle
from django.contrib.contenttypes.models import ContentType
from journal.models import journalarticle
from publications.views import  publication_label_html

def author_details(request,id):
    
    try:
        authorins = authors.objects.get(pk=id)
        
    except:
        authorins = []
        
    journalpaps = journalarticle.objects.filter(AUs = authorins)    
    journalpapshtml = []
    
    for paper in journalpaps:
        journalpapshtml.append(publication_label_html(paper.label))
    
    
    
    return render_to_response('author_detail.html',{'author':authorins,
                                                    'journalpaps':journalpapshtml,
                                                    },context_instance=RequestContext(request))