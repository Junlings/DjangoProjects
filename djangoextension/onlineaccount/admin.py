from django.contrib import admin

from models import onlineaccounts

class OnlineAccountAdmin(admin.ModelAdmin):
    
    list_display =('id','supplier','owner','username','password','financialaccount')



admin.site.register(onlineaccounts,OnlineAccountAdmin)


