from django.contrib import admin

from models import inventory_results
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id','__unicode__','item','last_commit','search_interval')

       
admin.site.register(inventory_results,InventoryAdmin)
