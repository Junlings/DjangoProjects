import time
import urllib, urllib2
from BeautifulSoup import BeautifulSoup
import json
from uti import escapeSpecialCharacters, loop_check, data_prep, clean_price
LOCAL_STORE_MODEL = None

def walmart_avail_encode(availbility):
    if availbility == 'Limited stock':
        return 2
    elif availbility == 'In stock':
        return 3
    elif availbility =='Out of stock':
        return 0
    else:
        return 0

def request_product_page(product_ID):
    url_onlinecheck = 'http://mobile.walmart.com/ip/' + product_ID
    req_onlinecheck = urllib2.Request(url_onlinecheck)
    fd = urllib2.urlopen(req_onlinecheck).read()
    
    index1 = fd.find('<body')
    index2 = fd[index1:].find('</body>')
    return fd[index1:index2]

def request_fullproduct_page(product_ID):
    url_onlinecheck = 'http://www.walmart.com/ip/' + product_ID
    req_onlinecheck = urllib2.Request(url_onlinecheck)
    fd = urllib2.urlopen(req_onlinecheck).read()
    #print fd
    index1 = fd.find('<body')
    index2 = fd[index1:].find('</body>')
    return fd[index1:index2+index1]    
    
def request_inventory_page(product_ID,MY_ZIP='32826',Miles='20'):

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.13) Gecko/2009073021 Firefox/3.0.13')]
    
    url_instorecheck = 'http://mobile.walmart.com/m/searchfindinstoreresults?product_id=' + product_ID + '&zip=' + MY_ZIP+'&all'    
    fd_instorecheck = opener.open(url_instorecheck)
    
    fd = fd_instorecheck.read()
    index1 = fd.find('<body')
    index2 = fd[index1:].find('</body>')
    soup = BeautifulSoup(fd[index1:index2+index1])
    return soup

def scrape_product_box(product_page):
    """ search certain page and return beautiful soup region """
    index1 = product_page.find('<div class="productTitle">')
    index2 = product_page[index1:].find('<div class="section socialBtn">')
    soup = BeautifulSoup(product_page[index1:index2+index1])
    productbox = soup
    return productbox


def extract_variables(fd,name,end=','):
    index1 = fd.find(name)
    index2 = fd[index1:].find(end)
    key,value = fd[index1:index2+index1].split(':')
    key = key.strip()
    if "'" in value:
        value = value.strip()[1:-1]
    else:
        value = value.strip()
    return value
    
def scrape_specification_box(fullproductpage):
    
    index1 = fullproductpage.find('<div class="LargeItemPhoto215"')
    index2 = fullproductpage[index1:].find('<img')
    fd_img = fullproductpage[index1:index1+index2]
    imgpath = "http:"+extract_variables(fd_img,"http://i.walmartimages.com",".jpg")+".jpg"
    
    try:
        index1 = fullproductpage.find('var DefaultItem =')
        index2 = fullproductpage[index1:].find('</script>')
        fd = fullproductpage[index1:index1+index2]
        
        product = {
            'longname' : extract_variables(fd,'prodName',"\n")[:-1],
            'shortname' : None,
            'modelid' : extract_variables(fd,'model'),
            'brand':extract_variables(fd,'brand'),
            'upc':extract_variables(fd,'upc'),
            }
        
        product.update(
            {
            'manufacturer' : {'name':extract_variables(fd,'brand').lower()},
            'mainimagepath' : imgpath ,
        })
    except:
        index1 = fullproductpage.find('WALMART.analytics.bluekai.defaultItem')
        index2 = fullproductpage[index1:].find('WALMART.analytics.bluekai.variants')
        fd = fullproductpage[index1:index1+index2]
        
        product = {
            'longname' : extract_variables(fd,'prodName',"\n")[:-1],
            'shortname' : None,
            'modelid' : extract_variables(fd,'model'),
            'brand':extract_variables(fd,'brand'),
            'upc':extract_variables(fd,'upc'),
            }
        
        product.update(
            {
            'manufacturer' : {'name':extract_variables(fd,'brand').lower()},
            'mainimagepath' : imgpath ,
        })
        
    return product
    

def get_mainimagepath(productbox):
    productimg = productbox.find('div', {'class':"productContent"}).find('img')['src']
    return productimg

def get_longname(productbox):
    #print productbox
    longname = productbox.find('div',{'class':"productTitle"}).find('span').text
    return longname

def get_specification(specification_box):
    
    for item in specification_box.findAll('tr'):
        print item
    
    

def obtain_product(sku):

    full_product_page = request_fullproduct_page(sku)
    product = scrape_specification_box(full_product_page)
    
    return product

def obtain_supply(sku):
    fullproductpage = request_fullproduct_page(sku)
    
    index1 = fullproductpage.find('var DefaultItem =')
    index2 = fullproductpage[index1:].find('</script>')
    fd = fullproductpage[index1:index1+index2]    
    
    itemdict = {
        'suppliers' : 'walmart',
        'suppliers_PID' : sku,
        'local_PID' : sku,
        'itemproduct':  obtain_product(sku),
        'price_base': clean_price(extract_variables(fd,'currentItemPrice')),
        'online_avail':extract_variables(fd,'isBuyableOnWWW'),
        'local_avail':extract_variables(fd,'isBuyableInStore'), 
    }
    
    return itemdict


def check_online_price(sku):
    fullproductpage = request_fullproduct_page(sku)
    
    index1 = fullproductpage.find('var DefaultItem =')
    index2 = fullproductpage[index1:].find('</script>')
    fd = fullproductpage[index1:index1+index2]     
    
    return extract_variables(fd,'currentItemPrice')

def check_online_avail(sku):
    fullproductpage = request_fullproduct_page(sku)
    
    index1 = fullproductpage.find('var DefaultItem =')
    index2 = fullproductpage[index1:].find('</script>')
    fd = fullproductpage[index1:index1+index2]     
    
    return extract_variables(fd,'isInStock')

def check_local_price(sku):
    return None  # not implemented

def check_walmart_instore(suppliers_PID,MY_ZIP,Miles,key=None):
    ''' check walmart in store stock'''
    fd_instorecheck = request_inventory_page(suppliers_PID,MY_ZIP,Miles)
    #print fd_instorecheck
    
    inventory = []
    #print soup_instorecheck
    for store in fd_instorecheck.find('div', {'class':'container_nopadding'}).findAll('table',{'class':'store'}):
        #print store
        info = store.findAll('td')
        avil = info[0].string.strip()
        store_info = info[1].find('span').string.strip().split('#')
        store_name = store_info[0].strip()
        store_num = store_info[1].strip()
        store_address = info[2].string.strip()
        #print info[3]
        zipcode = info[3].contents[4].string.strip()
        
        inventory.append({'store_name':store_name,
                          'num':store_num,
                          'store_address':store_address,
                          'availbility':avil,
                          'zipcode':zipcode,'availcode':walmart_avail_encode(avil)})
    return inventory

def check_local_avail_listset(supplier_PID,ziplist,keytype='num'):
    ''' check the instore availbility for given queryset'''
    Miles = 100
    avail_store_dict = loop_check(ziplist,check_walmart_instore,supplier_PID,Miles,keytype='num')
    return avail_store_dict

def check_local_avail_queryset(supplier_PID,queryset,keytype='num'):
    storelist,input = data_prep(queryset,keytype)
    availdata = check_local_avail_listset(supplier_PID,input)    
    return storelist,availdata


if __name__ == '__main__':
    
    #res = obtain_supply('20607288')#20573252')
    supply = obtain_supply('20573260')
    #price  = check_online_price('20607288')
    #avail = check_online_avail('20607288')
    #res = check_walmart_instore('15739136','32826','100')
    #res = check_local_avail_listset('15779542',[('890','32826','890')])
    #print price,avail
    print supply
    print 1