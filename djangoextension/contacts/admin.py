from django.contrib import admin
from contacts.models import address, social, test

class AddressInline(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nickname',('country','state','city'),'address_line1','address_line2','zipcode')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('notes',)
        }),
    )
    list_display =('id','__unicode__','nickname','country','state','city')

class SocialInline(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nickname','homephone','cellphone','businessphone','fax')
        }),
        ('Internet', {
            'classes': ('collapse',),
            'fields': ('email','website')
        }),
        ('social Media', {
            'classes': ('collapse',),
            'fields': ('facebook','linkedin','twitter')
        }),
        ('special', {
            'classes': ('collapse',),
            'fields': ('sina_weibo','qq','mitbbs_id')
        }),
        ('note', {
            'classes': ('collapse',),
            'fields': ('notes',)
        }),
    )
    list_display =('id','__unicode__','nickname')
    
admin.site.register(address,AddressInline)#,AddressInline)
admin.site.register(social,SocialInline)#,SocialInline)
admin.site.register(test)#,SocialInline)
