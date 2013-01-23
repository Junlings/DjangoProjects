from django.contrib import admin
from models import Messages, PurchaseRequest, SellRequest


class MessageAdmin(admin.ModelAdmin):
    list_display =('id','title','author','updated','link')
    
admin.site.register(Messages,MessageAdmin) #,AddressInline)#,AddressInline)
admin.site.register(PurchaseRequest)
admin.site.register(SellRequest)