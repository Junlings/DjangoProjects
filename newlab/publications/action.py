from models import keywords

def find_or_create_keywordlist(inputstring):
    aulist = []
    if ',' in inputstring:
        strings = inputstring.split(',')
        
        i = 1
        for singlestr in strings:
            kw = find_or_create_keyword(singlestr)
            aulist.append(kw)
            i += 1
            
            
    else:
        kw = find_or_create_keyword(inputstring)
        aulist.append(kw)
        
    return aulist


def find_or_create_keyword(inputstring):
    
    try:
        kw = keywords.objects.get(KW=inputstring.strip())
    except:
        kw = keywords(KW=inputstring.strip())
        kw.save()
        

    return kw