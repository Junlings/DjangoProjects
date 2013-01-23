import os
import sys
import datetime
from django.conf import settings

def default(f):
    now = datetime.datetime.now()
    path = os.path.join(settings.MEDIA_ROOT,'doc',str(now.year),str(now.month),str(now.day))
    
    try:
       os.makedirs(path)
    except OSError:
       pass   
    
    full_location = os.path.join(path,f.name)
    dest = open(full_location, 'wb+') # write should overwrite the file
    for chunk in f.chunks():
        dest.write(chunk)
    dest.close()
    
    return full_location