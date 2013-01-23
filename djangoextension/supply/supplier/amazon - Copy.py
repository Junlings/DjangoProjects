from amazonproduct import *
from BeautifulSoup import BeautifulSoup

#=========block functions
def request_product_page(ASIN):
    """ make request to page and scrape only the body-footer region """
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.0.13) Gecko/2009073021 Firefox/3.0.13')]

    url = "http://www.amazon.com/gp/aw/d/%s/" % str(ASIN)
    fd = opener.open(url).read()
    index1 = fd.find('<div id="divsinglecolumnminwidth"')
    index2 = fd.find('<div id="navFooter">')
    return fd[index1:index2]



def get_buyingbox(productpage):
    index1 = productpage.find('<form id="handleBuy')
    index2 = productpage[index1:].find('<script')
    #print productpage
    print productpage[index1:index2+index1]
    return BeautifulSoup(productpage[index1:index2+index1])  
    
def get_longname(buyingbox):
    #print buyingbox
    return buyingbox.find('span',{"id":"btAsinTitle"}).text  
    
def check_amazon(ASIN):
    ''' Check amazon.com online inventory and price using the AWS service'''
    
    AWS_KEY = 'AKIAJ5WBUQP6NX3GEFOQ'
    SECRET_KEY = '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'
    AssociateTag='fprime-20'
    
    # call amazonproduct API wrapper
    api = API(AWS_KEY, SECRET_KEY, 'us',AssociateTag)

    # retrive ASIN from model object
    #content = api.item_lookup(ASIN,ResponseGroup='Large')
    content = api.item_lookup(ASIN,ResponseGroup='Large')
    item = content.Items.Item
    
    # return 
    return item


if __name__ == '__main__':
    ASIN = 'B004Z7H07K'
    res = check_amazon(ASIN)

    
    print 1