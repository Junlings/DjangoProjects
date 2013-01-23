from models import organizations
from django.contrib import admin

class organizationsAdmin(admin.ModelAdmin):
    list_display = ('id','abbrname','type')
 
admin.site.register(organizations,organizationsAdmin)
