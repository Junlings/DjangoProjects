from django import forms
from django.utils.translation import ugettext_lazy as _

from models import ItemTemplate, Supplier

class ItemTemplateForm(forms.ModelForm):
    class Meta:
        model = ItemTemplate
    
    def __unicode__(self):
        return _(u"ItemTemplate Create Form") % {}
        
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
    
    def __unicode__(self):
        return _(u"Supplier Create Form") % {}
        