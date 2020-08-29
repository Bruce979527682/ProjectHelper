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
    sb.append('using Entity.Api;'+'\n')
    sb.append('using System.Collections.Generic;'+'\n')
    sb.append(''+'\n')
    sb.append('namespace BLL.Api'+'\n')
    sb.append('{'+'\n')
    sb.append('    /// <summary>'+'\n')
    sb.append('    /// ' + tnames[key]+'表BLL\n')
    sb.append('    /// </summary>'+'\n')
    sb.append('    public class ' + key + 'BLL: BaseSqlSugar<' + key + '>\n')
    sb.append('    {'+'\n')
    sb.append('        private string _cacheKey = "'+key+'_{0}";'+'\n')
    sb.append('        #region 单例'+'\n')
    sb.append('        private static ' + key + 'BLL _singleton;'+'\n')
    sb.append('        private static readonly object LockObject = new object();'+'\n')
    sb.append('        '+'\n')
    sb.append('        private ' + key + 'BLL()'+'\n')
    sb.append('        {'+'\n')
    sb.append('            '+'\n')
    sb.append('        }'+'\n')
    sb.append('        '+'\n')
    sb.append('        public static ' + key + 'BLL Singleton'+'\n')
    sb.append('        {'+'\n')
    sb.append('            get'+'\n')
    sb.append('            {'+'\n')
    sb.append('                if (_singleton == null)'+'\n')
    sb.append('                {'+'\n')
    sb.append('                    lock (LockObject)'+'\n')
    sb.append('                    {'+'\n')
    sb.append('                        if (_singleton == null)'+'\n')
    sb.append('                        {'+'\n')
    sb.append('                            _singleton = new ' + key + 'BLL();'+'\n')
    sb.append('                        }'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                }'+'\n')
    sb.append('                return _singleton;'+'\n')
    sb.append('            }'+'\n')
    sb.append('        }'+'\n')
    sb.append('        #endregion 单例'+'\n')    
    sb.append('        '+'\n')
    sb.append('        /// <summary>'+'\n')
    sb.append('        /// 获取' + tnames[key] +'数据'+'\n')
    sb.append('        /// </summary>'+'\n')
    sb.append('        /// <param name="cityInfoId">同城ID</param>'+'\n')
    sb.append('        /// <param name="pageIndex"></param>'+'\n')
    sb.append('        /// <param name="pageSize"></param>'+'\n')
    sb.append('        /// <returns></returns>'+'\n')
    sb.append('        public List<' + key + '> Get' + key + 'List(int pageIndex = 1, int pageSize = 10)'+'\n')
    sb.append('        {'+'\n')
    sb.append('            var where = $"Status<>-4";'+'\n')
    sb.append('            var totalCount = 0;'+'\n')
    sb.append('            return GetList(where, ref totalCount, pageIndex, pageSize);'+'\n')
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

def htmllist(rows, key):
    sb = []
    sb.append('<template>'+'\n')
    sb.append('  <div :style="{padding:"15px"}">'+'\n')
    sb.append('    <div style="margin:20px 0 10px;">'+'\n')
    sb.append('      <el-button type="primary" @click="editClick(0)">新增'+ tnames[key] +'</el-button>'+'\n')
    sb.append('    </div>'+'\n')
    sb.append('    <div>'+'\n')
    sb.append('      <el-table :data="list" border style="width: 100%">'+'\n')
    for row in rows:
        sb.append('        <el-table-column prop="' + str(row[3]) + '" label="' + str(row[2]) + '" width="120"></el-table-column>'+'\n')
    sb.append('        <el-table-column fixed="right" label="操作" width="100">'+'\n')
    sb.append('          <template slot-scope="scope">'+'\n')
    sb.append('            <el-button type="text" size="small" @click="editClick(1,scope.row)">编辑</el-button>'+'\n')
    sb.append('            <el-button type="text" size="small" @click="delService(scope.row.Id)">删除</el-button>'+'\n')
    sb.append('          </template>'+'\n')
    sb.append('        </el-table-column>'+'\n')
    sb.append('      </el-table>'+'\n')
    sb.append('      <el-pagination'+'\n')
    sb.append('        layout="prev, pager, next"'+'\n')
    sb.append('        :current-page="query.pageIndex"'+'\n')
    sb.append('        :page-size="query.pageSize"'+'\n')
    sb.append('        :total="count"'+'\n')
    sb.append('      ></el-pagination>'+'\n')
    sb.append('      <el-dialog title="添加修改'+ tnames[key] +'" :visible.sync="dialogVisible" width="30%" center>'+'\n')
    sb.append('        <div class="div_box">'+'\n')
    sb.append('          <el-form ref="elform" :model="editModel" label-width="120px" @submit.native.prevent>'+'\n')
    for row in rows:
        sb.append('            <el-form-item label="' + str(row[2]) + '">'+'\n')
        sb.append('              <el-input v-model="editModel.' + str(row[3]) + '"></el-input>'+'\n')
        sb.append('            </el-form-item>'+'\n')
    sb.append('          </el-form>'+'\n')
    sb.append('        </div>'+'\n')
    sb.append('        <span slot="footer" class="dialog-footer">'+'\n')
    sb.append('          <el-button @click="dialogVisible = false">取 消</el-button>'+'\n')
    sb.append('          <el-button type="primary" @click="saveModel()">确 定</el-button>'+'\n')
    sb.append('        </span>'+'\n')
    sb.append('      </el-dialog>'+'\n')
    sb.append('    </div>'+'\n')
    sb.append('  </div>'+'\n')
    sb.append('</template>'+'\n')
    sb.append(''+'\n')
    sb.append('<script>'+'\n')
    sb.append('export default {'+'\n')
    sb.append('  components: {},'+'\n')
    sb.append('  props: {},'+'\n')
    sb.append('  data() {'+'\n')
    sb.append('    return {'+'\n')
    sb.append('      query: {'+'\n')
    sb.append('        pageIndex: 1,'+'\n')
    sb.append('        pageSize: 10,'+'\n')
    sb.append('      },'+'\n')
    sb.append('      list: [],'+'\n')
    sb.append('      count: 0,'+'\n')
    sb.append('      dialogVisible: false,'+'\n')
    sb.append('      editModel: {'+'\n')
    for row in rows:
        sb.append('        ' + str(row[3]) + ': "",'+'\n')    
    sb.append('      },'+'\n')
    sb.append('      typeList: ['+'\n')
    sb.append('        { Id: 0, Name: "网页类型" },'+'\n')
    sb.append('        { Id: 1, Name: "接口类型" },'+'\n')
    sb.append('      ],'+'\n')
    sb.append('    };'+'\n')
    sb.append('  },'+'\n')
    sb.append('  watch: {},'+'\n')
    sb.append('  computed: {},'+'\n')
    sb.append('  methods: {'+'\n')
    sb.append('    loadData() {'+'\n')
    sb.append('      var self = this;'+'\n')
    sb.append('      this.$HttpGet("/Admin/Get' + key + 'List", self.query)'+'\n')
    sb.append('        .then(function (response) {'+'\n')
    sb.append('          if (response.data.code === 1) {'+'\n')
    sb.append('            self.list = response.data.obj.list;'+'\n')
    sb.append('            self.count = response.data.obj.count;'+'\n')
    sb.append('          } else {'+'\n')
    sb.append('            self.$message(response.data.msg);'+'\n')
    sb.append('          }'+'\n')
    sb.append('        })'+'\n')
    sb.append('        .catch(function (error) {'+'\n')
    sb.append('          console.log(error);'+'\n')
    sb.append('        });'+'\n')
    sb.append('    },'+'\n')
    sb.append('    saveModel() {'+'\n')
    sb.append('      var self = this;'+'\n')
    sb.append('      this.$HttpPostJson("/Admin/Save' + key + '", this.editModel)'+'\n')
    sb.append('        .then(function (response) {'+'\n')
    sb.append('          if (response.data.code == 1) {'+'\n')
    sb.append('            self.$message(response.data.msg);'+'\n')
    sb.append('            self.loadData();'+'\n')
    sb.append('          } else {'+'\n')
    sb.append('            self.$message(response.data.msg);'+'\n')
    sb.append('          }'+'\n')
    sb.append('        })'+'\n')
    sb.append('        .catch(function (error) {'+'\n')
    sb.append('          console.log(error);'+'\n')
    sb.append('        });'+'\n')
    sb.append('      self.dialogVisible = false;'+'\n')
    sb.append('    },'+'\n')
    sb.append('    editClick(type, row) {'+'\n')
    sb.append('      if (type == 0) {'+'\n')
    sb.append('        this.editModel = {'+'\n')
    sb.append('          Id: 0,'+'\n')
    sb.append('          Name: "",'+'\n')
    sb.append('          ImgUrl: "",'+'\n')
    sb.append('          Url: "",'+'\n')
    sb.append('          Content: "",'+'\n')
    sb.append('          Type: 0,'+'\n')
    sb.append('          ServiceType: "",'+'\n')
    sb.append('        };'+'\n')
    sb.append('      } else {'+'\n')
    sb.append('        if (row.ServiceType == 0) {'+'\n')
    sb.append('          row.ServiceType = "";'+'\n')
    sb.append('        }'+'\n')
    sb.append('        this.editModel = row;'+'\n')
    sb.append('      }'+'\n')
    sb.append('      this.dialogVisible = true;'+'\n')
    sb.append('    },'+'\n')
    sb.append('    delModel(id) {'+'\n')
    sb.append('      var self = this;'+'\n')
    sb.append('      this.$HttpPost("/Admin/Del' + key + '", { oid: id })'+'\n')
    sb.append('        .then(function (response) {'+'\n')
    sb.append('          if (response.data.code == 1) {'+'\n')
    sb.append('            self.$message(response.data.msg);'+'\n')
    sb.append('            self.loadData();'+'\n')
    sb.append('          } else {'+'\n')
    sb.append('            self.$message(response.data.msg);'+'\n')
    sb.append('          }'+'\n')
    sb.append('        })'+'\n')
    sb.append('        .catch(function (error) {'+'\n')
    sb.append('          console.log(error);'+'\n')
    sb.append('        });'+'\n')
    sb.append('    },'+'\n')
    sb.append('    convertType(type){'+'\n')
    sb.append('      var type = this.typeList.find(x=>x.Id == type);'+'\n')
    sb.append('      if(type){'+'\n')
    sb.append('        return type.Name;'+'\n')
    sb.append('      }'+'\n')
    sb.append('      return "";'+'\n')
    sb.append('    }'+'\n')
    sb.append('  },'+'\n')
    sb.append('  created() {'+'\n')
    sb.append('    this.loadData();'+'\n')
    sb.append('  },'+'\n')
    sb.append('  mounted() {},'+'\n')
    sb.append('};'+'\n')
    sb.append('</script>'+'\n')
    sb.append('<style lang="scss" scoped>'+'\n')
    sb.append('.div_box {'+'\n')
    sb.append('  margin: 10px 20px;'+'\n')
    sb.append('  padding: 10px;'+'\n')
    sb.append('  background: #fff;'+'\n')
    sb.append('}'+'\n')
    sb.append(''+'\n')
    sb.append('.el-icon-plus:before {'+'\n')
    sb.append('  padding-top: 35px;'+'\n')
    sb.append('  display: block;'+'\n')
    sb.append('}'+'\n')
    sb.append('</style>'+'\n')

    fout = open(filepath + '/'+key+'-htmllist.txt', "w", encoding='utf-8')
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
   
    # htmllist
    htmllist(items, key)

print('end')
