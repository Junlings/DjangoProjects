import cPickle as pickle
from companies.models import companys, company_rank
from djangoextension.contacts.models import address
import sys
import os
os.path.abspath(os.path.dirname(__file__))

def import_company():
    f1 = open('companies/fixture/company.pydat','rb')
    
    company_list = pickle.load(f1)
    
    for company in company_list:
        # add address ins
        address_ins = address(**{'nickname':company['shortname'],
                                 'country':'US',
                                 'state':company['state'],
                                 'city':company['city'],
                                 'address_line1':'N/A',
                                 'zipcode':'00000',
                                 'notes': 'automatic generate with company',
                                 })
        address_ins.save()
        
        

        # add instance
        instance = companys(**{'abbrname':company['shortname'],'type':company['type'],'address':address_ins})
        instance.save()
        
        # add rank ins
        if company['rank_2011'] != None:
            r1 = company_rank(**{'company':instance,
                                 'rank_agency':'ENR',
                                 'rank_year':'2011',
                                 'rank':company['rank_2011']})
            r1.save()
    
        if company['rank_2012'] != None:
            r1 = company_rank(**{'company':instance,
                                 'rank_agency':'ENR',
                                 'rank_year':'2012',
                                 'rank':company['rank_2012']})
            r1.save()