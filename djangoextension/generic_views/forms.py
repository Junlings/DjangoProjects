
from django import forms
from django.utils.translation import ugettext_lazy as _

class single_file_upload_form(forms.Form):
    file  = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        super(single_file_upload_form, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return _(u"Batch Product Create Form") % {}