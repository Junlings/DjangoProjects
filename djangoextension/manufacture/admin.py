from django.contrib import admin

from models import Manufacturer, ItemProduct
from uti.cvs_io import export_csv_template_action
class ItemProductAdmin(admin.ModelAdmin):
     actions = [export_csv_template_action("CSV Template Export")]


admin.site.register(Manufacturer)
admin.site.register(ItemProduct,ItemProductAdmin)
