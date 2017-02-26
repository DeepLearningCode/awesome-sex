# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'cutd'
__mtime__ = '2017/1/21'
# 无他 唯手熟尔
"""

import time
import requests
from bs4 import BeautifulSoup

start_url = "http://www.jiuseteng55.com/html/videos/guochandianying/"
vhost = "http://www.jiuseteng55.com"
# 九色腾
start_bs = BeautifulSoup(requests.get(start_url).content,"lxml")
# root = etree.HTML(requests.get(start_url).content)
# items = root.xpath("//*[@id=\"menu\"]/div/ul")
# for x in items:
#     print(x)
# 从类型开始
today = time.strftime("%Y-%m-%d", time.localtime())
try:
    for item in start_bs.find("div", {"class": "subnav list-group"}).find_all('a'):
        if 'vip专区' in item.text:
            pass
        else:
            item_url = vhost + item.attrs['href']
            item_type = item.text.split(' ')[0]
            alist = BeautifulSoup(requests.get(item_url).content, "lxml").find("div", {"id":'pages'}).find_all("a")
            if len(alist) >1:
                item_num = alist[-2].text
            else:
                item_num = 1
            print(item_type,item_url,item_num)
        try:
            for x in range(1,int(item_num)+1):
                if x == 1:
                    real_url = item_url
                else:
                    real_url = item_url +str(x)+ ".html"
                item_bs = BeautifulSoup(requests.get(real_url).content, "lxml")
                try:
                    for v in item_bs.find_all("div", {"class": "col-lg-3 col-md-3 col-sm-4 col-xs-12"}):
                        # vid = int(v.find("a").attrs["href"].split("/")[-1].replace('.html',''))
                        vname = v.find("img").attrs["alt"].replace("'",'').replace('\t','')
                        adate = v.find_all("span")[1].text
                        vlong = v.find_all("span")[0].text
                        img = v.find("img").attrs["src"]
                        vid0 = v.find('a').attrs['href']
                        vid = '/'+vid0.split('/')[1]+'/'+vid0.split('/')[2]+'/a'+vid0.split('/')[-1]
                        vbs = BeautifulSoup(requests.get(vhost+vid0).content, "lxml")
                        views = int(vbs.find("span", {"class": "num"}).text)
                        zan = int(vbs.find("span", {"id": "like_views"}).text) if int(vbs.find("span", {"id": "like_views"}).text) != 0 else 1
                        cai = int(vbs.find("span", {"id": "dislike_views"}).text) if int(vbs.find("span", {"id": "dislike_views"}).text) != 0 else 1
                        vrate = zan/(zan+cai)
                        # views = int(v.find("span", {"class": "views"}).text.replace(' 次观看',''))
                        sql = "INSERT INTO av (vname,vhost,vid,img,vdate,adate,vlong,vtype,vrate,views) VALUES ('" \
                              + vname + "', '" + vhost + "','" + vid + "','" + img + "','"+ today + "','"+adate+"','"+vlong+"','"+item_type+"',"+"%.2f"%vrate+","+str(views)+\
                              ")ON CONFLICT(vname, vid, vlong) DO UPDATE SET vdate = '"+today+"',adate='"+adate+"',vrate = "+ "%.4f" % vrate+",views="+str(views)+";"
                        print(sql)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
except Exception as e:
    print(e)
