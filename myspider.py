#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import re
import urllib.parse
import urllib.request
import urllib
import time
import _datetime
import datetime
import random
import xlwt
from selenium import webdriver
driver = webdriver.PhantomJS(executable_path='C:\\Users\\vzan\\Downloads\\phantomjs.exe')
from bs4 import BeautifulSoup
import json

#获得html文本
def getHTMLText(url): 
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.8.0.16453')
        req.add_header('Connection','keep-alive')       
        resp = urllib.request.urlopen(req)
        html = resp.read().decode("utf-8")
        
        return html
    except Exception as e:
        print(e)

def getLinkList(url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    list = soup.find_all('a',href=re.compile("schoolhtm/schoolTemple"))
    for l in list:
        str = "http://gkcx.eol.cn"+l.attrs['href'].strip()
        if str not in hrefs:
            hrefs.append(str)

imglinklist=[]
def handleImg():
    for index in range(1,100):
        getjson = getHTMLText('https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E6%98%8E%E6%98%9F%E5%9B%BE%E7%89%87&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=&z=&ic=&hd=&latest=&copyright=&word=%E6%98%8E%E6%98%9F%E5%9B%BE%E7%89%87&s=&se=&tab=&width=&height=&face=&istype=&qc=&nc=&fr=&expermode=&force=&pn='+str(index)+'&rn=30&gsm=5a&1559616409598=')
        jsondata = json.loads(getjson)
        for data in jsondata['data']:
            if 'thumbURL' in data.keys():
                path = data['thumbURL']
                imglinklist.append(path)
        time.sleep(1)
    print('get link end')

def downloadImgs():
    for imgPath in imglinklist:        
        try:
            pathname = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100000, 1000000))
            f = open('D:\\Images\\'+ pathname +".jpg", 'wb')
            f.write((urllib.request.urlopen(imgPath)).read())
            f.close()
        except Exception as e:
            print(imgPath+" error")    

    print("All Done!")


#程序主体区域
if __name__ == "__main__":
    b = True
    if b:
        
        try:            
            handleImg()
            downloadImgs()
            #html = getHTMLText('https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%C3%F7%D0%C7%CD%BC%C6%AC&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=111111')
            #html = getLinkList('https://image.baidu.com/search/index?tn=baiduimage&ct=201326592&lm=-1&cl=2&ie=gb18030&word=%C3%F7%D0%C7%CD%BC%C6%AC&fr=ala&ala=1&alatpl=adress&pos=0&hs=2&xthttps=111111')
            #html = getHTMLText('https://www.baidu.com/index.php')
        except Exception as ex:
            print("获取链接发生未知异常！："+ ex.args)
        
        print("结束！")
    else:
        pass