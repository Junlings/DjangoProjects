from models import ApplicationState, States
from django.contrib import admin


class StatesInline(admin.TabularInline):
    model = States
    extra = 0
          

class ApplicationStateAdmin(admin.ModelAdmin):
    list_display = ('id','opening','coverletter','resume','application_status',)
    inlines  = [StatesInline,]
    
    def application_status(self, obj):
        #print obj.status_set()
        return '<br/>'.join(c.__unicode__() for c in obj.status_set())    
    application_status.allow_tags = True


  
admin.site.register(ApplicationState,ApplicationStateAdmin)
#admin.site.register(States)
'''
class CompanysAdmin(admin.ModelAdmin):
    list_display = ('id','abbrname','type')
 

class CompanyAccountAdmin(admin.ModelAdmin):
    list_display = ('id','company','user','website','loginname','loginpass')
 
admin.site.register(companys,CompanysAdmin)
admin.site.register(company_account,CompanyAccountAdmin)

'''