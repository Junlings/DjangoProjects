# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse

from django.template import RequestContext
from django.core import serializers
from models import ItemProduct, Manufacturer
from forms import ItemProductForm, ManufacturerForm
import json
from resources import ItemProductResource
from generic_views.views import dojo_list_view, single_file_upload
from uti.cvs_io import read_css


def Product_create_view(request):
    return render_to_response('dojo/dojo_generic_create.html',{'form':ItemProductForm(),'base_template':'supply_base.html'},context_instance=RequestContext(request))

def Manufacturer_create_view(request):
    return render_to_response('dojo/dojo_generic_create.html',{'form':ManufacturerForm(),'base_template':'supply_base.html'},context_instance=RequestContext(request))
    
def process_uploaded_file(filename):

    read_css(filename,ItemProduct)
    return {'create_success':True,'notice_title':'File upload complete'+filename,
            'notice_list':[{'identification_name':"pp",'identification_id':"9"}]}

def Product_create_batch_view(request):
    return single_file_upload(request,process_uploaded_file)
   
    
def Product_list_view(request):
    #fields = transactions._meta.fields
    fields = ItemProductResource.fields
    fields_set = {
                    }

    return dojo_list_view(request,fields,fields_set)