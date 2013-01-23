from models import company_account, organization_account
from django.contrib import admin

 

class CompanyAccountAdmin(admin.ModelAdmin):
    list_display = ('id','company','user','website','loginname','loginpass')
 
admin.site.register(company_account,CompanyAccountAdmin)



class organizationAccountAdmin(admin.ModelAdmin):
    list_display = ('id','organization','user','website','loginname','loginpass','websitename','websitepass')
 
admin.site.register(organization_account,organizationAccountAdmin)