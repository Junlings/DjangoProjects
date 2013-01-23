from django import forms
from django.utils.translation import ugettext_lazy as _

from models import accounts, transactions
from models import MONTH_CHOICES, YEAR_CHOICES
class AccountForm(forms.ModelForm):
    class Meta:
        model = accounts
        exclude = ('owner',)
        #widgets = {
        #            'owner': forms.HiddenInput()
        #        }

    
    def __unicode__(self):
        return _(u"Account Create Form") % {}


class JQueryUIDatepickerWidget(forms.DateInput):
    def __init__(self, **kwargs):
        super(forms.DateInput, self).__init__(attrs={"size":10, "class": "dateinput"}, **kwargs)

    class Media:
        css = {"all":("http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/themes/redmond/jquery-ui.css",)}
        js = ("http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js",
              "http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.6/jquery-ui.min.js",)


TRANSACTION_CHOICES = (
    ('purchase','purchase'),
    ('sell','sell'),
    ('operation','operation'),
)

class TransactionFilterForm(forms.Form):
    
    account = forms.ModelChoiceField(queryset=accounts.objects.all(), empty_label=None)
    type = forms.MultipleChoiceField(choices=TRANSACTION_CHOICES, widget=forms.CheckboxSelectMultiple)
    datestart = forms.DateField(label="Start Date", widget=JQueryUIDatepickerWidget)
    dateend  = forms.DateField(label="End Date", widget=JQueryUIDatepickerWidget) 
    
        
    def __unicode__(self):
        return _(u"Transaction Select Form") % {}
        
        
class AccountSummaryForm(forms.Form):
    account = forms.ModelChoiceField(queryset=accounts.objects.all(), empty_label=None)
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    
    CHOICES = MONTH_CHOICES # (('Year Upto Date','Year Upto Date'),) + MONTH_CHOICES
    
    month = forms.ChoiceField(choices=CHOICES)
    
    def __unicode__(self):
        return _(u"Account Select Form") % {}    