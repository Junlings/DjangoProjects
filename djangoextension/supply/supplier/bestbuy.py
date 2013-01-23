import time
import urllib, urllib2
from BeautifulSoup import BeautifulSoup
import json
from uti import escapeSpecialCharacters, loop_check, data_prep, clean_price



LOCAL_STORE_MODEL = None


def bestbuy_avail_encode(availbility):
    if availbility == True:
        return 3
    elif availbility == False:
        return 0
    elif availbility == -1:
        return -1
    else:
        return 99


def request_product_page(sku):
    req = 'http://api.remix.bestbuy.com/v1/products%28sku='+ sku + '%29?apiKey=42jtrdyejxvxs968x9c3xmxw&format=json'
    
    fd = urllib2.urlopen(req)
    aa = json.loads(fd.read())['products'][0]    
    
    return aa

def request_inventory_page(sku,MY_ZIP='32826',Miles='20'):

    store_req = 'http://api.remix.bestbuy.com/v1/stores%28area%28'
    store_req += MY_ZIP + ',' + Miles
    store_req += '%29%29+products%28sku=' + sku
    store_req += '%29?apiKey=42jtrdyejxvxs968x9c3xmxw'
    store_req += '&format=json'
    
    fd = urllib2.urlopen(store_req)
    aa = json.loads(fd.read())
    
    return aa['stores']    
    


def obtain_product(sku):
    product_box = request_product_page(sku)
    if len(product_box['modelNumber'].split(' ')) > 1:
        modelid = ' '.join(product_box['modelNumber'].split(' ')[1:])
        brand = product_box['modelNumber'].split(' ')[0]
    else:
        modelid = product_box['modelNumber']
        brand = product_box['manufacturer'].lower()
    
    product = {
        'longname' : product_box['name'],
        'shortname' : product_box['modelNumber'],
        'modelid' : modelid,
        'brand':brand,
        'upc': product_box['upc']
    }
    
    product.update(
        {
        'manufacturer' : {'name':product_box['manufacturer'].lower()},
        'mainimagepath' : product_box['image'],
    })
    
    return product

def obtain_supply(sku):  
    product_box = request_product_page(sku)
    inventory_box = request_inventory_page(sku)
    if len(inventory_box) == 0:
        offer_box = {'active':False,'onlineAvailability':False,'regularPrice':'0.0'}
    
    else:
        offer_box = inventory_box[0]['products'][0]
    itemdict = {
        'suppliers' : 'bestbuy',
        'suppliers_PID' : sku,
        'local_PID' : sku,
        'itemproduct':  obtain_product(sku),
        'price_base': clean_price(offer_box['regularPrice']),
        'online_avail':offer_box['active'],
        'local_avail':offer_box['onlineAvailability'] 
    }
    
    return itemdict


def check_online_price(sku):
    product_box = request_product_page(sku)
    inventory_box = request_inventory_page(sku)
    offer_box = inventory_box[0]['products'][0]     
    
    if offer_box['onSale']:
        onsale = offer_box['offers']
    else:
        onsale = False
    
    resdict= {
        'online_price':offer_box['priceInCart'],
        'online_sale': onsale,
        'source_data':offer_box['priceUpdateDate']
    }
    return resdict

def check_online_avail(sku):
    product_box = request_product_page(sku)
    inventory_box = request_inventory_page(sku)
    offer_box = inventory_box[0]['products'][0]
    resdict= {
        'online_inventory':offer_box['onlineAvailability'],
        'source_data':offer_box['onlineAvailabilityUpdateDate']
    }
    return resdict    
    
def check_local_price(sku):
    product_box = request_product_page(sku)
    inventory_box = request_inventory_page(sku)
    offer_box = inventory_box[0]['products'][0]     
    
    if offer_box['onSale']:
        onsale = offer_box['offers']
    else:
        onsale = False
    
    resdict= {
        'local_sale': onsale,
        'local_price':offer_box['salePrice'],
        'source_data':offer_box['priceUpdateDate']
    }
    return resdict

    
def check_local_avail(sku,MY_ZIP,Miles,key=None):
    MYZIP = str(MY_ZIP)
    Miles = str(Miles)
    inventory_box = request_inventory_page(sku,MYZIP,Miles)
    record_self = 0
    
    if len(inventory_box) > 0:
        return_store = []
        for store in inventory_box:
            mystore = {}
            mystore['zipcode'] = store['postalCode']
            mystore['availbility'] = store['products'][0]['inStoreAvailability']
            mystore['availcode'] = bestbuy_avail_encode(mystore['availbility'])
            mystore['store_name'] = store['longName']
            mystore['num'] = str(store['storeId'])
            
            if mystore['zipcode'] == MYZIP:
                record_self = 1
            return_store.append(mystore)
    else:
        store = {}
        store['zipcode'] = MYZIP
        store['availbility'] = -1
        store['availcode'] = bestbuy_avail_encode(store['availbility'])
        store['num'] = key
        #store['store_name'] = store['longName']
        return_store = [store]
    
    if record_self == 1:
        ''' which means this zip do not sell that '''
        return_store.append({  'zipcode':MYZIP,
                               'availbility':0,
                               'availcode' : bestbuy_avail_encode(0),
                               'num':key
                               })

    return return_store

def check_local_avail_listset(supplier_PID,ziplist):
    ''' check the instore availbility for given queryset'''
    Miles = 100
    avail_store_dict = loop_check(ziplist,check_local_avail,supplier_PID,Miles,keytype='num')
    return avail_store_dict


def check_local_avail_queryset(supplier_PID,queryset,keytype='num'):
    #print supplier_PID
    storelist,input = data_prep(queryset,keytype)
    availdata = check_local_avail_listset(supplier_PID,input)    
    return storelist,availdata

if __name__ == '__main__':
    #res = request_product_page('2044104')
    #product = obtain_product('2044104')
    #supply = obtain_supply('4881212')
    #price  = check_online_price('2044104')
    #avail = check_online_avail('2044104')
    #avail = check_local_price('2044104')
    avail = check_local_avail('3158934','32826','20')
    #avail = availlist = check_local_avail_listset('2044104',[('1530','32839'),('510','32809')])
    
    #print avail
    print supply
    print 1