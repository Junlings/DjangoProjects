from django.contrib import admin

from models import conference, conferencepaper,conferenceproceeding# cpapercontent, cpaperdatabases, cpaperindex, cpapernotes, cpaperonline, cpaperplacement, , Authorship
from django.db.models import AutoField

from django.contrib.contenttypes.generic import GenericTabularInline


from publications.admin import authorshipInline
    
class cpaperarticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('KWS',)
    list_display = ('id','label','TI')
    inlines  = [authorshipInline]##,keywordsInline]
    #raw_id_fields = ("conference",'proceeding')
    #actions = ['parse_RIS','export_bib',]
    #list_filter = ('get_title',)  #  how can i make this work??
    search_fields = ['TI','LB']

    fieldsets = (
        (None, {
            'fields': ('label', 'TI','AB','KWS')
        }),
        ('Placement', {
            'fields': ('conference','proceeding','SP'),   
        }),
        
        ('File', {
            'fields': (('doc', 'doclink')),
        }),
    )
 

class conferenceAdmin(admin.ModelAdmin):
    list_display = ('id','PY', 'DA', 'PB','C1','LA')

class conferenceproceedingAdmin(admin.ModelAdmin):
    list_display = ('id','C3','conference','get_fulltext',) #,'PY', 'DA', 'PB','C1','LA')


 
admin.site.register(conferencepaper,cpaperarticleAdmin)
admin.site.register(conference)#,conferenceAdmin)
admin.site.register(conferenceproceeding)#,conferenceproceedingAdmin)
#admin.site.register(cpapercontent)