from django.core.urlresolvers import reverse
from djangoextension.djangorestframework.resources import ModelResource
from models import ItemProduct, Manufacturer
from forms import ItemProductForm, ManufacturerForm

class ItemProductResource(ModelResource):
    """
    A test resource has field name of nickname
    """
    model = ItemProduct
    form =  ItemProductForm
    fields = ('id','shortname','longname','get_manufacturer','modelid','mainimage','mainimagepath')

    ordering = ('id',)
