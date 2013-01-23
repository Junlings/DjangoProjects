from models import customers
from django.contrib import admin

class CustomersAdmin(admin.ModelAdmin):
    list_display =('id','firstname','lastname')
    
    
admin.site.register(customers,CustomersAdmin)