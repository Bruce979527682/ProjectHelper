#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

cdate = datetime.datetime.now().strftime('%Y-%m-%d')
deskpath = GetDesktopPath()
filepath = deskpath + '\\'+ cdate + '-Read'
isExists=os.path.exists(filepath)
if not isExists:
    os.makedirs(filepath)

readfile = open(r''+ deskpath +'\\read.cs','r', encoding='UTF-8')     
lines =readfile.readlines()
clist=[]
for line in lines:
     line = line.lstrip('\ufeff')
     line = line.rstrip('\n')
     line = line.replace('\'','"')
     clist.append('    sb.append(\''+ line +'\'+\'\\n\')'+'\n')

fout = open(filepath + '\\newfile.txt', "w", encoding='utf-8')
fout.writelines(clist)
fout.close()
print('done')