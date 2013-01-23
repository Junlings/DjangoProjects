import pickle
from publications.models import Authorship, keywords, publication
from journal.models import journalarticle,journal
from contributor.models import authors

import datetime

def updatelib():
    
    b = pickle.load(open('UHPC_RIS.pydat','r'))
    for lib in b:
        
        try:
            if 'LB' in lib.keys():
                print lib['LB']
                pp = publication.objects.get(label=lib['LB'])
            
                print 'match id %s \n' % lib['LB']
            
        except:
            continue
        
        

def doit():
    a = pickle.load(open('dateeee.pydat','r'))
    
    for key in a.keys():
        
        print a[key]

        inoutdict = {
            'id':key,
            'label':a[key]['LB'],
            'TI':a[key]['get_title'],
            'AB':a[key]['get_AB'],
            
            'PY':a[key]['get_PY'],
            'VL':a[key]['get_VL'],
            'IS':a[key]['get_IS'],
            'SP':a[key]['get_SP'],
            'doc':a[key]['get_fulltext'],
            'created_on':datetime.datetime.now(),
    
        }
        if type(a[key]['T2']) == type(10L):
            inoutdict['T2'] = journal.objects.get(pk=a[key]['T2'])
      
        try:
            j1 = journalarticle(**inoutdict)
            j1.save()
        except:
            continue

        # create the authors
        if len(a[key]['get_author']) > 0:
            for au in a[key]['get_author']:
                author = authors.objects.get(pk=au[0])
                mpublication = publication.objects.get(pk=j1.id)
                sequence = au[1]
                aa = Authorship(author=author,publication=mpublication,sequence=sequence)
                aa.save()

        
        try:
            # create the keywords
            for kw in a[key]['get_KW']:
                j1.KWS.add(kw)
                j1.save()
        except:
            continue
        
    print 1