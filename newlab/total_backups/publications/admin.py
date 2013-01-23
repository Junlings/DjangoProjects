from django.contrib import admin

from models import book, stand, thes, rprt, Authorship,keywords
from django.db.models import AutoField

from django.contrib.contenttypes.generic import GenericTabularInline

class authorshipInline(admin.TabularInline):
    model = Authorship
    extra = 0


    
class bookAdmin(admin.ModelAdmin):
    list_display = ('id','TI','PB','PY','VL','doc')
    fieldsets = (
        (None, {
            'fields': (('label', 'TI','PB','PY','VL')),
        }),
        ('File', {
            'fields': (('doc', 'doclink')),
        }),
    )
    inlines  = [authorshipInline]

class rprtAdmin(admin.ModelAdmin):
    list_display = ('id','label','TI','PB','PY','VL','doc')
    fieldsets = (
        (None, {
            'fields': (('label', 'TI','PB','PY','VL','SN')),
        }),
       ('File', {
            'fields': (('doc', 'doclink')),
        }),
    )
    inlines  = [authorshipInline]
    
class standAdmin(admin.ModelAdmin):
    list_display = ('id','label','TI','PB','PY','doc',)
    fieldsets = (
        (None, {
            'fields': (('label', 'TI','PB','PY','VL')),
        }),
        ('File', {
            'fields': (('doc', 'doclink')),
        }),
    )
    inlines  = [authorshipInline]
    
class thesAdmin(admin.ModelAdmin):
    list_display = ('id','label','TI','PB','PY','VL','doc',)    
    fieldsets = (
        (None, {
            'fields': (('label', 'TI','PB','PY','VL')),
        }),
        ('File', {
            'fields': (('doc', 'doclink')),
        }),
    )
    inlines  = [authorshipInline,]
    search_fields = ['TI']


admin.site.register(book,bookAdmin)
admin.site.register(stand,standAdmin)
admin.site.register(thes,thesAdmin)
admin.site.register(rprt,rprtAdmin)
admin.site.register(keywords)