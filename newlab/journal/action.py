# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect
from django.template import RequestContext
from models import journalarticle, journalcontent, journalindex, journalnotes, journalonline, journalplacement, journal, Authorship

#from forms import MeetingForm, TasksForm, TransactionForm, TransactionDocForm, TransactionReportForm, Transaction_Monthly_Form
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from settings import ROOT_URL


from contributor.models import authors   # import author
from keywords.models import keywords

import pickle as pickle
from django.utils.encoding import smart_unicode

import StringIO



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
    return j1     
     
         

def create_journalarticle(inputdict):
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

def modify_journalarticle(j1,inputdict):
    try:
        if 'TY' in inputdict.keys():
            if inputdict['TY'][0] == 'JOUR':
                #j1 = journalarticle()
                
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


def parse_ris(res):
    res_dict = {}
    lines = res.split('\n')
    print lines
    for line in lines:
        if line.strip() == u'':
           continue

        print line
        print smart_unicode('-') in line
        if smart_unicode('-') in line:
            print '- in', line
            aa = line.split('-')
            key = aa[0].strip()
           
            content = '-'.join(aa[1:]).strip()
            
            if key in res_dict.keys():
                res_dict[key].append(content)
            else:
                res_dict[key] = [content]
        
        else:
            pass

            #content = line.strip()
            #res_dict[key].append(content)
    return res_dict

        
def parse_RIS(request,query):
    res_dict = parse_ris(query.RIS)
    if len(res_dict.keys()) > 0 :
        modify_journalarticle(query,res_dict)
    return None
    
    
def export_bib(request,query):
    ''' generate bib for single journal article record '''
    tlabel = ('%s,\n' % query.LB)
    
    tJournal = '  Journal = {%s},\n' % query.T2.name
    
    tAuthor = []
    for author in query.AUs.all():
        tAuthor.append(','.join([author.lastname,author.firstname]))
    tAuthor = 'and'.join(tAuthor)
    tAuthor = '  Author = {%s},\n' % tAuthor
    
    tcontent = query.get_content()
    if tcontent:
        tTitle = '  Title = {%s},\n' % tcontent.TI
        tAbstract = '  Abstract = {%s},\n' % tcontent.AB
    
        
        tKeywords = []
        for keyword in tcontent.KW.all():
            tKeywords.append(keyword.KW)
        tKeywords = ','.join(tKeywords)
        tKeywords = '  Keyword = %s,\n' % tKeywords
    else:
        print 'no content found. export ceased'
        return ''
    
    tplacement = query.get_placement()
    if tplacement:
        tVolume = '  Volume = {%s},\n' % tplacement.VL
        tNumber = '  Number = {%s},\n' % tplacement.IS
        tPages = '  Pages = {%s},\n' % (tplacement.SP)
        tYear = '  Year = {%s}}\n' % tplacement.PY 
    else:
        print 'no placement found. export ceased'
        return ''    
    
    output = StringIO.StringIO()  
    output.write('@article{\n')
    output.write(tlabel)
    output.write(tAuthor)
    output.write(tTitle)
    output.write(tJournal)
    output.write(tVolume)
    output.write(tNumber)
    output.write(tPages)
    output.write(tAbstract)
    output.write(tKeywords)
    output.write(tYear)
    
    return output  # output single bib format for use 
    
    
    