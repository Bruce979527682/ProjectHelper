#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
import os
import pandas as pd

deskPath = os.path.join(os.path.expanduser("~"), 'Desktop')

import csv
    
with open(deskPath+'\\ExportData.csv','r',encoding='UTF-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    dates = []
    cols = []
    framedate = {}
    allrow = []
    for row in csv_reader:
        allrow.append(row)
        if row[0] != '' and row[0] not in dates:
            dates.append(row[0])
        if row[1] != '' and row[1] not in cols:
            cols.append(row[1])
            framedate[row[1]] = {}
    for row1 in allrow:
        framedate[row1[1]][row1[0]] = row1[2]
        
    df = pd.DataFrame(framedate, columns=cols, index=dates)
    # df = pd.DataFrame(framedate)
    df.fillna(0)
    df.to_excel(deskPath+'\\2018至现在同城流水信息.xls')
print('end')