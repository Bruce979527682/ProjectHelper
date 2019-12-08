#!/usr/bin/python
# -*- coding: UTF-8 -*-
import csv
with open('./test.csv','r',encoding='UTF-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        print(row)
        print(row[0])