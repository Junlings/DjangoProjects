from models import recruitercompanys, Recruiter
from django.contrib import admin


class RecruiterInline(admin.TabularInline):
    model = Recruiter
    extra = 0
    
class CompanysAdmin(admin.ModelAdmin):
    list_display = ('id','abbrname','type')
    list_filter = ['type',]
    search_fields = ['abbrname',]
    inlines  = [RecruiterInline,]

admin.site.register(recruitercompanys,CompanysAdmin)