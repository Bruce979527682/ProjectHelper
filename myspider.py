#!/usr/bin/python3
# -*- coding:utf-8 -*-
import sys
import re
import urllib.parse
import urllib.request
import urllib
import time
import _datetime
import xlwt
from selenium import webdriver
driver = webdriver.PhantomJS(executable_path='C:\\Users\\vzan\\Downloads\\phantomjs.exe')
from bs4 import BeautifulSoup

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

#程序主体区域
if __name__ == "__main__":
    b = True
    if b:
        
        try:
            #html = getHTMLText('http://image.baidu.com/search/index?word=%E4%BA%BA&ct=201326592&cl=2&nc=1&lm=-1&st=-1&tn=baiduimage&istype=2&fm=index&pv=&z=0&ie=utf-8')
            html = getLinkList('http://image.baidu.com/search/index?word=%E4%BA%BA&ct=201326592&cl=2&nc=1&lm=-1&st=-1&tn=baiduimage&istype=2&fm=index&pv=&z=0&ie=utf-8')
            #html = getHTMLText('https://www.baidu.com/index.php')
        except Exception:
            print("获取链接发生未知异常！")
        
        print("结束！")
    else:
        pass