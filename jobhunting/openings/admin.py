from models import openings,requirement
from django.contrib import admin
from applications.models import ApplicationState


class ReqInline(admin.TabularInline):
    model = requirement
    extra = 0


class OpeningsAdmin(admin.ModelAdmin):
    list_display = ('id','company','title','date_add','location_city','location_state','get_status_count')
    fieldsets = (
           (None, {
               'fields': ('company', 'title', 'type', 'date_expire','location_state','location_city','description')
           }),          
           ('Other', {
               'classes': ('collapse',),
               'fields': ('source', 'active', 'notes')
           }),            
       )

    #filter_horizontal = ("accept_skillset","accept_certifications","pre_skillset","pre_certification" )
    inlines  = [ReqInline,]
    
    
    def get_status_count(self,obj):    
        objs = ApplicationState.objects.filter(opening=obj)
        num = len(list(objs))
        return num
 
admin.site.register(openings, OpeningsAdmin) #,OpeningsAdmin)