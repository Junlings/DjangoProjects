# -*- coding: utf-8 -*-
import urllib2
import time
import cPickle as pickle
import encodings
from BeautifulSoup import BeautifulSoup 
from django.utils.encoding import smart_unicode, smart_str
import re


from datetime import datetime, timedelta

def request_url(URL):
    page = urllib2.urlopen(URL)
    html = page.read()
    unicode_str = html.decode("GB18030","ignore")
    encoded_str = unicode_str.encode("utf8")
    aa = BeautifulSoup(encoded_str,fromEncoding="GB18030")    
    return aa

def process_detail(url):
    soup = request_url(url)
    region = soup.find("td", {"class":"jiawenzhang-type"})
    regioninfo = region.text
    

    key_list = [
        u"我想买的物品",
        u"单张面值",
        u"可接受价格",
        u"物品新旧要求",
        u"邮寄方式要求",
        u"买卖双方谁承担邮寄损失",
        u"付款方式说明",
        u"广告的有效期",
        u"物品来源",
        u"我的联系方式",
        u"Warranty期限",]
    
    
    
    
    res_dict = {}
    for i in range(0,len(key_list)-1):
        st = key_list[i]+u"(.*?)"+key_list[i+1]
        content = re.findall(st, regioninfo)
        if len(content) > 0:
            contentinput = content[0][content[0].find(':')+1:]
        else:
            contentinput = ''
        res_dict[key_list[i]] = contentinput

    return res_dict


def process_entry(soup):
    res_dict = {}
    for entry in soup.findAll("item"):    
        temp = {'title': entry.contents[1].text,
                'key': entry.attrs[0][1].split('/')[-1].split('.')[0],
                'author':entry.contents[6].text,
                'updated':datetime.strptime(entry.contents[8].text, "%Y-%m-%dT%H:%M:%S-04:00")  ,
                'link':entry.attrs[0][1]}
        res_dict.update({temp['key'] : temp})
    return res_dict

def process(url):
    soup = request_url(url)
    return process_entry(soup)
    
if __name__ == '__main__':
    
    #res = process('http://www.mitbbs.com/board_rss/FleaMarket.xml')
    #res_dict = process_detail("http://www.mitbbs.com/article_t/FleaMarket/33233444.html")
    #res_dict = process_detail("http://www.mitbbs.com/article_t/FleaMarket/33233517.html")
    for key,value in res_dict.items():
        print key,value
    print 1
    
        