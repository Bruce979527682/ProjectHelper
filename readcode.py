#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os

cdate = datetime.datetime.now().strftime('%Y-%m-%d')
filepath = 'C:/Users/EDZ/Desktop/'+cdate
isExists=os.path.exists(filepath)
if not isExists:
    os.makedirs(filepath)

# csvfile = open(r'accounts.csv','r', encoding='UTF-8')
readfile = open(r'C:\work\Friend-0817\User.MiniSNS\Views\Friend\activitylist.cshtml','r', encoding='UTF-8')     
lines =readfile.readlines()
clist=[]
for line in lines:
     line = line.lstrip('\ufeff')
     line = line.rstrip('\n')
     line = line.replace('\'','"')
     clist.append('    sb.append(\''+ line +'\'+\'\\n\')'+'\n')

fout = open(filepath + '/newfile.txt', "w", encoding='utf-8')
fout.writelines(clist)
fout.close()
print('done')