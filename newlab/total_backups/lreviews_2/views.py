# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.template import RequestContext

#from forms import MeetingForm, TasksForm, TransactionForm, TransactionDocForm, TransactionReportForm, Transaction_Monthly_Form
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from settings import ROOT_URL
#from documents.models import fulltext

#from contributor.models import authors   # import author
#from keywords.models import keywords
from models import reviewproj, singlereviews,reviewquestion

from django.db.models import Q
import pickle as pickle
from django.contrib.contenttypes.models import ContentType
from publications.views import  publication_get_html

import json

def project_index(request):
    
    libs = reviewproj.objects.filter(Q(managers=request.user) | Q(contributors=request.user))

    projects = {}
    for lib in libs:
        projects[lib.id] = {'lib':lib}
        if request.user in lib.managers.all():
            projects[lib.id]['owner'] = True
        else:
            projects[lib.id]['owner'] = False
        if request.user in lib.contributors.all():
            projects[lib.id]['Contributor'] = True
        else:
            projects[lib.id]['Contributor'] = False
                
    
    return render_to_response('project_index.html',{'projects':projects,
                                                    },context_instance=RequestContext(request))

def project_details(request,id):
    
    project = reviewproj.objects.get(id=id) #filter(Person=request.user)
    questions = reviewquestion.objects.filter(project=project)
    reviews = singlereviews.objects.filter(question__project=project)
    references = {}#references = project.get_allreferences()
    reflib = project.associateLab
    matrix = project.get_allref_userlib_progress(request)
    return render_to_response('project_details.html',{'project':project,
                                                      'reflib':reflib,
                                                      'matrix':matrix,
                                                      'reviews':reviews,
                                                      'references':references,
                                                      'questions':questions,
                                                    },context_instance=RequestContext(request))    


def project_lb_details(request,id,label):
    project = reviewproj.objects.get(id=id) #filter(Person=request.user)
    questions = reviewquestion.objects.filter(project=project)
    items = {}
    
    for question in questions:
        items[question.order] = {}
        items[question.order]['question'] = question
        items[question.order]['choices'] = question.get_choices_html(label=label,question=question,user=request.user)
        items[question.order]['ajax'] = question.get_choices_ajax()
        items[question.order]['answer'] = question.get_answer(label,request.user)
    
    
    
    res = publication_get_html(request,label)
    if len(res) > 0:
        phtml,ptype = res
    
        return render_to_response('project_lb_details.html',{
                                                      'label':phtml,
                                                      'ptype':ptype,
                                                      'label2':label,
                                                      'project':project,
                                                      'items':items,
                                                    },context_instance=RequestContext(request))        
    else:
        return render_to_response('no_label_found.html',{
                                                      'label2':label,
                                                    },context_instance=RequestContext(request))          
        
def project_submit(request):
    if request.is_ajax():
        #print 'This is ajax request'
        #print request.POST
        data = request.POST #json.loads(request.POST)#request.POST
        print data
        project = reviewproj.objects.get(pk=int(data['project']))
        
        
        answers = json.loads(data['answers'])
        
        for key,answer in answers.items():

                
            try:
                # update the reviews
                a1 = singlereviews.objects.get(object_type=data['ptype'],
                               object_LB=data['label'],
                               reviewer=request.user,
                               question=project.get_question_order(key))
                a1.reviews = answer
                a1.save()
            
            except:
                # create the reviews
                a1 = singlereviews(object_type=data['ptype'],
                                   object_LB=data['label'],
                                   reviewer=request.user,
                                   question=project.get_question_order(key),
                                   reviews=answer)
            
                a1.save()
        return HttpResponse('test', mimetype="text/plain",status='200')
        
    else:
        return HttpResponse(status='400')