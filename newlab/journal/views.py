# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect
from django.template import RequestContext
from models import journal,journalarticle

#from forms import MeetingForm, TasksForm, TransactionForm, TransactionDocForm, TransactionReportForm, Transaction_Monthly_Form
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from settings import ROOT_URL


from contributor.models import authors   # import author
from publications.models import keywords


from django.db.models import Q
import pickle as pickle
from django.contrib.contenttypes.models import ContentType

def journal_list(request):

    p = journal.objects.all() #filter(Person=request.user)
    fields = ['name','impact','publisher'] #,'Quantity','TotalReceiptPrice','TotalCost']
    return render_to_response('journal_list.html',{'item_list':p,'fields':fields,'detail_view':'purchase_details'},context_instance=RequestContext(request))

def journal_detail(request,id):
    p = journal.objects.get(pk=id) #filter(Person=request.user)
    
    
    


