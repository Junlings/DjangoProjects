""" This module is used to retrive information about target store/ availbility and product
    last update: 2012-11-20

"""

import time
import urllib, urllib2
from BeautifulSoup import BeautifulSoup
import json
from uti import escapeSpecialCharacters, loop_check, data_prep, clean_price


def target_avail_encode(availbility):
    ''' ecnoding of the target stock information
    3: instock
    2: limited stock
    0: out of stock
    1: clearance
    -1: unknown
    '''
    
    if availbility == 'limited stock':
        return 2
    elif availbility == 'in stock':
        return 3
    elif availbility == 'out of stock':
        return 0
    else:
        return -1
    

def request_inventory_page(tcin,MY_ZIP='32826',Miles='20'):
    ''' make request and get inventory page '''
    # request based on zipcode
    url = 'http://m.target.com/fiats-results/t-%s?zipCode=%s' % (tcin,MY_ZIP)  
    fd = urllib2.urlopen(url).read()
    
    # scrpe the body only
    index1 = fd.find('<body')
    index2 = fd.find('</body>')
    return fd[index1:index2]

def request_product_page(tcin):
    ''' obtain product page'''
    url = "http://sites.target.com/site/en/spot/mobile_product_detail.jsp?tcin=%s" % tcin
    fd = urllib2.urlopen(url).read()
    index1 = fd.find('<body')
    index2 = fd.find('</body>')
    return fd[index1:index2]       
    
'''
def scrape_dcpi(productpage):
    #print fd
    index1 = productpage.find('&dpci')
    index2 = productpage[index1:].find('"')
    return productpage[index1+6:index1+index2]      
'''

def get_longname(productbox):
    name = productbox.find('h2',{"class":"product"}).text
    return name

def get_mainimagepath(productbox):
    
    imgpath = productbox.find('div', {"id":"product-images"}).find('img').attrs[0][1]
    #print imgpath
    return imgpath
    
def get_baseprice(productpage):
    # get online price
    index1 = productpage.find('$')
    index2 = productpage[index1:].find('.')
    
    price = productpage[index1:index1+index2+2]
    return clean_price(price)
    

def get_manufacture(longname):
    manufacture = longname.split(' ')[0].strip().lower()
    if '&reg' in manufacture:
        manufacture = manufacture[:-5]    
    return manufacture    


def get_local_avail(productpage):
    # get local available
    index1 = productpage.find('</hgroup>')
    index2 = productpage[index1:].find('</header>')
    avail = BeautifulSoup(productpage[index1:index1+index2])   
    #
    #print productpage
    avail2 = avail.find('p').text
    if avail2 == u'sold online & in stores':
        return {'online_avail':True,'local_avail':True}
    elif avail2 == u'sold online only':
        return {'online_avail':True,'local_avail':False}
    else:
        return {'online_avail':False,'local_avail':False}

def request_fullproduct_page(dpci):
    search_url = "http://www.target.com/s/" + dpci
    fd = urllib2.urlopen(search_url).read()
    

    index1 = fd.find('<span class="productTitle">')
    index2 = fd[index1:].find('</span>')
    prodlink = BeautifulSoup(fd[index1:index2+index1+1])
    
    #print prodlink
    url = prodlink.find('a').attrs[0][1]
    
    print 1
    


#=========function groups
def obtain_product(tcin):
    productpage = request_product_page(tcin)
    #dpci = scrape_dcpi(productpage)

    product_box = BeautifulSoup(productpage)
    print product_box
    product = {
        'longname' : get_longname(product_box),
        'shortname' : None,
        'modelid' : None,
        'brand':None,
        'upc':None}
    
    product.update(
        {
        'manufacturer' : {'name':get_manufacture(product['longname'])},
        'mainimagepath' : get_mainimagepath(product_box) ,
    })
    
    return product

def obtain_supply(tcin):
    productpage = request_product_page(tcin)
    #dpci = scrape_dcpi(productpage)  
    
    itemdict = {
        'suppliers' : {'name':'target'},
        'suppliers_PID' : tcin,
        'local_PID' : tcin,#dpci,
        'itemproduct':  obtain_product(tcin),
        'price_base': get_baseprice(productpage)}
    
    avail = get_local_avail(productpage)
    itemdict.update(avail)
    
    return itemdict


def check_online_price(tcin):
    productpage = request_product_page(tcin)
    dpci = scrape_dcpi(productpage)    
    
    return None  # not implemented

def check_online_avail(tcin):
    productpage = request_product_page(tcin)    
    if 'out of stock' in productpage:
        return False
    else:
        return True
    
    

def check_local_price(tcin):
    return None  # not implemented


def check_local_avail(tcin,MY_ZIP,Miles,key=None):
    
    inventorypage = request_inventory_page(tcin,MY_ZIP,Miles)

    #soup = BeautifulSoup(inventorypage)
    ol = BeautifulSoup(inventorypage).find('ol',{'class':"linked-table-rows"})
    stock_list = []



    for li in ol.findAll('li'):
        href = li.a['href']
        store_name = li.find('h4').text
        avil = li.find('p',{'class':'adr'}).text
        stock_list.append({'name':store_name,
                      'availbility':avil,'availcode':target_avail_encode(avil)})
    return stock_list


    
    for li in ol.findAll('li'):
        href = li.a['href']
        store_name = li.find('h4').text
        avil = href.split('=')[-1]
        num = href.split('=')[1].split('/')[-1].split('-')[-1]
        stock_list.append({'name':store_name,'num':num,
                      'availbility':avil,'availcode':target_avail_encode(avil)})
    return stock_list

def check_local_avail_listset(supplier_PID,ziplist):
    ''' check the instore availbility for given queryset'''

    Miles = 100
    avail_store_dict = loop_check(ziplist,check_local_avail,supplier_PID,Miles,keytype='name')
    return avail_store_dict


def check_local_avail_queryset(supplier_PID,queryset,keytype='name'):
    storelist,input = data_prep(queryset,keytype)
    
    # need to get dpci based on online id
    
    availdata =check_local_avail_listset(supplier_PID,input)    
    print availdata
    return storelist,availdata


if __name__ == '__main__':
    
    tcin = '14007156'
    dpci = '072-08-0400'
    #res = request_inventory_page(dpci)
    #productpage = request_product_page(tcin)
    #res = scrape_dcpi(productpage)
    
    #res = obtain_product(tcin)
    #res = obtain_supply(tcin)
    avail = check_local_avail(tcin,'32826','20')
    print avail
    #availlist = check_local_avail_listset('14007156',[('1','32608','Gainesville'),('2','32822','Ocala')])
    #print availlist
    
    #print res
#   print 1
    print 1