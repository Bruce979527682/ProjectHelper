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

workbook = xlrd.open_workbook(r''+deskPath+'\\basetable.xlsx')
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
    sb.append('  KEY `Key_Index` (' +
              str(ikey).replace('[', '').replace(']', '').replace("'", '')+')'+'\n')
    sb.append(') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'+'\n')
    fout = open(filepath + '/'+key+'-database.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def listpage(rows, key):
    sb = []

    sb.append('<template>'+'\n')
    sb.append('  <div class="data-main-container">'+'\n')
    sb.append('    <section class="data-section">'+'\n')
    sb.append('      <h1 class="title">'+'\n')
    sb.append('        <el-button'+'\n')
    sb.append('          type="text"'+'\n')
    sb.append('          icon="el-icon-back"'+'\n')
    sb.append('          style="margin-top: -5px"'+'\n')
    sb.append('          @click="switchPage(0)"'+'\n')
    sb.append('          >返回</el-button'+'\n')
    sb.append('        >'+'\n')
    sb.append('        <el-divider direction="vertical"></el-divider>'+'\n')
    sb.append('        <span>'+ tnames[key] +'</span>'+'\n')
    sb.append('      </h1>'+'\n')
    sb.append('      <el-row style="margin-bottom: 15px">'+'\n')
    sb.append('        <el-button'+'\n')
    sb.append('          type="primary"'+'\n')
    sb.append('          size="mini"'+'\n')
    sb.append('          @click="editItem()"'+'\n')
    sb.append('          style="width: 120px"'+'\n')
    sb.append('          >新建'+ tnames[key] +'</el-button'+'\n')
    sb.append('        >'+'\n')
    sb.append('      </el-row>'+'\n')
    sb.append('      <el-row>'+'\n')
    sb.append('        <el-table'+'\n')
    sb.append('          :data="list"'+'\n')
    sb.append('          style="width: 100%"'+'\n')
    sb.append('          :header-cell-style="{'+'\n')
    sb.append('            textAlign: "center",'+'\n')
    sb.append('            backgroundColor: "#F0F2F5",'+'\n')
    sb.append('          }"'+'\n')
    sb.append('          :cell-style="{ textAlign: "center" }"'+'\n')
    sb.append('          @sort-change="tableSort"'+'\n')
    sb.append('        >'+'\n')
    
    for row in rows:
        sb.append('          <el-table-column label="'+ row[2] +'">'+'\n')
        sb.append('            <template slot-scope="scope">'+'\n')
        sb.append('              <span>{{ scope.row.'+ row[3] +' }}</span>'+'\n')
        sb.append('            </template>'+'\n')
        sb.append('          </el-table-column>'+'\n')
    
    sb.append('          <el-table-column label="操作" width="190px">'+'\n')
    sb.append('            <template slot-scope="scope">'+'\n')
    sb.append('              <el-button'+'\n')
    sb.append('                type="text"'+'\n')
    sb.append('                @click="editItem(scope.row)"'+'\n')
    sb.append('                style="padding-top: 7px"'+'\n')
    sb.append('                >编辑</el-button'+'\n')
    sb.append('              >'+'\n')
    sb.append('            </template>'+'\n')
    sb.append('          </el-table-column>'+'\n')
    sb.append('        </el-table>'+'\n')
    sb.append('        <el-pagination'+'\n')
    sb.append('            @size-change="handleSizeChange"'+'\n')
    sb.append('            @current-change="handleCurrentChange"'+'\n')
    sb.append('            :current-page="query.page"'+'\n')
    sb.append('            :page-sizes="[10]"'+'\n')
    sb.append('            :page-size="query.size"'+'\n')
    sb.append('            layout="total, sizes, prev, pager, next, jumper"'+'\n')
    sb.append('            :total="query.total"'+'\n')
    sb.append('            class="div-paging"'+'\n')
    sb.append('        ></el-pagination>'+'\n')
    sb.append('      </el-row>'+'\n')
    sb.append('    </section>'+'\n')
    sb.append('  </div>'+'\n')
    sb.append('</template>'+'\n')
    sb.append('<script>'+'\n')
    sb.append('import { getLiveStudioInfo } from "@/utils/http/modules/common.api";'+'\n')
    sb.append('import {'+'\n')
    sb.append('  getlList,'+'\n')
    sb.append('} from "@/utils/http/modules/Scrm/request";'+'\n')
    sb.append('export default {'+'\n')
    sb.append('  data() {'+'\n')
    sb.append('    return {'+'\n')
    sb.append('      zid: 0,'+'\n')
    sb.append('      list: [],'+'\n')
    sb.append('      query: {'+'\n')
    sb.append('        zbId: 0,'+'\n')
    sb.append('        page: 1,'+'\n')
    sb.append('        size: 10,'+'\n')
    sb.append('      },'+'\n')
    sb.append('      dialogVisible: false,'+'\n')
    sb.append('    };'+'\n')
    sb.append('  },'+'\n')
    sb.append('  components: {},'+'\n')
    sb.append('  methods: {'+'\n')
    sb.append('    initPage() {'+'\n')
    sb.append('      this.$bus.$emit("breadcrumbItem", ['+'\n')
    sb.append('        { name: "'+ tnames[key] +'" },'+'\n')
    sb.append('      ]);'+'\n')
    sb.append('      this.zid = this.$store.state.zbid;'+'\n')
    sb.append('      this.query.zbId = this.$store.state.zbid;'+'\n')
    sb.append('    },'+'\n')
    sb.append('    loadData() {'+'\n')
    sb.append('      var self = this;'+'\n')
    sb.append('      getList(self.query).then((response) => {'+'\n')
    sb.append('        if (response.data.code == 0) {'+'\n')
    sb.append('          self.list = response.data.data.list;'+'\n')
    sb.append('          self.query.total = response.data.data.totalRows;'+'\n')
    sb.append('        } else {'+'\n')
    sb.append('          self.$elementMessage(response.data.msg);'+'\n')
    sb.append('        }'+'\n')
    sb.append('      });'+'\n')
    sb.append('    },'+'\n')
    sb.append('    handleSizeChange(val) {'+'\n')
    sb.append('      this.query.page = 1;'+'\n')
    sb.append('      this.query.size = val;'+'\n')
    sb.append('      this.loadData();'+'\n')
    sb.append('    },'+'\n')
    sb.append('    handleCurrentChange(val) {'+'\n')
    sb.append('      this.query.page = val;'+'\n')
    sb.append('      this.loadData();'+'\n')
    sb.append('    },'+'\n')
    sb.append('    clickEvent(data) {'+'\n')
    sb.append('        var self = this;'+'\n')
    sb.append('        }'+'\n')
    sb.append('    },'+'\n')
    sb.append('    editItem(data) {'+'\n')
    sb.append('        var self = this;'+'\n')
    sb.append('        }'+'\n')
    sb.append('    },'+'\n')
    sb.append('    switchPage(type) {'+'\n')
    sb.append('      if (type == 0) {'+'\n')
    sb.append('        this.$router.push({ path: `/` });'+'\n')
    sb.append('      }'+'\n')
    sb.append('    },'+'\n')
    sb.append('    async checkVersion(zbId) {'+'\n')
    sb.append('      var self = this;'+'\n')
    sb.append('      var res = await getLiveStudioInfo(zbId);'+'\n')
    sb.append('      if (res) {'+'\n')
    sb.append('        self.$upgradeModel(zbId, res.dataObj.Version);'+'\n')
    sb.append('      }'+'\n')
    sb.append('    },'+'\n')
    sb.append('  },'+'\n')
    sb.append('  created() {'+'\n')
    sb.append('    this.initPage();'+'\n')
    sb.append('    this.checkVersion(this.zid);'+'\n')
    sb.append('    this.loadData();'+'\n')
    sb.append('  },'+'\n')
    sb.append('};'+'\n')
    sb.append('</script>'+'\n')
    sb.append(''+'\n')
    sb.append('<style scoped>'+'\n')
    sb.append('.data-main-container {'+'\n')
    sb.append('  background-color: #f0f2f5;'+'\n')
    sb.append('  font-size: 14px;'+'\n')
    sb.append('  width: 100%;'+'\n')
    sb.append('}'+'\n')
    sb.append('.data-section {'+'\n')
    sb.append('  background-color: #fff;'+'\n')
    sb.append('  border-radius: 2px;'+'\n')
    sb.append('  padding: 0 15px;'+'\n')
    sb.append('  height: 100%;'+'\n')
    sb.append('}'+'\n')
    sb.append('.title {'+'\n')
    sb.append('  align-items: center;'+'\n')
    sb.append('  line-height: 50px;'+'\n')
    sb.append('  align-content: center;'+'\n')
    sb.append('  color: #353535;'+'\n')
    sb.append('  font-size: 16px;'+'\n')
    sb.append('  border-bottom: 1px solid #ccc;'+'\n')
    sb.append('  margin: 0px 0 15px 0;'+'\n')
    sb.append('}'+'\n')
    sb.append('.div-paging {'+'\n')
    sb.append('  text-align: center;'+'\n')
    sb.append('  margin: 15px;'+'\n')
    sb.append('}'+'\n')
    sb.append('</style>'+'\n')
    
    fout = open(filepath + '/'+key+'-常用列表页.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def detailpage(rows, key):
    sb = []

    
    
    fout = open(filepath + '/'+key+'-常用详情页.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

for key in tables:
    items = tables[key]
    # database
    database(items)

    # 列表页
    listpage(items, key)

    # 详情页
    # detailpage(items, key)

print('end')
