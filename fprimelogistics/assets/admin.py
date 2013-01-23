from django.contrib import admin
import datetime
from models import asset, assetgroup, assetstorage, assetestimate
from inventory.models import storage
from sellings.models import SellRequest
from action import update_estimate

class AssetStorageInline(admin.StackedInline):
    model = assetstorage
    extra = 0
    
    fieldsets = (
        (None, {
            'fields': ('location', ('movein','moveout'))
        }),
    )    
    
class AssetGroupAdmin(admin.ModelAdmin):

    filter_horizontal = ('assets',)
    list_display =('id','name')

class EstimateAdmin(admin.ModelAdmin):

    #filter_horizontal = ('assets',)
    list_display =('id','asset')


class AssetAdmin(admin.ModelAdmin):
    list_display =('id','item','FSIN','created','location','onsale','sold')
    inlines  = [AssetStorageInline,]
    list_filter = ['onsale','sold',]
    
    actions = ['update_status','Move_TO_FBA','Move_TO_YULIN','Move_TO_JUNXIA','Move_TO_JUNHUANG','Move_TO_LICHEN','Set_onsale','Set_sold','update_estimate']
    
    def update_status(self,request,queryset):
        for asset in queryset:
            if asset.onsale != True:
                for obj in SellRequest.objects.all():
                    if asset in obj.items.all():
                        asset.onsale = True
                        asset.save()
                        break
        return 1            
    
    
    def update_prev_location(self,obj,newlocal):
        current_location = assetstorage.objects.filter(item=obj).order_by('-movein')[0]
        if newlocal != current_location.location: 
            # update prev location moveout
            current_location.moveout = datetime.datetime.now()
            current_location.save()
            # create new location
            assetstorageinst = assetstorage(item=obj,location=newlocal,movein=datetime.datetime.now())
            assetstorageinst.save()
        
        return 1
    
    def Move_TO_FBA(self,request,queryset):
        NEW_LOC = storage.objects.get(nickname='amazon FBA')
        for asset in queryset:
            self.update_prev_location(asset,NEW_LOC)
            
    def Move_TO_YULIN(self,request,queryset):
        NEW_LOC = storage.objects.get(nickname='yulin xiao home')
        for asset in queryset:
            self.update_prev_location(asset,NEW_LOC)

    def Move_TO_JUNXIA(self,request,queryset):
        NEW_LOC = storage.objects.get(nickname='jun xia home')
        for asset in queryset:
            self.update_prev_location(asset,NEW_LOC)

    def Move_TO_JUNHUANG(self,request,queryset):
        NEW_LOC = storage.objects.get(nickname='jun huang house')
        for asset in queryset:
            self.update_prev_location(asset,NEW_LOC)


    def Move_TO_LICHEN(self,request,queryset):
        NEW_LOC  = storage.objects.get(nickname='Li House')
        for asset in queryset:
            self.update_prev_location(asset,NEW_LOC)
    
    def Set_onsale(self,request,queryset):
        for asset in queryset:
            asset.onsale = True
            asset.save()
        
    def Set_sold(self,request,queryset):
        for asset in queryset:
            asset.sold = True
            asset.save()
        
    def update_estimate(self,request,queryset):
        for asset in queryset:
            update_estimate(asset)
        
        
admin.site.register(asset,AssetAdmin)
admin.site.register(assetgroup,AssetGroupAdmin)
admin.site.register(assetestimate,EstimateAdmin)

