from django.contrib import admin

from models import PostSellRequest, postsell_cost, PostsellDoc

class PostDocInline(admin.TabularInline):
    model = PostsellDoc
    extra = 0
          
 
    
class PostCostInline(admin.StackedInline):
    model = postsell_cost
    fieldsets = (
        (None, {
            'fields': (('restockingfee', 'tax_chargedback'),'account_product_tax')
        }),
        ('shipping', {
            'fields': ('shipping', 'account_shipping','shippment')
        }),
        ('Commission', {
            'fields': ('commission', 'account_commission')
        }),
    )

class PostRequestAdmin(admin.ModelAdmin):
    list_display =('id',)
    inlines  = [PostCostInline,PostDocInline,]
    
admin.site.register(PostSellRequest,PostRequestAdmin)
