from models import authors
from publications.models import Authorship
def Merge_author(request, queryset):
    
    objs= list(queryset)
    
    for obj in objs[1:]:  # loop over the rest instance
        arecords = Authorship.objects.filter(author=obj)
        
        for arecord in arecords:
            arecord.author = objs[0]
            arecord.save()
        
        obj.delete()


def find_or_create_authorlist(inputstring,pb):
    aulist = []
    if ',' in inputstring:
        strings = inputstring.split(',')
        
        i = 1
        for singlestr in strings:
            au = find_or_create_author(singlestr)
            au1 = Authorship(author=au,publication=pb,sequence=i)
            au1.save()
            aulist.append(au1)
            i += 1
            
            
    else:
        au = find_or_create_author(inputstring)
        au1 = Authorship(author=au,publication=pb,sequence=1)
        au1.save()
        aulist.append(au1)
        
    return aulist


def find_or_create_author(inputstring):
    if ',' in inputstring:
        name = inputstring.split(',')
        lastname = name[0]
        firstname = name[1]
    
    else:
        name = inputstring.split(' ')
        lastname = name[-1]
        firstname = ' '.join(name[:-1])
    
    try:
        spauthor = authors.objects.get(firstname=firstname.strip(),lastname=lastname.strip())
    except:
        spauthor = authors()
        spauthor.firstname = firstname.strip()
        spauthor.lastname = lastname.strip()
        spauthor.middlename = ''
        spauthor.save()
        

    return spauthor