import math
import time
import urllib, urllib2

import json
def get_geocode(zipcode):
    time.sleep(0.5)  # wait 0.5 second for each request
    #print 'process zipcode', zipcode
    
    address = urllib.quote(zipcode)
    url ='http://maps.googleapis.com/maps/api/geocode/json?address='
    url +='%s&sensor=false' % address
    
    req = urllib2.Request(url)
    fd = urllib2.urlopen(req).read()
    
    aa = json.loads(fd)
    
    try:
        latlng = aa['results'][0]['geometry']['location']
        return [latlng['lat'],latlng['lng']]
    except:
        return None

def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km
    
    lat1 = float(lat1)
    lon1 = float(lon1)
    lat2 = float(lat2)
    lon2 = float(lon2)
    
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d*0.621371192  # to convert to miles

if __name__ == '__main__':
    seattle = [47.621800, -122.350326]
    olympia = [47.041917, -122.893766]
    print distance(seattle, olympia)
    
    print get_geocode('14801')
    
    print distance(get_geocode('32826'),get_geocode('32608'))