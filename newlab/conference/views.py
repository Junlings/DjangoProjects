# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect
from django.template import RequestContext
from models import journalarticle, journalcontent, journalindex, journalnotes, journalonline, journalplacement, journal, Authorship

#from forms import MeetingForm, TasksForm, TransactionForm, TransactionDocForm, TransactionReportForm, Transaction_Monthly_Form
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from settings import ROOT_URL
from documents.models import fulltext

from contributor.models import authors   # import author
from keywords.models import keywords
from models import journal

from django.db.models import Q
import pickle as pickle
from django.contrib.contenttypes.models import ContentType
from lreviews.models import singlereviews

def journal_list(request):

    p = journal.objects.all() #filter(Person=request.user)
    fields = ['name','impact','publisher'] #,'Quantity','TotalReceiptPrice','TotalCost']
    return render_to_response('journal_list.html',{'item_list':p,'fields':fields,'detail_view':'purchase_details'},context_instance=RequestContext(request))

def journal_index(request):

    alljournal = journal.objects.all() #filter(Person=request.user)
    alljournalpaper = journalarticle.objects.all() #filter(Person=request.user)
    
    
    alljournalpaperfulltext = fulltext.objects.filter(content_type=ContentType.objects.get(app_label="journal", model="journalarticle")) #filter(Person=request.user)
    
    
    
    
    fields = ['name','impact','publisher'] #,'Quantity','TotalReceiptPrice','TotalCost']
    return render_to_response('journal_index.html',{'alljournal':alljournal,
                                                    'alljournalpaper':alljournalpaper,
                                                    'alljournalpaperfulltext':alljournalpaperfulltext,
                                                    
                                                    },context_instance=RequestContext(request))

def paper_by_label(request,label):
    p1 = journalarticle.objects.get(LB=label) #filter(Person=request.user)
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
        jfulltext = fulltext.objects.get(content_type=ContentType.objects.get(app_label="journal", model="journalarticle"),object_id=p1.id) #filter(Person=request.user)
    except:
        jfulltext = None
        
    reviews = singlereviews.objects.filter(object_LB=p1.LB)
    return render_to_response('paper_details.html',{'paper':p1,
                                                    'authors':authors,
                                                    'content':content,
                                                    'placement':placement,
                                                    'KWs':KWs,
                                                    'reviews':reviews,
                                                    'fulltext':jfulltext,
                                                    },context_instance=RequestContext(request))    

'''
def find_or_create_author(inputstring):
    if ',' in inputstring:
        name = inputstring.split(',')
        lastname = name[0]
        firstname = name[1]
    
    else:
        name = inputstring.split(' ')
        lastname = name[-1]
        firstname = ' '.join(name[:-1])
    
    try:
        spauthor = authors.objects.get(firstname=firstname.strip(),lastname=lastname.strip())
    except:
        spauthor = authors()
        spauthor.firstname = firstname.strip()
        spauthor.lastname = lastname.strip()
        spauthor.middlename = ''
        spauthor.save()
        

    return spauthor


def find_or_create_keywords(inputstring):

    try:  
        kword = keywords.objects.get(KW=inputstring)
    except:
        kword = keywords()
        kword.KW = inputstring.lower()
        kword.save()
    return kword

def find_or_create_journal(inputstring):
    try:
        jour = journal.objects.get(name=inputstring)
    except:
        jour = journal()
        jour.name = inputstring
        jour.save()
    return jour

def create_jour_content(jour,inputdict):
    
    j1 = journalcontent()
    j1.paper = jour
    if 'TI' in inputdict.keys():
        j1.TI = inputdict['TI'][0]    

    if 'ST' in inputdict.keys():
        j1.ST = inputdict['ST'][0]    

    if 'AB' in inputdict.keys():
        j1.AB = inputdict['AB'][0]    
    j1.save()
    if 'KW' in inputdict.keys():
        for kword in inputdict['KW']:
            j1.KW.add(find_or_create_keywords(kword))    
    
    j1.save()
    return j1
    

def create_jour_placement(jour,inputdict):
    j1 = journalplacement()
    j1.paper = jour    
    if 'PY' in inputdict.keys():
        j1.PY = inputdict['PY'][0]
    if 'VL' in inputdict.keys():
        j1.VL = inputdict['VL'][0]
    if 'IS' in inputdict.keys():
        j1.IS = inputdict['IS'][0]
    if 'SP' in inputdict.keys():
        j1.SP = inputdict['SP'][0]
    if 'M2' in inputdict.keys():
        j1.M2 = inputdict['M2'][0]
        
    j1.save()
    
    print 'save placement'
    return j1     
     
         

def create_journalarticle(inputdict):
    try:
        if 'TY' in inputdict.keys():
            if inputdict['TY'][0] == 'JOUR':
                try:
                    j1 = journalarticle.objects.get(LB=inputdict['LB'][0])
                    
                    try:
                        j1place = journalplacement.objects.get(paper=j1)
                        j1place.delete()
                        try:
                            create_jour_placement(j1,inputdict)
                        except:
                            pass
                    except:
                        try:
                            create_jour_placement(j1,inputdict)
                        except:
                            pass
                except:
                    j1 = journalarticle()
                
                    # create journal
                    if 'T2' in inputdict.keys():
                        j1.T2 = find_or_create_journal(inputdict['T2'][0])
                    else:
                        j1.T2 = find_or_create_journal('unknown')
                    # create type
                    if 'M2' in inputdict.keys():
                        j1.M2 = inputdict['M2'][0]
                    
                    # create label
                    if 'LB' in inputdict.keys():
                        j1.LB = inputdict['LB'][0]
                        
                    j1.save()
            
                    # create author list
                    seq = 1
                    for author in inputdict['AU']:
                        spauthor = find_or_create_author(author)
                        a1 = Authorship(author=spauthor,sequence=seq,article=j1)
                        a1.author = spauthor
                        a1.sequence = seq
                        a1.save()
                        seq += 1
        
                    j1.save()
                    
                    # create content
                    create_jour_content(j1,inputdict)
                    
                    # create placement
                    try:
                        create_jour_placement(j1,inputdict)
                    except:
                        pass
                    return j1
    except:
        pass
    """
    try:
        if 'TY' in inputdict.keys():
            if inputdict['TY'][0] == 'JOUR':
                j1 = journalarticle()
                
                # create journal
                if 'T2' in inputdict.keys():
                    j1.T2 = find_or_create_journal(inputdict['T2'][0])
                else:
                    j1.T2 = find_or_create_journal('unknown')
                # create type
                if 'M2' in inputdict.keys():
                    j1.M2 = inputdict['M2'][0]
                
                # create label
                if 'LB' in inputdict.keys():
                    j1.LB = inputdict['LB'][0]
                    
                j1.save()
        
                # create author list
                seq = 1
                for author in inputdict['AU']:
                    spauthor = find_or_create_author(author)
                    a1 = Authorship(author=spauthor,sequence=seq,article=j1)
                    a1.author = spauthor
                    a1.sequence = seq
                    a1.save()
                    seq += 1
    
                j1.save()
                
                # create content
                create_jour_content(j1,inputdict)
                
                # create placement
                create_jour_placement(j1,inputdict)
                
                return j1
    except:
        pass
    """ 
def trial():
    f1 = open('UHPC_RIS.pydat','r')
    res = pickle.load(f1)
    for file in res:
        create_journalarticle(file)
'''    

    