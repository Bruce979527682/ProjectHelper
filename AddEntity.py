#!/usr/bin/python
# -*- coding: UTF-8 -*-
import xlrd #读
import xlwt #写
import math

fout = open('C:/Users/EDZ/Desktop/basetable.txt','w')

workbook = xlrd.open_workbook(r'C:\Users\EDZ\Desktop\basetable.xlsx')
excels = workbook.sheet_by_index(0)
tables={}
tnames={}
key=''
for rows in excels._cell_values:
    if rows != excels._cell_values[0]:
        if rows[0] == '':
            tables[key].append(rows)
        else:            
            key = rows[1]
            tnames.setdefault(key,rows[0])
            tables.setdefault(key,[rows])
strings=[]
i=0
for i in range(0,len(tables)):    
    for key in tables:
        #entity
        strings.append('using Entity.Base;'+'\n')
        strings.append('using System;'+'\n')
        strings.append('using Utility;'+'\n')
        strings.append('namespace Entity.MiniSNS.Friend'+'\n')
        strings.append('{'+'\n')
        strings.append('    /// <summary>'+'\n')
        strings.append('    /// '+ tnames[key]+'表\n')
        strings.append('    /// </summary>'+'\n')
        strings.append('    [Serializable]'+'\n')
        strings.append('    [SqlTable(dbEnum.QLWL)]'+'\n')
        strings.append('    public class '+ key +'\n')
        strings.append('    {'+'\n')
        items = tables[key]
        for row in items:
            strings.append('        /// <summary>'+'\n')
            strings.append('        /// '+ row[2]+'\n')
            strings.append('        /// </summary>'+'\n')
            if row[6] == 'y' and row[7] == 'y':
                strings.append('        [SqlField(IsPrimaryKey = true, IsAutoId = true)]'+'\n')
            elif row[6] == 'y':
                strings.append('        [SqlField(IsPrimaryKey = true)]'+'\n')
            elif row[7] == 'y':
                strings.append('        [SqlField(IsAutoId = true)]'+'\n')
            else:
                strings.append('        [SqlField]'+'\n')
            if row[11] != '':
                if str(row[4]) == 'varchar':
                    strings.append('        public string '+ str(row[3]) +' { get; set; } = '+ str(row[11]) +';'+'\n')
                elif str(row[4]) == 'datetime':
                    strings.append('        public DateTime '+ str(row[3]) +' { get; set; } = '+ str(row[11]) +';'+'\n')
                else:
                    strings.append('        public '+ str(row[4]) +' '+ str(row[3]) +' { get; set; } = '+ str(row[11]) +';'+'\n')
            else:
                if str(row[4]) == 'varchar':
                    strings.append('        public string '+ str(row[3]) +' { get; set; }'+'\n')
                elif str(row[4]) == 'datetime':
                    strings.append('        public DateTime '+ str(row[3]) +' { get; set; }'+'\n')
                else:
                    strings.append('        public '+ str(row[4]) +' '+ str(row[3]) +' { get; set; }'+'\n')            
        strings.append('    }'+'\n')
        strings.append('}'+'\n')

        strings.append('\n')
        strings.append('\n')
        strings.append('\n')
        #bll
        strings.append('using DAL.Base;'+'\n')
        strings.append('using Entity.MiniSNS.Friend;'+'\n')
        strings.append('using System.Collections.Generic;'+'\n')
        strings.append('namespace BLL.MiniSNS.Friend'+'\n')
        strings.append('{'+'\n')
        strings.append('    /// <summary>'+'\n')
        strings.append('    /// '+ tnames[key]+'表BLL\n')
        strings.append('    /// </summary>'+'\n')
        strings.append('    public class '+ key +'BLL: BaseMySql<'+ key +'>\n')
        strings.append('    {'+'\n') 
        strings.append('        public '+key+' GetModelByCache(int id)'+'\n')
        strings.append('        {'+'\n')
        strings.append('            string key = string.Format(FCacheKey.'+key+'IdKey, id);'+'\n')
        strings.append('            var model = RedisUtil.Get<'+key+'>(key);'+'\n')
        strings.append('            if (model != null)'+'\n')
        strings.append('            {'+'\n')
        strings.append('                return model;'+'\n')
        strings.append('            }'+'\n')
        strings.append('            else'+'\n')
        strings.append('            {'+'\n')
        strings.append('                model = GetModel(id);'+'\n')
        strings.append('                if (model != null)'+'\n')
        strings.append('                {'+'\n')
        strings.append('                    RedisUtil.Set<'+key+'>(key, model);'+'\n')
        strings.append('                }'+'\n')
        strings.append('                return model;'+'\n')
        strings.append('            }'+'\n')
        strings.append('        }'+'\n')
        strings.append('        '+'\n')
        strings.append('        public '+key+' GetModelByCache(int minisnsId,int userId)'+'\n')
        strings.append('        {'+'\n')
        strings.append('            var strWhere = $"MinisnsId={minisnsId} and UserId={userId}";'+'\n')
        strings.append('            string key = string.Format(FCacheKey.'+key+'MinsnsIdKey, minisnsId, userId);'+'\n')
        strings.append('            var model = RedisUtil.Get<'+key+'>(key);'+'\n')
        strings.append('            if (model != null)'+'\n')
        strings.append('            {'+'\n')
        strings.append('                return model;'+'\n')
        strings.append('            }'+'\n')
        strings.append('            else'+'\n')
        strings.append('            {'+'\n')
        strings.append('                model = GetModel(strWhere);'+'\n')
        strings.append('                if (model != null)'+'\n')
        strings.append('                {'+'\n')
        strings.append('                    RedisUtil.Set<'+key+'>(key, model);'+'\n')
        strings.append('                }'+'\n')
        strings.append('                return model;'+'\n')
        strings.append('            }'+'\n')
        strings.append('        }'+'\n')
        strings.append('        '+'\n')
        strings.append('        public bool RemoveCache(int id)'+'\n')
        strings.append('        {'+'\n')
        strings.append('            string key = string.Format(FCacheKey.'+key+'Key, id);'+'\n')
        strings.append('            return RedisUtil.Remove(key);'+'\n')                 
        strings.append('        }'+'\n')
        strings.append('        '+'\n')
        strings.append('        public bool RemoveCache(int minisnsId, int userId)'+'\n')
        strings.append('        {'+'\n')
        strings.append('            string key = string.Format(FCacheKey.'+key+'MinsnsIdKey, minisnsId, userId);'+'\n')
        strings.append('            return RedisUtil.Remove(key);'+'\n')                 
        strings.append('        }'+'\n')
        strings.append('    }'+'\n')
        strings.append('}'+'\n')

        strings.append('\n')
        strings.append('\n')
        strings.append('\n')

        #database
        strings.append('CREATE TABLE `'+ key +'` ('+'\n')
        
        for row in items:
            if row[4] == 'int' or row[4] == 'varchar':
                if row[4] == 'int' and row[7] == 'y':
                    strings.append('  `'+ row[3] +'` '+ row[4] +'('+ str(int(row[5])) +')  '+ ('NOT NULL' if row[9]=='y' else '') +' '+ ('AUTO_INCREMENT' if row[7]=='y' else '')+',' +'\n') 
                else:
                    strings.append('  `'+ row[3] +'` '+ row[4] +'('+ str(int(row[5])) +') '+ ('NOT NULL' if row[9]=='y' else '') + ',' +'\n')
            else:
                strings.append('  `'+ row[3] +'` '+ row[4] +' '+ ('NOT NULL' if row[9]=='y' else '') +','+'\n')
        pkeycol = list(filter(lambda x:x[6]=='y',items))
        indexcol = list(filter(lambda x:x[8]=='y',items))
        if pkeycol != None:
            if len(indexcol) > 0:
                strings.append('  PRIMARY KEY (`'+ pkeycol[0][3] +'`),'+'\n')
            else:
                strings.append('  PRIMARY KEY (`'+ pkeycol[0][3] +'`)'+'\n')
        ikey = []
        for ic in indexcol:
            ikey.append('  `'+ ic[3] +'`')
        strings.append('  KEY `Key_Index` ('+str(ikey).replace('[','').replace(']','').replace("'",'')+')'+'\n')
        strings.append(') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'+'\n')
        strings.append('\n')
        strings.append('\n')
        strings.append('\n')
fout.writelines(strings)
print('end')
fout.close()