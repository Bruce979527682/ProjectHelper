#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
file = open("./area.txt",'r', encoding='UTF-8')
lines = file.readlines()
fout = open('./insert.txt','w')
provinces = []
citys = []
areas = []
for line in lines:
    strs = line.strip().split(' ')
    if len(strs) > 1:
        code = strs[0]
        name = strs[1]    
        if('0000' == code[2:6]):
            provinces.append(line.strip())
        if('0000' != code[2:6] and '00' == code[4:6]):
            citys.append(line.strip())
        if('0000' != code[2:6] and '00' != code[4:6]):
            areas.append(line.strip())

for province in provinces:
    print(province)
    clists = list(filter(lambda x:x[0:2]==province[0:2],citys))
    if len(clists) > 1：
        for city in clists:
            print(city)
            alists = list(filter(lambda x:x[0:4]==city[0:4],areas))
            for area in alists:
                print(area)
    else:
        clists = list(filter(lambda x:x[0:2]==province[0:2],areas))

print("end;")

file.close()
fout.close()