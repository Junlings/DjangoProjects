from django.core.urlresolvers import reverse
from djangoextension.djangorestframework.resources import ModelResource
from models import test, address


class TestResource(ModelResource):
    """
    A test resource has field name of nickname
    """
    model = test
    fields = ('id','nickname')
    ordering = ('nickname',)
    
class AddressResource(ModelResource):
    """
    Address model
    """
    model = address
    fields = ('id','nickname','country','state','city','address_line1','address_line2','zipcode','notes')
    ordering = ('id',)    
    