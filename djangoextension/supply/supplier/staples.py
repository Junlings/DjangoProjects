import urllib, urllib2
from BeautifulSoup import BeautifulSoup
import json

import cPickle as pickle
import csv
import time
from uti import escapeSpecialCharacters, loop_check, data_prep, clean_price

LOCAL_STORE_MODEL = None

def staples_avail_encode(availbility):
    if 'Clearance' in availbility:
        return 1
    elif 'In' in availbility:
        return 3
    elif 'Low' in availbility:
        return 2
    elif 'Not' in availbility:
        return 0
    else:
        return -1

#=========block functions
def request_product_page(sku):
    """ make request to page and scrape only the body-footer region """
    url = "http://www.staples.com/product-nr_%s" % str(sku)
    fd = urllib2.urlopen(url).read()
    index1 = fd.find('<body')
    index2 = fd.find('<div id="footer">')
    return fd[index1:index2]

def request_inventory_page(sku,MY_ZIP="32826",Miles='20'):
    sku = sku
    url ='http://www.staples.com/office/supplies/StaplesStoreInventory?storeId=10001&catalogId=10051&langId=-1&'
    url += 'partNumber=%s&catentryId=&address1=&city=&state=&zipCode=%s&distance=%s' % (sku,MY_ZIP,Miles)
    
    params = urllib.urlencode({
        'partNumber':'sku',
        'catentryId': '',
        'address1':'',
        'city':'',
        'state':'',
        'zipCode':32826,
        'distance':20,
        })
    req = urllib2.Request(url)#
    fd = urllib2.urlopen(req).read()
    index1 = fd.find('<body')
    index2 = fd.find('<div id="footer">')
    return fd[index1:index2]

def scrape_product_box(inventory_page):
    """ search certain page and return beautiful soup region """
    index1 = inventory_page.find('<div id="wrapall">')
    soup = BeautifulSoup(inventory_page[index1:])
    productbox = soup.find('div',{'class':"productbox"})
    return productbox

def scrape_inventory_box(inventory_page):
    index1 = inventory_page.find('<table id="resultsTbl">')
    index2 = inventory_page.find('</table>')
    inventory = BeautifulSoup(inventory_page[index1:index2])
    return inventory    

def scrape_price_box(product_page):
    #print product_page
    index1 = product_page.find('<div class="pricenew">')
    index2 = product_page[index1:].find('class="pqty"')
    
    if index1 == -1:
        index1 = product_page.find('<td class="pricenew specon"')
        index2 = product_page[index1:].find('<dd class="pqty">')        
    res = BeautifulSoup(product_page[index1:index2+index1])
    return res    
    

def get_mainimagepath(productbox):
    productimg = productbox.find('img')['src']
    return productimg
    
def get_longname(productbox):
    longname = productbox.find('p',{'class':"skutitle"}).text
    return longname

def get_manufacture(longname):
    manufacture = longname.split(' ')[0].strip().lower()
    if '&reg' in manufacture:
        manufacture = manufacture[:-5]    
    return manufacture

def get_modelid(productbox):
    modelid = productbox.find('p',{'class':"model"}).text.strip()[6:]
    return  modelid

def get_local_avail(product_page):
    # get local available
    if product_page.find('<li class="storeavail">') != -1:
        instore = True
    else:
        instore = False
    return instore

def get_baseprice(price_box):
    #print price_box
    try:
        price_base = price_box.find('i').text
    except:
        ii = price_box.find('b')
        price_base = ii.text  
    
    return clean_price(price_base)

#=========function groups
def obtain_product(sku):
    inventory_page = request_inventory_page(sku)
    product_box = scrape_product_box(inventory_page)
    
    product = {
        'longname' : get_longname(product_box),
        'shortname' : None,
        'modelid' : get_modelid(product_box),
        'upc':None}
    
    mau = get_manufacture(product['longname'])
    product.update(
        {
        'manufacturer' : {'name':mau},
        'mainimagepath' : get_mainimagepath(product_box) ,
        'brand':mau,
    })
    
    return product


def obtain_supply(sku):
    product_page = request_product_page(sku)
    price_box = scrape_price_box(product_page)    
    
    itemdict = {
        'suppliers' : 'staples',
        'suppliers_PID' : sku,
        'local_PID' : sku,
        'itemproduct':  obtain_product(sku),
        'price_base': get_baseprice(price_box),
        'online_avail':True,
        'local_avail':get_local_avail(product_page) 
    }
    
    return itemdict
    
def check_online_price(sku):
    product_page = request_product_page(sku)
    price_box = scrape_price_box(product_page)      
    
    # get online price
    try:
        price_base = price_box.find('i').text
        price_web = None
    except:
        ii = price_box.find('b')
        price_base = ii.text
        price_web = ii.findNext('b').text
    return price_web

def check_online_avail(sku):
    return None  # not implemented

def check_local_price(sku):
    return None  # not implemented

def check_local_avail(sku,MY_ZIP,Miles,key=None):
    stock_list = []
    
    inventory_page = request_inventory_page(sku,MY_ZIP,Miles)
    inventory_box = scrape_inventory_box(inventory_page)
    #print inventory_box

    for li in inventory_box.find('tbody').findAll('tr'):
        store = li.find('td').contents
        try:
            store_name = store[0].__unicode__() + store[2].__unicode__() + store[4].__unicode__()
        except:
            try:
                store_name = store[0].__unicode__() + store[2].__unicode__()
            except:
                raise error
        #print '=============='
        store_name = escapeSpecialCharacters(store_name,'\t')
        avil = li.find('p').contents[0].__unicode__()
        avil = escapeSpecialCharacters(avil,'\t')
        avil = escapeSpecialCharacters(avil,'\n').strip()
        #print avil
        stock_list.append({'store_name':store_name,'zipcode':store_name.split('\n')[-2],
                      'availbility':avil,'availcode':staples_avail_encode(avil)})
    return stock_list

def check_local_avail_listset(supplier_PID,ziplist,primarykey='zipcode'):
    ''' check the instore availbility for given queryset'''
    Miles = 100
    avail_store_dict = loop_check(ziplist,check_local_avail,supplier_PID,Miles,keytype='zipcode')
    return avail_store_dict


def check_local_avail_queryset(supplier_PID,queryset,keytype='zipcode'):
    storelist,input = data_prep(queryset,keytype)
    availdata = check_local_avail_listset(supplier_PID,input)    
    return storelist,availdata


if __name__ == '__main__':
    res = obtain_supply('414699')
    print res
    #avail = check_local_avail('344778','32826','20')
    #availlist = check_local_avail_listset('344778',[('1','32828','32828')])
    #print availlist 
    print 1