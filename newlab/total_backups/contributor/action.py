from journal.models import journalarticle

def Merge_author(request, queryset):
    
    objs= list(queryset)
    
    for obj in objs[1:]:  # loop over the rest instance
        arecords = Authorship.objects.filter(author=obj)
        
        for arecord in arecords:
            arecord.author = objs[0]
            arecord.save()
        
        obj.delete()