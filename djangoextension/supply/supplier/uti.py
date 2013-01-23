""" this is the abstract class defination of supplier class """

import time
Debug = True

def stlog(msg):
    if Debug:
        print msg
    else:
        pass
    
def clean_price(price):
    price = str(price).strip()
    if '$' in price:
        price = price[1:]
    
    if '.' in price:
        price_1,price_2 = price.split('.')
        price = price_1 +'.' +price_2[0:2]
    return price

def escapeSpecialCharacters (text, characters ):
    for character in characters:
        text = text.replace( character, '')
    return text

def data_prep(storequery,keytype='zipcode'):
    search_storelist = list(storequery)
    search_input = []
    
    for i in range(0,len(search_storelist)):
        store = search_storelist[i]
        if keytype == 'zipcode':  # only zipcode as key
            search_input.append((store.id,store.zipcode,store.zipcode))
        elif keytype == 'num':
            search_input.append((store.id,store.zipcode,store.num))
        elif keytype == 'name':
            search_input.append((store.id,store.zipcode,store.name))
        else:
            search_input.append((store.id,store.zipcode,store.id))
    return search_storelist,search_input


def loop_check(storelist,check_fun,supplier_PID,Miles,keytype,tsleep=0.3):
    
    #print storelist
    #print check_fun
    
    avail_store_dict = {}
    keyvaluelist = []
    n_request = 0
    skiplist = []
    
    msg = "===================Start checking store for item %s================" % supplier_PID
    stlog(msg)
    for store in storelist:
        id = store[0]
        zipcode = store[1]
        key = store[2]
        
   
        avail_store_dict[key] = {'availcode':None,'id':id,'zipcode':zipcode,keytype:key}  # 
        keyvaluelist.append(key)        
            
    for store in storelist:
        id = store[0]
        zipcode = store[1]
        key = store[2]      
        
        if key in skiplist:
            msg = 'Skip request->>> due to skipkey list:' + key
            stlog(msg)
            continue
        
        # check if already detectedm if so, move to next zip in the ziplist
        if avail_store_dict[key]['availcode'] != None:
            msg = 'Skip Store with keyname:' + key
            stlog(msg)
            continue
        
        n_request += 1
        msg = 'processing request number %s Store key %s' % (str(n_request),store)
        stlog(msg)
        
        MY_ZIP = zipcode
        
        avail_store = check_fun(supplier_PID,MY_ZIP,Miles)
        '''
        try:
            time.sleep(tsleep)
            # here may need to check if the first returned store is the store with same zip
            avail_store = check_fun(supplier_PID,MY_ZIP,Miles)
            msg = 'Get availbility information'
            print avail_store
            stlog(msg)
            
        except:
            msg = 'check error happended'
            stlog(msg)
            
            continue
        '''
        for store in avail_store:
            
            if keytype not in store.keys():
                msg = '%s not availale in rearch results' % keytype
                stlog(msg)
                continue
            else:
                keyvalue = store[keytype]
                
                
            if  keyvalue in keyvaluelist:

                if avail_store_dict[keyvalue]['availcode'] == None:  # have not been updated
                    # update info
                    msg = 'Updating key %s :avail %s' % (keyvalue,store['availcode'])
                    stlog(msg)
                    avail_store_dict[keyvalue].update(store)
                    
                    #if avail_store_dict[keyvalue]['availcode'] == None:
                    #    print 'check fail,key=', key, avail_store_dict[key]
                else:
                    # already updated
                    skiplist.append(keyvalue)
                    msg = 'skip key= ' + keyvalue
                    stlog(msg)
            else:
                msg = ' %s not in the keyvaluelist' % keyvalue
                stlog(msg)
                #stlog(keyvalue)
                #stlog(keyvaluelist)
        
    msg = 'process total %s requests' %  n_request
    stlog(msg)
    
    
    avail_dict = []
    for key,value in avail_store_dict.items():
        avail_dict.append(value)
        
    
    return avail_dict 