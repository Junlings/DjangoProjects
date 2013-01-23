from django.contrib import admin

from models import authors, address, contacts, socialmedia, socialmedia_china, publisher
from action import Merge_author




class authorAdmin(admin.ModelAdmin):
    list_display = ('id','firstname','lastname')    
    actions = ['Merge_author',]
    search_fields = ['firstname','lastname']
    def Merge_author(self,request,queryset):
        Merge_author(request,queryset)
                
admin.site.register(authors,authorAdmin)
admin.site.register(publisher)