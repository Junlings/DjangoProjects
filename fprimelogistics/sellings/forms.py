from django import forms
from django.utils.translation import ugettext_lazy as _

from sellings.models import Sellingplatform, SellRequest
        
class SellFilterForm(forms.Form):
    sell = forms.ModelChoiceField(queryset=SellRequest.objects.all(), empty_label="--ANY--")

    def __unicode__(self):
        return _(u"Sell Select Form") % {}

MONTH_CHOICES = (
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
    ('12','12'),
)

YEAR_CHOICES = (
    ('2012','2012'),
)

class SellSelectForm(forms.Form):
    year = forms.ChoiceField(choices=YEAR_CHOICES)
    
    CHOICES = MONTH_CHOICES # (('Year Upto Date','Year Upto Date'),) + MONTH_CHOICES
    month = forms.ChoiceField(choices=CHOICES)
    
    def __unicode__(self):
        return _(u"Sell Monthly Select Form") % {}  

