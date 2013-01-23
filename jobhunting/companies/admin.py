from models import companys, company_rank
from django.contrib import admin


class RankInline(admin.TabularInline):
    model = company_rank
    extra = 0
    
class CompanysAdmin(admin.ModelAdmin):
    list_display = ('id','abbrname','type')
    list_filter = ['type',]
    search_fields = ['abbrname',]
    inlines  = [RankInline,]

admin.site.register(companys,CompanysAdmin)