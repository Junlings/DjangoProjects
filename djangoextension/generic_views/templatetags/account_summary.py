import types

from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.template import Library, Node, Variable, VariableDoesNotExist

from django.template.defaultfilters import register
from django.forms.models import model_to_dict


@register.filter(name='YTD_sum')
def YTD_sum(account,para):
    sum = account.YTD_balance()
    return sum[para]

