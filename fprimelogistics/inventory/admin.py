from django.contrib import admin

from models import storage

'''
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
    #actions = [export_as_csv_action("CSV Export", fields=['id','Person','Itemtemplate','Quantity','TotalReceiptPrice','TotalCost'])]

class TransactionAdmin(admin.ModelAdmin):
    fieldsets = (
        ('account', {
            'fields': ('credit_account', 'debit_account','amount')
        }),
        ('notes', {
            'classes': ('collapse',),
            'fields': ('notes',)
        }),
        ('administration', {
            'classes': ('collapse',),
            'fields': (( 'submit','submit_by'), ('approve','approve_by'))
        }),        
        
        
    )
    
    list_display =('id','credit_account','debit_account','amount','submit','approve')    
    

admin.site.register(accounts, AccountAdmin)
admin.site.register(transactions,TransactionAdmin)

'''
admin.site.register(storage)