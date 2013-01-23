from django import forms
from django.utils.translation import ugettext_lazy as _

from models import ItemProduct, Manufacturer

class ItemProductForm(forms.ModelForm):
    class Meta:
        model = ItemProduct
    
    def __unicode__(self):
        return _(u"ItemProduct Create Form") % {}
        
        
class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
    
    def __unicode__(self):
        return _(u"Manufacturer Create Form") % {}
        