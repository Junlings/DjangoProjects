from models import UserProfile, UserRefLib, UserRef
from django.contrib import admin

class UserRefInline(admin.TabularInline):
    model = UserRef
    extra = 0

class UserRefLibAdmin(admin.ModelAdmin):
    inlines  = [UserRefInline,]

    
admin.site.register(UserProfile)
admin.site.register(UserRefLib,UserRefLibAdmin)#,ClientInline)
