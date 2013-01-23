from django.contrib import admin

from models import SellDoc, SellRequest, sell_cost, Sellingplatformslot, Sellingplatform
from django.db.models import AutoField
from action import Commit_selling_fullfill, record_sell_transaction

class SellingSlotInline(admin.TabularInline):
    model = Sellingplatformslot
    extra = 0

class SellingDocInline(admin.TabularInline):
    model = SellDoc
    extra = 0
          
class SellingCostInline(admin.StackedInline):
    model = sell_cost
    extra = 1
    fieldsets = (
        (None, {
            'fields': (('sellprice', 'tax_charged','shipping_handling'),'account_product_tax')
        }),
        ('shipping', {
            'fields': ('shipping', 'account_shipping','shippment')
        }),
        ('Financial', {
            'fields': ('financialcharge', 'account_financial')
        }),        
        ('Platform', {
            'fields': ('commission', 'account_commission')
        }),
    )
    
    #list_display =('id','productcost','tax','shipping','commission','total_cost')
    #actions = [export_as_csv_action("CSV Export", fields=['id','Person','Itemtemplate','Quantity','TotalReceiptPrice','TotalCost'])]


class SellRequestAdmin(admin.ModelAdmin):
    list_display =('id','item_list','sale_platform','sale_URL','order_on','order_id','custom','fullfilled','fee_platform','tracking_number') #,'total_income','total_deducation','net_earn','fullfilled')
    filter_horizontal = ('items',)
    inlines  = [SellingSlotInline,SellingCostInline, SellingDocInline,]
    actions = ['Commit_fullfill','Record_transaction',]
    
    def Commit_fullfill(self,request,queryset):
        for sellrequest in queryset:
            if not sellrequest.fullfilled:  # if not fullfilled before
                
                # add assets
                Commit_selling_fullfill(sellrequest)    
                # add transactiions
                #record_purchase_transaction(purchaserequest)
                # register storage
                #register_storage(purchaserequest)    

    
    def Record_transaction(self,request,queryset):
        ''' for temprary use '''
        for sellrequest in queryset:
            record_sell_transaction(sellrequest)
    
    
admin.site.register(SellRequest,SellRequestAdmin)
admin.site.register(Sellingplatform)