from django.contrib import admin

from models import Local_Stores_Staples, Local_Stores_Bestbuy,  Local_Stores_Target, Local_Stores_Walmart

class StoreStaplesAdmin(admin.ModelAdmin):
    list_display = ('id','__unicode__','zipcode', 'phone','state','city','address')

class StoreBestbuyAdmin(admin.ModelAdmin):
    list_display = ('id','num','__unicode__','zipcode', 'phone','state','city','address')

class StoreTargetAdmin(admin.ModelAdmin):
    list_display = ('id','num','__unicode__','zipcode', 'phone','state','city','address')
    
class StoreWalmartAdmin(admin.ModelAdmin):
    list_display = ('id','num','__unicode__','zipcode', 'phone','state','city','address')



class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','owner', 'state','city','zipcode','last_commit','search_interval')

    
admin.site.register(Local_Stores_Staples,StoreStaplesAdmin)
admin.site.register(Local_Stores_Bestbuy,StoreBestbuyAdmin)
admin.site.register(Local_Stores_Target,StoreTargetAdmin)
admin.site.register(Local_Stores_Walmart,StoreWalmartAdmin)
#admin.site.register(inventory_results,InventoryAdmin)