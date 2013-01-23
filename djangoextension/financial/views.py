# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core import serializers
from models import accounts, transactions, AccountMonthlySummary
from forms import AccountForm, TransactionFilterForm, AccountSummaryForm
import json
from resources import TransactionsResource, AccountsResource
from djangoextension.generic_views.views import dojo_list_view
import datetime
from djangoextension.djangorestframework.serializer import Serializer
from uti.encoder import JSONEncoder
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

def account_create_view(request):
    return render_to_response('dojo/dojo_generic_create.html',{'form':AccountForm()},context_instance=RequestContext(request))



def account_list_view(request):
    fields = AccountsResource.fields
    fields_set = {
                    }
    return dojo_list_view(request,fields,fields_set)
    
    
def transaction_list_view(request):
    #fields = transactions._meta.fields
    fields = TransactionsResource.fields
    fields_set = {'id':{'name':'id','width':'5%'},
                  'get_credit_account':{'name':'Credit Account','width':'10%'},
                  'get_debit_account':{'name':'Debit Account','width':'10%'},
                  'get_request_info':{'name':'Request','width':'25%'},
                  'get_response_info':{'name':'Response','width':'25%'}
                    }

    return dojo_list_view(request,fields,fields_set)
    
    

def Transaction_list_view2(request):
    myaccounts = accounts.objects.filter(owner=request.user)
    #data = {}
    #data['type'] = ['purchase','sell','operation']
    myform = TransactionFilterForm(initial={'type':['purchase','sell','operation']})
    myform.fields['account'].queryset = accounts.objects.filter(owner=request.user)
    
    
    return render_to_response('transaction_select.html', {'forms':myform,
                                                    },
                                                             context_instance=RequestContext(request))    

def financial_index(request):
    myaccounts = accounts.objects.filter(owner=request.user)
    return render_to_response('financial_index.html', {'accounts':myaccounts
                                                    },
                                                             context_instance=RequestContext(request))

def Transaction_list_comission(request):
    myaccounts = accounts.objects.filter(owner=request.user)
    comission = {}
    purchasecosttype = ContentType.objects.get(model='Purchase_cost',app_label='vending')
    for accountobj in myaccounts:
        objs = transactions.objects.filter((Q(accountA=accountobj) | Q(accountB=accountobj)) & Q(fieldname='commission') & Q(content_type=purchasecosttype))
        comission[accountobj.__unicode__()] = {'amount':transactions.objects.summary_general(objs,accountobj),
                                               'transactions':[]}        
        for obj in objs:
            comission[accountobj.__unicode__()]['transactions'].append({'transaction':obj,'purchase':obj.related_purchase()})

        
    
    return render_to_response('transaction_comission.html', {'comission':comission,
                                                    },
                                                             context_instance=RequestContext(request))

def Transaction_list_transfer(request):
    myaccounts = accounts.objects.filter(owner=request.user)
    comission = {}
    #purchasecosttype = ContentType.objects.get(fieldname='internal_transfer')
    for accountobj in myaccounts:
        objs = transactions.objects.filter((Q(accountA=accountobj) | Q(accountB=accountobj)) & Q(fieldname='internal_transfer')).order_by('lastmodified')
        comission[accountobj.__unicode__()] = {'amount':transactions.objects.summary_general(objs,accountobj),
                                               'transactions':[]}        
        for obj in objs:
            comission[accountobj.__unicode__()]['transactions'].append({'transaction':obj})

        
    
    return render_to_response('transaction_transfer.html', {'comission':comission,
                                                    },
                                                             context_instance=RequestContext(request))
    


def generate_transaction(obj_list,accountobj):
    outputdict = []
    
    for record in obj_list:
        temp = {'amountplus':0.0,'amountminus':0.0}
        if record.accountA == accountobj:
            if record.modeA == 'credit':
                temp['amountplus'] = record.amount
            else:
                temp['amountminus'] = record.amount
        elif record.accountB == accountobj:
            if record.modeB == 'credit':
                temp['amountplus'] = record.amount
            else:
                temp['amountminus'] = record.amount
        
        temp['notes'] = record.notes
        if record.content_type != None:
            objmodel = record.content_type.model_class()
            objinst = objmodel.objects.get(pk=record.object_id)
            temp['notes'] += objinst.__unicode__() + '  |  ' + record.fieldname
        
        temp['id'] = record.id
        temp['ddate'] = record.lastmodified.date()
        outputdict.append(temp)    
    return outputdict

def Transaction_list_view_search(request):
    if request.is_ajax():
        cus_filter = {}
        
        if request.GET['operationon'] != 'false':
            obj_list = transactions.objects.exclude(content_type=None)

        
        # add account filter
        if request.GET['account'] != '':
            accountobj = accounts.objects.get(pk=request.GET['account'])
            obj_list = transactions.objects.filter(Q(accountA=accountobj) | Q(accountB=accountobj))
        

        if request.GET['datestart'] != '':
            datestart = datetime.datetime.strptime(request.GET['datestart'],"%m/%d/%Y")
        else:
            datestart = datetime.datetime.strptime('01/01/1990',"%m/%d/%Y")


        if request.GET['dateend'] != '':
            dateend = datetime.datetime.strptime(request.GET['dateend'],"%m/%d/%Y")
        else:
            dateend = datetime.datetime.strptime('01/01/9999',"%m/%d/%Y")
            
        cus_filter['lastmodified__range'] = [datestart,dateend]
        
        obj_list = obj_list.filter(**cus_filter) #onsale=True,item__itemproduct__shortname=u'Xbox 360 Wireless')
        json_ser = Serializer()
        

        outputdict = generate_transaction(obj_list,accountobj)

            
        availdata = json_ser.serialize(outputdict) #obj_list)
        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')  
        
    else:    
        cus_filter = {}
        obj_list = transactions.objects.all()
        
        # add account filter

        
        # add startdate filter

        datestart = datetime.datetime.strptime('03/01/2012',"%m/%d/%Y")

        dateend = datetime.datetime.strptime('06/01/2012',"%m/%d/%Y")
            
        cus_filter['lastmodified__range'] = [datestart,dateend]
        
        obj_list = obj_list.filter(**cus_filter) #onsale=True,item__itemproduct__shortname=u'Xbox 360 Wireless')
        json_ser = Serializer()
        availdata = json_ser.serialize(obj_list)
        
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')
        
def Account_list_view(request):
    myaccounts = accounts.objects.filter(owner=request.user)
    data = {'account':'',
            'year':datetime.datetime.now().year,
            'month':datetime.datetime.now().month-1}
    #raise error
    myform = AccountSummaryForm(data)
    myform.fields['account'].queryset = accounts.objects.filter(owner=request.user)
    return render_to_response('account_select.html', {'forms':myform,'accounts':myaccounts,
                                                    },
                                                             context_instance=RequestContext(request))       
    
    
def Account_list_view_search(request):
    if request.is_ajax():
        cus_filter = {}
        obj_list = AccountMonthlySummary.objects.all()
        
        # add account filter
        if request.GET['account'] != '':
            accountobj = accounts.objects.get(pk=request.GET['account'])
            cus_filter['account'] = accountobj
        # add startdate filter
        if request.GET['year'] != '':
            cus_filter['year'] = request.GET['year']

        if request.GET['month'] != '':
            if request.GET['month'] != 'Year Upto Date':
                cus_filter['month'] = request.GET['month']

            
        obj_list = obj_list.filter(**cus_filter) #onsale=True,item__itemproduct__shortname=u'Xbox 360 Wireless')
        json_ser = Serializer()
  
        outputdict = {}
            

        outputdict['account'] = obj_list[0].account.__unicode__()
        outputdict['year'] = obj_list[0].year
        outputdict['month'] = obj_list[0].month
        outputdict['total_debit'] = obj_list[0].total_debit
        outputdict['total_credit'] = obj_list[0].total_credit
        outputdict['total_transactions'] = obj_list[0].number_of_transaction()
        
        outputdict['total_all'] = obj_list[0].total_credit-obj_list[0].total_debit
        outputdict['transactions'] = generate_transaction(obj_list[0].transaction.all(),obj_list[0].account)

           
            
        availdata = json_ser.serialize(outputdict) #obj_list)
        avail_json_data = JSONEncoder().encode(availdata)
        return HttpResponse(avail_json_data, mimetype='application/json')             
                
    else:

        cus_filter = {}
        obj_list = AccountMonthlySummary.objects.all()
        
        # add account filter

        accountobj = accounts.objects.get(pk=2)
        cus_filter['account'] = accountobj
        # add startdate filter

        cus_filter['year'] = '2012'


        cus_filter['month'] = '5'
            
        
        
        obj_list = obj_list.filter(**cus_filter) #onsale=True,item__itemproduct__shortname=u'Xbox 360 Wireless')
        json_ser = Serializer()
        
        outputdict = {}
        outputdict['account'] = obj_list[0].account.__unicode__()
        outputdict['year'] = obj_list[0].year
        outputdict['month'] = obj_list[0].month
        outputdict['total_debit'] = obj_list[0].total_debit
        outputdict['total_credit'] = obj_list[0].total_credit
        outputdict['total_transactions'] = obj_list[0].number_of_transaction()
        
        outputdict['total_all'] = obj_list[0].total_credit-obj_list[0].total_debit
        outputdict['transactions'] = generate_transaction(obj_list[0].transaction.all(),obj_list[0].account)
        availdata = json_ser.serialize(outputdict) #obj_list)
        
        avail_json_data = JSONEncoder().encode(outputdict)
        return HttpResponse(avail_json_data, mimetype='application/json')