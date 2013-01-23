from django.contrib import admin

from models import journal, journalarticle

from django.db.models import AutoField
from django.contrib.contenttypes.generic import GenericTabularInline

from publications.admin import authorshipInline


    
class journalarticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('KWS',)
    raw_id_fields = ("T2",)
    list_display = ('id','label','TI','T2','doc','PY','VL','IS','SP','get_authors','get_keywords')
    inlines  = [authorshipInline]##,keywordsInline]
    #actions = ['parse_RIS','export_bib',]
    #list_filter = ('get_title',)  #  how can i make this work??
    search_fields = ['TI','label']
    list_filter = ('T2', )

    fieldsets = (
        (None, {
            'fields': ('label', 'TI','AB','KWS')
        }),
        ('Placement', {
            'fields': ('T2', 'PY','VL','IS','SP'),   
        }),
        ('File', {
            'fields': (('doc', 'doclink')),
        }),
    )
    
    
    def parse_RIS(self,request,queryset):
        for query in queryset:
            parse_RIS(request,query)

    def export_bib(self,request,queryset):
        for query in queryset:
            export_bib(request,query)
            
class journalAdmin(admin.ModelAdmin):
    list_display = ('id','name','shortname','impact', 'publisher', 'peroidic','website','notes')
    search_fields = ['name',]

class journalcontentAdmin(admin.ModelAdmin):
    list_display = ('id','TI','paper','get_label','get_fulltext')
    
admin.site.register(journalarticle,journalarticleAdmin)
admin.site.register(journal,journalAdmin)
