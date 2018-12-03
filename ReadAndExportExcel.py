#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd #读
import xlwt #写
workbook = xlrd.open_workbook(r'basetable.xlsx')
table = workbook.sheet_by_index(0)
rows = table.row_values(0)

print("end;")