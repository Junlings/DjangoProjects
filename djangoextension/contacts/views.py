# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from contacts.models import test as testmodel

from django.template import RequestContext
from django.core import serializers
from contacts.forms import AddressForm

from contacts.admin import AddressInline
from contacts.models import address
import json

def root_view(request):
    return render_to_response('dojo_generic_create.html',{'form':AddressForm()},context_instance=RequestContext(request))

def list_view(request):
    fields = address._meta.fields
    grid = {'width':'65em','height':'65em','padding':'1px'}
    return render_to_response('dojo/rest_datagrid/dojo_generic_list.html',{'fields':fields,'gird':grid},context_instance=RequestContext(request))