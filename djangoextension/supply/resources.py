from django.core.urlresolvers import reverse
from djangoextension.djangorestframework.resources import ModelResource
from models import ItemTemplate, Supplier
from forms import ItemTemplateForm, SupplierForm

class ItemTemplateResource(ModelResource):
    """
    A test resource has field name of nickname
    """
    model = ItemTemplate
    form =  ItemTemplateForm
    fields = ('id','get_product','get_manufacturer','get_suppliers','suppliers_PID','notes')

    ordering = ('id',)