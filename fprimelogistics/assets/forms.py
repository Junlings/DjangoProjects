from django import forms
from django.utils.translation import ugettext_lazy as _

from models import asset, assetgroup, assetstorage
from inventory.models import storage
from vending.models import PurchaseRequest
from sellings.models import Sellingplatform, SellRequest
class AssetForm(forms.ModelForm):
    class Meta:
        model = asset
    
    def __unicode__(self):
        return _(u"Asset Create Form") % {}
        
class AssetFilterForm(forms.Form):
    storage = forms.ModelChoiceField(queryset=storage.objects.all(), empty_label="--ANY--")
    purchase = forms.ModelChoiceField(queryset=PurchaseRequest.objects.all(), empty_label="--ANY--")
    sell_platform = forms.ModelChoiceField(queryset=Sellingplatform.objects.all(), empty_label="--ANY--")
    onsale = forms.NullBooleanField()
    sold = forms.NullBooleanField()
    #selling = forms.ModelChoiceField(queryset=SellRequest.objects.all(), empty_label="--ANY--")
    
    def __unicode__(self):
        return _(u"Asset Select Form") % {}