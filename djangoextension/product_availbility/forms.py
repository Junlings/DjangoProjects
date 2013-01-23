from django import forms
from registration.forms import RegistrationForm
from django.utils.translation import ugettext_lazy as _
from models import inventory_results
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.localflavor.us.forms import USStateSelect,USStateField




class CheckForm(forms.Form):
    zipcode = forms.CharField(max_length=5)
    miles = forms.CharField(max_length=4)
 
class ItemForm(forms.Form):
    #staples_supply = Supplier.objects.get(name='Staples')
    
    item = forms.ModelMultipleChoiceField(queryset=inventory_results.objects.all())
    #state = USStateField(widget=USStateSelect)


    def __unicode__(self):
        return _(u"Item Template select Form") % {}    
    
        
