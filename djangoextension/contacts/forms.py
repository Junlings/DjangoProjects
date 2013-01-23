from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from contacts.models import address

class AddressForm(ModelForm):
    class Meta:
        model = address
