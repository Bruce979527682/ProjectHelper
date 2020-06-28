#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd  # 读
import xlwt  # 写
import math
import datetime
import os

def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')

deskPath = GetDesktopPath()

cdate = datetime.datetime.now().strftime('%Y-%m-%d')

filepath = deskPath + '\\' +cdate
isExists=os.path.exists(filepath)
if not isExists:
    os.makedirs(filepath)

workbook = xlrd.open_workbook(r''+deskPath+'\\shop.xlsx')
excels = workbook.sheet_by_index(0)
tables = {}
tnames = {}
key = ''
for rows in excels._cell_values:
    if rows != excels._cell_values[0]:
        if rows[0] == '':
            tables[key].append(rows)
        else:
            key = rows[1]
            tnames.setdefault(key, rows[0])
            tables.setdefault(key, [rows])
i = 0

def entity(rows, key):
    sb = []
    sb.append('using SqlSugar;'+'\n')
    sb.append('using System;'+'\n')
    sb.append(''+'\n')
    sb.append('namespace Entity.Api'+'\n')
    sb.append('{'+'\n')
    sb.append('    /// <summary>'+'\n')
    sb.append('    /// ' + tnames[key]+'表\n')
    sb.append('    /// </summary>'+'\n')
    sb.append('    public class ' + key + '\n')
    sb.append('    {'+'\n')

    for row in rows:
        sb.append('        /// <summary>'+'\n')
        sb.append('        /// ' + row[2]+'\n')
        sb.append('        /// </summary>'+'\n')
        if row[6] == 'y' and row[7] == 'y':
            sb.append('        [SugarColumn(IsPrimaryKey = true, IsIdentity = true)]'+'\n')
        elif row[6] == 'y':
            sb.append('        [SugarColumn(IsPrimaryKey = true)]'+'\n')
        elif row[7] == 'y':
            sb.append('        [SugarColumn(IsIdentity = true)]'+'\n')        
        if row[11] != '':
            if str(row[4]) == 'varchar':
                sb.append('        public string ' + str(row[3]) + ' { get; set; } = ' + str(row[11]) + ';'+'\n')
            elif str(row[4]) == 'datetime':
                sb.append('        public DateTime ' +  str(row[3]) + ' { get; set; } = ' + str(row[11]) + ';'+'\n')
            elif str(row[4]) == 'text':
                sb.append('        public string ' +  str(row[3]) + ' { get; set; } = ' + str(row[11]) + ';'+'\n')
            elif str(row[4]) == 'int':
                sb.append('        public int ' +  str(row[3]) + ' { get; set; } = ' + str(int(row[11])) + ';'+'\n')
            else:
                sb.append('        public ' + str(row[4]) + ' ' + str(row[3]) + ' { get; set; } = ' + str(row[11]) + ';'+'\n')
        else:
            if str(row[4]) == 'varchar':
                sb.append('        public string ' + str(row[3]) + ' { get; set; }'+'\n')
            elif str(row[4]) == 'datetime':
                sb.append('        public DateTime ' + str(row[3]) + ' { get; set; }'+'\n')
            elif str(row[4]) == 'text':
                sb.append('        public string ' +  str(row[3]) + ' { get; set; }'+'\n')
            elif str(row[4]) == 'int':
                sb.append('        public int ' +  str(row[3]) + ' { get; set; }'+'\n')
            else:
                sb.append('        public ' +  str(row[4]) + ' ' + str(row[3]) + ' { get; set; }'+'\n')
    sb.append(''+'\n')
    sb.append('        #region 扩展字段'+'\n')
    sb.append(''+'\n')
    sb.append('        //[SugarColumn(IsIgnore = true)]'+'\n')
    sb.append('        //public string AddTimeStr { get; set; }'+'\n')
    sb.append(''+'\n')
    sb.append('        #endregion 扩展字段'+'\n')
    sb.append(''+'\n')
    sb.append('    }'+'\n')
    sb.append('}'+'\n')

    fout = open(filepath + '/'+key+'.cs', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def bll(rows, key):
    sb = []
    sb.append('using System;'+'\n')
    sb.append('using DAL.Base;'+'\n')
    sb.append('using Entity.City;'+'\n')
    sb.append('using System.Collections.Generic;'+'\n')
    sb.append('using MySql.Data.MySqlClient;'+'\n')
    sb.append('using System.Data;'+'\n')
    sb.append('namespace BLL.City'+'\n')
    sb.append('{'+'\n')
    sb.append('    /// <summary>'+'\n')
    sb.append('    /// ' + tnames[key]+'表BLL\n')
    sb.append('    /// </summary>'+'\n')
    sb.append('    public class ' + key + 'BLL: BaseMySql<' + key + '>\n')
    sb.append('    {'+'\n')
    sb.append('        private string _cacheKey = "'+key+'_{0}";'+'\n')
    sb.append('        #region 单例模式'+'\n')
    sb.append('        private static ' + key + 'BLL _singleModel;'+'\n')
    sb.append('        private static readonly object SynObject = new object();'+'\n')
    sb.append('        '+'\n')
    sb.append('        private ' + key + 'BLL()'+'\n')
    sb.append('        {'+'\n')
    sb.append('            '+'\n')
    sb.append('        }'+'\n')
    sb.append('        '+'\n')
    sb.append('        public static ' + key + 'BLL SingleModel'+'\n')
    sb.append('        {'+'\n')
    sb.append('            get'+'\n')
    sb.append('            {'+'\n')
    sb.append('                if (_singleModel == null)'+'\n')
    sb.append('                {'+'\n')
    sb.append('                    lock (SynObject)'+'\n')
    sb.append('                    {'+'\n')
    sb.append('                        if (_singleModel == null)'+'\n')
    sb.append('                        {'+'\n')
    sb.append('                            _singleModel = new ' + key + 'BLL();'+'\n')
    sb.append('                        }'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                }'+'\n')
    sb.append('                return _singleModel;'+'\n')
    sb.append('            }'+'\n')
    sb.append('        }'+'\n')
    sb.append('        #endregion 单例模式'+'\n')    
    sb.append('        '+'\n')
    sb.append('        /// <summary>'+'\n')
    sb.append('        /// 获取' + tnames[key] +'数据'+'\n')
    sb.append('        /// </summary>'+'\n')
    sb.append('        /// <param name="cityInfoId">同城ID</param>'+'\n')
    sb.append('        /// <param name="pageIndex"></param>'+'\n')
    sb.append('        /// <param name="pageSize"></param>'+'\n')
    sb.append('        /// <returns></returns>'+'\n')
    sb.append('        public List<' + key + '> Get' + key + 'List(int cityInfoId, int pageIndex = 1, int pageSize = 10)'+'\n')
    sb.append('        {'+'\n')
    sb.append('            var where = $"Status<>-4";'+'\n')
    sb.append('            var totalCount = 0;'+'\n')
    sb.append('            return GetList(where, ref totalCount, pageSize, pageIndex);'+'\n')
    sb.append('        }'+'\n')
    sb.append('        '+'\n')
    sb.append('        /// <summary>'+'\n')
    sb.append('        /// 修改' + tnames[key] +'状态'+'\n')
    sb.append('        /// </summary>'+'\n')
    sb.append('        /// <param name="cityInfoId">同城ID</param>'+'\n')
    sb.append('        /// <param name="id"></param>'+'\n')
    sb.append('        /// <param name="status">状态</param>'+'\n')
    sb.append('        /// <returns></returns>'+'\n')
    sb.append('        public bool UpdateStatus(int id, int status)'+'\n')
    sb.append('        {'+'\n')
    sb.append('            var model = GetModel(id);'+'\n')
    sb.append('            if (model != null)'+'\n')
    sb.append('            {'+'\n')
    sb.append('                model.Status = status;'+'\n')
    sb.append('                return Update(model, new string[] { "Status" });'+'\n')
    sb.append('            }'+'\n')
    sb.append('            return false;'+'\n')
    sb.append('        }'+'\n')
    sb.append(''+'\n')    
    sb.append(''+'\n')
    sb.append('    }'+'\n')
    sb.append('}'+'\n')
    fout = open(filepath + '/'+key+'BLL.cs', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def database(rows):
    sb = []
    sb.append('CREATE TABLE `' + key + '` ('+'\n')

    for row in rows:
        if row[4] == 'int' or row[4] == 'varchar':
            if row[4] == 'int' and row[7] == 'y':
                sb.append('  `' + row[3] + '` ' + row[4] + '(' + str(int(row[5])) + ')  ' + (
                    'NOT NULL' if row[9] == 'y' else '') + ' ' + ('AUTO_INCREMENT' if row[7] == 'y' else '')+' COMMENT \''+ row[2] +'\',' + '\n')
            else:
                sb.append('  `' + row[3] + '` ' + row[4] + '(' + str(int(row[5])) + ') ' + (
                    'NOT NULL' if row[9] == 'y' else '') + 'COMMENT \''+ row[2] +'\',' + '\n')
        else:
            sb.append('  `' + row[3] + '` ' + row[4] + ' ' +
                      ('NOT NULL' if row[9] == 'y' else '') + 'COMMENT \''+ row[2] +'\','+'\n')
    pkeycol = list(filter(lambda x: x[6] == 'y', rows))
    indexcol = list(filter(lambda x: x[8] == 'y', rows))
    ukeycol = list(filter(lambda x: x[10] == 'y', rows))
    if pkeycol != None and len(pkeycol) > 0:
        if len(indexcol) > 0:
            sb.append('  PRIMARY KEY (`' + pkeycol[0][3] + '`),'+'\n')
        else:
            sb.append('  PRIMARY KEY (`' + pkeycol[0][3] + '`)'+'\n')
    else:
        print( rows[0][0] + 'PRIMARY KEY null')
    ikey = []
    for ic in indexcol:
        ikey.append(' `' + ic[3] + '`')
    ukey = []
    for uc in ukeycol:
        ukey.append(' `' + uc[3] + '`')
    if ukeycol != None:
        sb.append('  UNIQUE KEY `Key_Unique` (' + str(ukey).replace('[', '').replace(']', '').replace("'", '')+') USING BTREE,'+'\n')
    sb.append('  KEY `Key_Index` (' + str(ikey).replace('[', '').replace(']', '').replace("'", '')+')'+'\n')
    sb.append(') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'+'\n')
    fout = open(filepath + '/'+key+'-database.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

for key in tables:
    items = tables[key]
    # entity
    entity(items, key)
    
    # bll
    bll(items, key)
        
    # database
    database(items)

print('end')
