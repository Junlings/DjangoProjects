from amazonproduct import *
from BeautifulSoup import BeautifulSoup

from uti import clean_price

def config():
    AWS_KEY = 'AKIAJ5WBUQP6NX3GEFOQ'
    SECRET_KEY = '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'
    AssociateTag='fprime-20'
    
    # call amazonproduct API wrapper
    api = API(AWS_KEY, SECRET_KEY, 'us',AssociateTag)
    
    return api    
    
def item_lookup(api,ASIN,**qargs):
    ''' Check amazon.com online inventory and price using the AWS service'''
    
    content = api.item_lookup(ASIN,ResponseGroup='Large',**qargs)
    item = content.Items.Item
    return item


def browse_node_lookup(nodeid):
    AWS_KEY = 'AKIAJ5WBUQP6NX3GEFOQ'
    SECRET_KEY = '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'
    AssociateTag='fprime-20'
    
    # call amazonproduct API wrapper
    api = API(AWS_KEY, SECRET_KEY, 'us',AssociateTag)
    

def get_manufacture(ItemAttributes):
    return ItemAttributes.Manufacturer.pyval

def get_agelimits(ItemAttributes):
    """ get manufacture suggested age range"""
    max = ItemAttributes.ManufacturerMaximumAge.pyval
    max_unit = ItemAttributes.ManufacturerMaximumAge.attrib['Units']
    min= ItemAttributes.ManufacturerMinimumAge.pyval
    min_unit =ItemAttributes.ManufacturerMinimumAge.attrib['Units']
    return [min,min_unit,max,max_unit]
    
def get_title(ItemAttributes):
    return ItemAttributes.Title.pyval
    
def get_productGroup(ItemAttributes):
    return ItemAttributes.ProductGroup.pyval

def get_UPC(ItemAttributes):
    return ItemAttributes.UPC.pyval    
    
def get_brand(ItemAttributes):
    return ItemAttributes.Brand.pyval   

def get_modelid(ItemAttributes):
    return ItemAttributes.Model.pyval


def get_images(ImageSets):
    bigimagepath = ImageSets.ImageSet.LargeImage.URL.pyval
    smallimagepath = ImageSets.ImageSet.SmallImage.URL.pyval
    
    return {'small':smallimagepath,'large':bigimagepath}

def get_baseprice(Offers):
    if Offers.TotalOffers.pyval != 0:
        return clean_price(Offers.Offer.OfferListing.Price.FormattedPrice.pyval)
    else:
        return None
    
def obtain_product(ASIN):
    api = config()
    res = api.item_lookup(ASIN,ResponseGroup='Medium')
    ItemAttributes = res.Items.Item.ItemAttributes
    ImageSets = res.Items.Item.ImageSets
    product = {
        'longname' : get_title(ItemAttributes),
        'shortname' : None,
        'modelid' : get_modelid(ItemAttributes),
        'brand':get_brand(ItemAttributes),
        'upc':get_UPC(ItemAttributes)
        }
    
    product.update(
        {
        'manufacturer' : {'name':get_manufacture(ItemAttributes)},
        'mainimagepath' : get_images(ImageSets)['small'] ,
    })
    
    return product

def obtain_supply(ASIN):
    api = config()
    res = api.item_lookup(ASIN,ResponseGroup='OfferFull',Condition='New',MerchantId='Amazon')
    Offers = res.Items.Item.Offers
    itemdict = {
        'suppliers' : {'name':'Amazon','platform':'Amazon'},
        'suppliers_PID' : ASIN,
        'itemproduct':  obtain_product(ASIN),
        'price_base': get_baseprice(Offers),
        'online_avail':True,
        'local_avail':False,
    }
    
    return itemdict

if __name__ == '__main__':
    ASIN = 'B0051VVOB2' #'B004Z7H07K'
    api = config()
    
    res = api.item_lookup(ASIN,ResponseGroup='OfferFull,Medium',Condition='New',MerchantId='All')
    #print get_manufacture(res.Items.Item.ItemAttributes)
    #print get_title(res.Items.Item.ItemAttributes)
    #print get_productGroup(res.Items.Item.ItemAttributes)
    #print get_UPC(res.Items.Item.ItemAttributes)
    #res = get_agelimits(res.Items.Item.ItemAttributes)
    #print get_images(res.Items.Item.ImageSets)
    
    #print obtain_product(ASIN)
    print obtain_supply(ASIN)
    print res
