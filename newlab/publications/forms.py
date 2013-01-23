from django import forms
from django.utils.translation import ugettext_lazy as _
from models import *
from journal.models import journalarticle, journal
import datetime
import os
from contributor.action import find_or_create_authorlist
from action import find_or_create_keywordlist

def handle_uploaded_publication(f,name):
    #now = datetime.datetime.now()
    
    filename = name + '.'+f.name.split('.')[-1]
    filepath = os.path.join('doc','fulltext')
    abspath = os.path.join(settings.MEDIA_ROOT,filepath)
    
    try:
       os.makedirs(abspath)
    except OSError:
       pass   
    
    dest = open(os.path.join(abspath,filename),'wb+') # write should overwrite the file
    for chunk in f.chunks():
        dest.write(chunk)
    dest.close()
    
    return os.path.join(filepath,filename)


class journalarticleForm(forms.ModelForm):
    keywordlist = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'size':'80'}))
    authorlist = forms.CharField(max_length=200, required=False,widget=forms.TextInput(attrs={'size':'80'}))
    tjournal = forms.ModelChoiceField(queryset=journal.objects.all(), empty_label=None,label='Journal Published')
    
    class Meta:
        model = journalarticle
        fields = ('label','TI','AB','PY','VL','IS','SP','doc', 'doclink')
    
    def __unicode__(self):
        return _(u"Journal Article Create Form") % {}
        
        

    def __init__(self, *args, **kwargs):
        super(journalarticleForm, self).__init__(*args, **kwargs)
        
        self.fields['TI'].widget = forms.TextInput(attrs={'size':'80'})
        self.fields['doclink'].widget = forms.TextInput(attrs={'size':'80'})
        self.fields.keyOrder = [
          'label',
          'TI',
          'tjournal',
          'authorlist',
          'AB',
          'keywordlist',
          'PY',
          'VL',
          'IS',
          'SP',
          'doc',
          'doclink',
          ]
        
    def save(self, request,commit=True):
        instance = super(journalarticleForm, self).save(commit=False)
        instance.save()
        
        # deal with journal
        if self.cleaned_data['tjournal']:
            #t2 = journal.objects.get(pk=self.cleaned_data['tjournal'])
            instance.T2 = self.cleaned_data['tjournal']
            instance.save()
            
        # deal with the upload file
        if 'doc' in request.FILES.keys():
            name = '_'+instance.label+'_'
            filename = handle_uploaded_publication(request.FILES['doc'],name)
    
            instance.doc = filename
            instance.save()
        
        # deal with author list
        if self.cleaned_data['authorlist'] != '':
            aulist = find_or_create_authorlist(self.cleaned_data['authorlist'],instance)
            
        # deal with keyword list
        if self.cleaned_data['keywordlist'] != '':
            kwlist = find_or_create_keywordlist(self.cleaned_data['keywordlist'])
            for kw in kwlist:
                instance.KWS.add(kw)
                instance.save()
        
        
        
        