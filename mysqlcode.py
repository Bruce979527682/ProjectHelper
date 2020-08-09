#!/usr/bin/python
#coding:UTF-8

import requests
from bs4 import BeautifulSoup
import MySQLdb

conn=MySQLdb.connect(host='192.168.30.124',user='root',passwd='root',db='test',charset="utf8") #创建数据库的连接，里面可以指定参数(用户名、密码、主机等信息)
cur=conn.cursor() #通过获取的数据库连接conn下的cursor()方法来创建游标

link="http://www.santostang.com/"
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
r=requests.get(link,headers=headers)

soup=BeautifulSoup(r.text,"lxml")
title_list=soup.find_all('h1',class_="post-title")
for eachone in title_list:
    url=eachone.a['href']
    title=eachone.a.text.strip()
    cur.execute("INSERT INTO urls (url,content) VALUES (%s,%s)",(url,title))#执行，写入纯SQL语句

cur.close()#关闭光标
conn.commit()#在提交事物，在向数据库插入一条数据时必须要有这个方法，否则数据不会被真正的插入。
conn.close()#关闭数据库连接
