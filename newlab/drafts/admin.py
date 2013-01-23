from django.contrib import admin

from models import document, sections, plainparagraph, equations, images, tables, plaintext


class sectionInline(admin.TabularInline):
    model = document.sections.through
    extra = 0

class paragraphinline(admin.TabularInline):
    model = sections.paragraph.through
    extra = 0
    
class textinline(admin.TabularInline):
    model = plainparagraph.texts.through
    extra = 0

class textinline(admin.TabularInline):
    model = plainparagraph.texts.through
    extra = 0
    
class tablesinline(admin.TabularInline):
    model = plainparagraph.tables.through
    extra = 0
    
class imagesinline(admin.TabularInline):
    model = plainparagraph.images.through
    extra = 0
    
class equationinline(admin.TabularInline):
    model = plainparagraph.equation.through
    extra = 0

class documentAdmin(admin.ModelAdmin):
    #list_display = ('id','LB','get_title','T2','get_author','get_KW','get_fulltext')
    inlines  = [sectionInline,]
    #actions = ['parse_RIS','export_bib',]
    
class sectionAdmin(admin.ModelAdmin):
    inlines  = [paragraphinline,]

class paragraphAdmin(admin.ModelAdmin):
    inlines  = [textinline,tablesinline,imagesinline,equationinline]

admin.site.register(plaintext)
admin.site.register(equations)
admin.site.register(images)
admin.site.register(tables)
admin.site.register(document,documentAdmin)
admin.site.register(sections,sectionAdmin) #,documentAdmin)
admin.site.register(plainparagraph,paragraphAdmin)
#admin.site.register(plaintext)
#admin.site.register(paragraph)
#admin.site.register(images)
#admin.site.register(section)
#admin.site.register(tables)
#admin.site.register(data)

