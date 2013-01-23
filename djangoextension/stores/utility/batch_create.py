from stores.models import inventory_results
from purchases.models import ItemTemplate
from django.contrib.auth.models import User
from datetime import datetime
import cPickle as pickle
from views import search_results_internal
import time
from utility.dumpload import dump_data, load_data

PRODUCT_LIST = (
    
    (10,'ipad3/64/4/A/W'),
    (11,'ipad3/64/4/A/B'),
    (12,'ipad3/32/4/A/W'),
    (13,'ipad3/32/4/A/B'),
    (14,'ipad3/16/4/A/B'),
    (15,'ipad3/16/4/A/W'),
    
)


US_STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

def batch_create(obj_id):
    ''' for single item, add all state instance to the models'''
    item = ItemTemplate.objects.get(pk=obj_id)
    user = User.objects.all()[0]
    for state in US_STATES:
        print state[0]
        temp = {'name':str(item.id) + '_' + state[0],
                'item':item,
                'owner':user,
                'state':state[0],
                'last_commit':datetime.now(),
                'search_interval':'10 days'}
        p = inventory_results(**temp)
        p.save()



def simple_res(avail_store_dict):
    temp_store = {}
    for key in avail_store_dict.keys():
        store = avail_store_dict[key]
        temp_store[key] = {'state':store['state'],
                           'city':store['city'],
                           'zipcode':store['zipcode'],
                           #'storeId':store['storeId'],
                           'availbility':store['availbility'],
                           'icon':store['icon']
                           }
    return temp_store
    
def batch_update(obj_id,filename):
    ''' update the status for single item for all existing inventory results '''
    item = ItemTemplate.objects.get(pk=obj_id)
    objs = inventory_results.objects.filter(item=item)
    all_res = {}
    
    for obj in objs:
        time.sleep(1.0)
        avail_store_dict = search_results_internal(obj)
        try:
            all_res.update(simple_res(avail_store_dict))
        except:
            continue
    foutname = '%(name)s_%(id)s_%(datetime)s' % {'name':filename,'id':obj_id,'datetime':datetime.now()}
    folder = 'doc/inventory/commit'
    dump_data(foutname,all_res,folder=folder)
    
def update_ipad3_4g():
    
    for product in PRODUCT_LIST:
        batch_update(product[0],product[1])