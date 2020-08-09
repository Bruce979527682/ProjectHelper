#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os
import json

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

cdate = datetime.datetime.now().strftime('%Y-%m-%d')
deskpath = GetDesktopPath()
filepath = deskpath + '\\'+ cdate + '-Read'
isExists=os.path.exists(filepath)
if not isExists:
    os.makedirs(filepath)

readfile = open(r''+ deskpath +'\\LAreaData2.js','r', encoding='UTF-8')   
type = 1
if type == 1:
    lines =readfile.read()
    lines = lines.encode('utf-8').decode('unicode_escape') # unicode转中文
    str_new = lines[14:-2] #截取字符串
    str_new = json.loads(str_new) # 字符串转json
    str_new = json.dumps(str_new, ensure_ascii=False, indent=4, separators=(',', ': ')) # josn转字符串加格式化
    fout = open(filepath + '\\newfile1.js', "w", encoding='utf-8')
    fout.write(str_new)
    fout.close()
    
else:
    lines =readfile.readlines()
    newlines = []
    for index,line in lines:
        newstr = ''
        if index == 0:
            newstr = line[26:-1]
        elif index == 1:
            newstr = line
        else:
            newstr = line
        newstr = newstr.encode('utf-8').decode('unicode_escape') # unicode转中文
        newstr = json.dumps(newstr, ensure_ascii=False, indent=4, separators=(',', ': ')) # josn转字符串加格式化
        newlines
    fout = open(filepath + '\\newfile2.js', "w", encoding='utf-8')
    fout.writelines(newlines)
    fout.close()   

print('done')