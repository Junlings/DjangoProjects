from django.contrib import admin

from models import accounts, transactions, TransactionConfirmCredit, TransactionConfirmDebit, AccountMonthlySummary #transaction_requests, transaction_responses
from django.contrib.contenttypes.models import ContentType
'''
class RequestInline(admin.StackedInline):
    model = transaction_requests
    #max_num = 1

class ResponseInline(admin.StackedInline):
    model = transaction_responses
    #max_num = 1
'''

class TransactionConfirmCreditInline(admin.StackedInline):
    model = TransactionConfirmCredit
    #max_num = 1

class TransactionConfirmDebitInline(admin.StackedInline):
    model =  TransactionConfirmDebit
    #max_num = 1

class AccountAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('owner', 'nickname','type','endwith')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('associate', 'expire', 'verify','notes')
        }),
    )
    
    list_display =('id','__unicode__','type')
    actions = ['generate_summary_2012']
    #actions = [export_as_csv_action("CSV Export", fields=['id','Person','Itemtemplate','Quantity','TotalReceiptPrice','TotalCost'])]
    
    def generate_summary_2012(self,request,queryset):
        for item in queryset:
            item.generate_summary('2012')    
    
class TransactionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('account', {
            'fields': (('accountA', 'modeA'),('accountB', 'modeB'),'amount','lastmodified','fullfilled')
        }),
        ('relation', {
            'fields': ('content_type', 'object_id','fieldname')
        }),
        ('notes', {
            'classes': ('collapse',),
            'fields': ('notes',)
        })
        
    )
    inlines = [TransactionConfirmCreditInline,TransactionConfirmDebitInline]

    list_display =('id','accountA','modeA','accountB','modeB','amount','content_type','object_id','fieldname','lastmodified','notes','fullfilled')    

    actions = ['batch_adjust_objs_purchase','batch_adjust_objs_sell']
    
    
    def batch_adjust_objs_purchase(self,request,queryset):
        for item in queryset:
            item.content_type = ContentType.objects.get(app_label="vending", model="Purchase_cost")
            item.save()
    def batch_adjust_objs_sell(self,request,queryset):
        for item in queryset:
            item.content_type = ContentType.objects.get(app_label="sellings", model="sell_cost")
            item.save()
  
    
class AccountMonthlySummaryAdmin(admin.ModelAdmin):
    list_display =('id','account','number_of_transaction','year','month','total_credit','total_debit','balance')#,'object_id','fieldname','lastmodified','notes','fullfilled')    
    actions = ['get_transaction','get_transaction_summary',]
    filter_horizontal = ('transaction',)
    
    def get_transaction(self,request,queryset):
        for item in queryset:
            item.get_transactions()

    def get_transaction_summary(self,request,queryset):
        for item in queryset:
            item.get_transaction_summary()
            
admin.site.register(accounts, AccountAdmin)
admin.site.register(transactions,TransactionAdmin)
admin.site.register(AccountMonthlySummary,AccountMonthlySummaryAdmin)

