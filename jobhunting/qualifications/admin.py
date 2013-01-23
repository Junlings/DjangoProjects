from models import skills, certifications
from django.contrib import admin


admin.site.register(skills)
admin.site.register(certifications)

'''
class CompanysAdmin(admin.ModelAdmin):
    list_display = ('id','abbrname','type')
 

class CompanyAccountAdmin(admin.ModelAdmin):
    list_display = ('id','company','user','website','loginname','loginpass')
 
admin.site.register(companys,CompanysAdmin)
admin.site.register(company_account,CompanyAccountAdmin)
'''