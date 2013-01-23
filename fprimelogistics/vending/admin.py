from django.contrib import admin

from models import PurchaseDoc, PurchaseRequest, Purchase_cost
from action import Commit_vending_fullfill, record_purchase_transaction

class PurchaseDocInline(admin.TabularInline):
    model = PurchaseDoc
    extra = 0
          
 
    
class PurchaseCostInline(admin.StackedInline):
    model = Purchase_cost
    extra = 1
    fieldsets = (
        (None, {
            'fields': (('productcost', 'tax'),'account_product_tax')
        }),
        ('shipping', {
            'fields': ('shipping', 'account_shipping','shippment')
        }),
        ('Commission', {
            'fields': ('commission', 'account_commission')
        }),
    )
    
    #list_display =('id','productcost','tax','shipping','commission','total_cost')
    #actions = [export_as_csv_action("CSV Export", fields=['id','Person','Itemtemplate','Quantity','TotalReceiptPrice','TotalCost'])]


class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display =('id','item','orderon','storage','quantity','person','docs_count','account_info','fullfilled')
    list_filter = ['fullfilled',]
    #search_fields = ['item',]
    filter_horizontal = ('assets',)
    inlines  = [PurchaseCostInline, PurchaseDocInline,]
    actions = ['Commit_fullfill','Record_transaction']

    def Commit_fullfill(self,request,queryset):
        for purchaserequest in queryset:
            
            if not purchaserequest.fullfilled:  # if not fullfilled before
                
                # add assets
                Commit_vending_fullfill(purchaserequest)    
                # add transactiions
                record_purchase_transaction(purchaserequest)
                # register storage
                #register_storage(purchaserequest)
                
    def Record_transaction(self,request,queryset):
        ''' for temprary use '''
        for purchaserequest in queryset:
            record_purchase_transaction(purchaserequest)
    
admin.site.register(PurchaseRequest,PurchaseRequestAdmin)

