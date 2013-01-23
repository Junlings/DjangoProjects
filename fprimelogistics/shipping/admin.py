from django.contrib import admin

from models import shipments


class ShipmentsAdmin(admin.ModelAdmin):
    fields = ('nickname','carrier','tracking','notes')
    
    list_display =('id','__unicode__','tracking')
    #actions = [export_as_csv_action("CSV Export", fields=['id','Person','Itemtemplate','Quantity','TotalReceiptPrice','TotalCost'])]


admin.site.register(shipments, ShipmentsAdmin)



