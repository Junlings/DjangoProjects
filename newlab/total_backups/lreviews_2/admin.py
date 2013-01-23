from django.contrib import admin

from models import singlereviews, reviewproj, reviewquestion,Choice
from django.db.models import AutoField

from django.contrib.contenttypes.generic import GenericTabularInline
'''
class fulltextInline(GenericTabularInline):
    model = commfulltext
    extra = 0
'''    
class reviewchoicesInline(admin.TabularInline):
    model = Choice
    extra = 0
    
class reviewquestionInline(admin.TabularInline):
    
    model = reviewquestion
    extra = 0
    
class singlereviewsInline(admin.TabularInline):
    #inlines  = [fulltextInline]
    model = singlereviews
    extra = 0
    
class ReviewProjAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('shortname',)}
    list_display = ('id','shortname')
    inlines  = [reviewquestionInline]
    filter_horizontal = ('managers','contributors',)

class reviewquestionAdmin(admin.ModelAdmin):
    list_display = ('id','project','question','qtype','order','get_choices')
    inlines  = [reviewchoicesInline]
    

    
admin.site.register(reviewproj,ReviewProjAdmin)
admin.site.register(reviewquestion,reviewquestionAdmin)
admin.site.register(singlereviews)
admin.site.register(Choice)