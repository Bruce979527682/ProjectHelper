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

def entity(rows, key):
    sb = []
    sb.append('using Entity.Base;'+'\n')
    sb.append('using System;'+'\n')
    sb.append('using Utility;'+'\n')
    sb.append('namespace Entity.MiniSNS.Friend'+'\n')
    sb.append('{'+'\n')
    sb.append('    /// <summary>'+'\n')
    sb.append('    /// ' + tnames[key]+'表\n')
    sb.append('    /// </summary>'+'\n')
    sb.append('    [Serializable]'+'\n')
    sb.append('    [SqlTable(dbEnum.QLWL)]'+'\n')
    sb.append('    public class ' + key + '\n')
    sb.append('    {'+'\n')

    for row in rows:
        sb.append('        /// <summary>'+'\n')
        sb.append('        /// ' + row[2]+'\n')
        sb.append('        /// </summary>'+'\n')
        if row[6] == 'y' and row[7] == 'y':
            sb.append(
                '        [SqlField(IsPrimaryKey = true, IsAutoId = true)]'+'\n')
        elif row[6] == 'y':
            sb.append('        [SqlField(IsPrimaryKey = true)]'+'\n')
        elif row[7] == 'y':
            sb.append('        [SqlField(IsAutoId = true)]'+'\n')
        else:
            sb.append('        [SqlField]'+'\n')
        if row[11] != '':
            if str(row[4]) == 'varchar':
                sb.append('        public string ' +
                          str(row[3]) + ' { get; set; } = ' + str(row[11]) + ';'+'\n')
            elif str(row[4]) == 'datetime':
                sb.append('        public DateTime ' +
                          str(row[3]) + ' { get; set; } = ' + str(row[11]) + ';'+'\n')
            else:
                sb.append('        public ' + str(row[4]) + ' ' + str(
                    row[3]) + ' { get; set; } = ' + str(row[11]) + ';'+'\n')
        else:
            if str(row[4]) == 'varchar':
                sb.append('        public string ' +
                          str(row[3]) + ' { get; set; }'+'\n')
            elif str(row[4]) == 'datetime':
                sb.append('        public DateTime ' +
                          str(row[3]) + ' { get; set; }'+'\n')
            else:
                sb.append('        public ' +
                          str(row[4]) + ' ' + str(row[3]) + ' { get; set; }'+'\n')
    sb.append('    }'+'\n')
    sb.append('}'+'\n')
    fout = open(filepath + '/'+key+'.cs', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def bll(rows, key):
    sb = []
    sb.append('using System;'+'\n')
    sb.append('using DAL.Base;'+'\n')
    sb.append('using Entity.MiniSNS.Friend;'+'\n')
    sb.append('using System.Collections.Generic;'+'\n')
    sb.append('namespace BLL.MiniSNS.Friend'+'\n')
    sb.append('{'+'\n')
    sb.append('    /// <summary>'+'\n')
    sb.append('    /// ' + tnames[key]+'表BLL\n')
    sb.append('    /// </summary>'+'\n')
    sb.append('    public class ' + key + 'BLL: BaseMySql<' + key + '>\n')
    sb.append('    {'+'\n')
    sb.append('        private string _cacheKey = "'+key+'_{0}";'+'\n')
    sb.append('        public '+key+' GetModelByCache(int id)'+'\n')
    sb.append('        {'+'\n')
    sb.append(
        '            string key = string.Format(_cacheKey, id);'+'\n')
    sb.append('            var model = RedisUtil.Get<'+key+'>(key);'+'\n')
    sb.append('            if (model != null)'+'\n')
    sb.append('            {'+'\n')
    sb.append('                return model;'+'\n')
    sb.append('            }'+'\n')
    sb.append('            else'+'\n')
    sb.append('            {'+'\n')
    sb.append('                model = GetModel(id);'+'\n')
    sb.append('                if (model != null)'+'\n')
    sb.append('                {'+'\n')
    sb.append('                    RedisUtil.Set<' + key+'>(key, model,TimeSpan.FromDays(1));'+'\n')
    sb.append('                }'+'\n')
    sb.append('                return model;'+'\n')
    sb.append('            }'+'\n')
    sb.append('        }'+'\n')
    sb.append('        '+'\n')
    sb.append('        public bool RemoveCache(int id)'+'\n')
    sb.append('        {'+'\n')
    sb.append(
        '            string key = string.Format(_cacheKey, id);'+'\n')
    sb.append('            return RedisUtil.Remove(key);'+'\n')
    sb.append('        }'+'\n')
    sb.append('        '+'\n')
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
    if pkeycol != None:
        if len(indexcol) > 0:
            sb.append('  PRIMARY KEY (`' + pkeycol[0][3] + '`),'+'\n')
        else:
            sb.append('  PRIMARY KEY (`' + pkeycol[0][3] + '`)'+'\n')
    ikey = []
    for ic in indexcol:
        ikey.append(' `' + ic[3] + '`')
    sb.append('  KEY `Key_Index` (' +
              str(ikey).replace('[', '').replace(']', '').replace("'", '')+')'+'\n')
    sb.append(') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;'+'\n')
    fout = open(filepath + '/'+key+'-database.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def client(rows, key):
    sb = []
    sb.append('@model  '+key+''+'\n')
    sb.append('@{'+'\n')
    sb.append('    ViewBag.Title = "'+key+'";'+'\n')
    sb.append('    Layout = "~/Views/Shared/_Layout.cshtml";'+'\n')
    sb.append('}'+'\n')
    sb.append(''+'\n')
    sb.append('<div id="main">'+'\n')
    sb.append(''+'\n')
    sb.append('</div>'+'\n')
    sb.append(''+'\n')
    sb.append('<script>'+'\n')
    sb.append('    var app = new Vue({'+'\n')
    sb.append('        el: "#main",'+'\n')
    sb.append('        data: {'+'\n')
    sb.append('            list: [],'+'\n')
    sb.append('            isCreatedComplete: false,'+'\n')
    sb.append('            time: 60,'+'\n')
    sb.append('            startTime: 60,'+'\n')
    sb.append('            sendMsg: false,'+'\n')
    sb.append('            queryParm: {'+'\n')
    sb.append('                pageindex: 1,'+'\n')
    sb.append('                pagesize: 10,'+'\n')
    sb.append('            },'+'\n')
    sb.append('            inputData: {'+'\n')
    for row in rows:
        if row[4] == 'int':
            sb.append('                ' + row[3].lower() + ': 0,'+'\n')
        else:
            sb.append('                ' + row[3].lower() + ': "",'+'\n')

    sb.append('            }'+'\n')
    sb.append('        },'+'\n')
    sb.append('        filters: {'+'\n')
    sb.append('            nameFilter: function (value) {'+'\n')
    sb.append('                return value;'+'\n')
    sb.append('            }'+'\n')
    sb.append('        },'+'\n')
    sb.append('        methods: {'+'\n')
    sb.append('            loadData() {'+'\n')
    sb.append(''+'\n')
    sb.append('            },'+'\n')
    sb.append('            handleScroll() {'+'\n')
    sb.append('                var height = document.documentElement.scrollHeight;'+'\n')
    sb.append('                var scrolltop = document.documentElement.scrollTop;'+'\n')
    sb.append('                var cheight = document.documentElement.clientHeight;'+'\n')
    sb.append('                if (cheight + scrolltop > height - 40) {'+'\n')
    sb.append('                    if (!this.isLoading && !this.isStopped) {'+'\n')
    sb.append('                        this.loadData();'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                }'+'\n')
    sb.append('            },'+'\n')
    sb.append('            submitData() {'+'\n')
    sb.append('                $.ajax({'+'\n')
    sb.append('                    type: "POST",'+'\n')
    sb.append('                    url: "/fh/i",'+'\n')
    sb.append('                    data: this.inputData,'+'\n')
    sb.append('                    dataType: "json",'+'\n')
    sb.append('                    success: function (data) {'+'\n')
    sb.append('                        layer.closeAll();'+'\n')
    sb.append('                        if (1 == data.code) {'+'\n')
    sb.append(''+'\n')
    sb.append('                        } else {'+'\n')
    sb.append(
        '                            PopMsg("操作失败，请重新再试");'+'\n')
    sb.append('                        }'+'\n')
    sb.append('                    },'+'\n')
    sb.append(
        '                    error: function (XMLHttpRequest, textStatus, errorThrown) {'+'\n')
    sb.append('                        layer.closeAll();'+'\n')
    sb.append('                        PopMsg("操作失败，网络连接异常");'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                });'+'\n')
    sb.append('            }'+'\n')
    sb.append('        },'+'\n')
    sb.append('        computed: {'+'\n')
    sb.append('            isFinished() {'+'\n')

    notnull = []
    for row in rows:
        if row[12] == 'y':
            notnull.append('this.inputData.'+row[3].lower()+' != ""')
    notnullstr = ' && '.join(notnull)

    sb.append('                if (' + notnullstr + ') {'+'\n')
    sb.append('                    return true;'+'\n')
    sb.append('                }'+'\n')
    sb.append('                return false;'+'\n')
    sb.append('            }'+'\n')
    sb.append('        },'+'\n')
    sb.append('        watch: {'+'\n')
    sb.append(''+'\n')
    sb.append('        },'+'\n')
    sb.append('        beforeMount() {'+'\n')
    sb.append('            this.loadData();'+'\n')
    sb.append('        },'+'\n')
    sb.append('        mounted() {'+'\n')
    sb.append(''+'\n')
    sb.append('            //window.addEventListener(\'scroll\', this.handleScroll);'+'\n')
    sb.append('            // 上拉加载更多'+'\n')
    sb.append('            $(window).scroll(function () {'+'\n')
    sb.append('                var scrollTop = $(this).scrollTop(); //---溢出顶部的高'+'\n')
    sb.append('                var scrollHeight = $(document).height(); //---页面所有内容的高'+'\n')
    sb.append('                var windowHeight = $(this).height(); //---页面可见的高'+'\n')
    sb.append('                if ((scrollTop + windowHeight) >= (scrollHeight)) {'+'\n')
    sb.append('                    if (!app.isLoading && !app.isStopped) {'+'\n')
    sb.append('                        app.queryParm.pageindex += 1;'+'\n')
    sb.append('                        app.loadData();'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                }'+'\n')
    sb.append('            });'+'\n')
    sb.append('            '+'\n')
    sb.append('        },'+'\n')
    sb.append('        created: function () {'+'\n')
    sb.append('            this.isCreatedComplete = true;'+'\n')
    sb.append('        }'+'\n')
    sb.append('    });'+'\n')
    sb.append('</script>'+'\n')
    fout = open(filepath + '/'+key+'-client.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def server(rows, key):
    sb = []
    sb.append('        /// <summary>'+'\n')
    sb.append('        /// 新增信息'+'\n')
    sb.append('        /// </summary>'+'\n')
    sb.append('        /// <returns></returns>'+'\n')
    sb.append('        [HttpPost]'+'\n')
    sb.append('        public JsonResult submit()'+'\n')
    sb.append('        {'+'\n')
    sb.append('            var minisnsId = Utils.GetRequestInt("id", 0);'+'\n')

    for row in rows:
        if row[4] == 'int':
            sb.append('            var ' + row[3].lower() +
                      ' = Utils.GetRequestInt("' + row[3].lower() + '", 0);'+'\n')
        else:
            sb.append('            var ' + row[3].lower() +
                      ' = Utils.GetRequest("' + row[3].lower() + '", "");'+'\n')
    sb.append('            var ' + key.lower() + ' = new ' + key + ''+'\n')
    sb.append('            {'+'\n')

    for row in rows:
        if row[4] == 'int':
            sb.append('                ' + row[3] + ' = ' + row[3].lower() + ','+'\n')
        elif row[4] == 'varchar':
            sb.append('                ' + row[3] + ' = ' + row[3].lower() + ','+'\n')
        elif row[4] == 'datetime':
            sb.append('                ' + row[3] + ' = DateTime.Now,'+'\n')
        else:
            sb.append('                ' + row[3] + ' = ' + row[3].lower() + ','+'\n')

    sb.append('            };'+'\n')
    sb.append(
        '            return Json(new { code = -4, msg = "操作失败！" });'+'\n')
    sb.append('        }'+'\n')
    fout = open(filepath + '/'+key+'-cs.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def clientht(rows, key):
    sb = []
    sb.append('@model WebUI.MiniSNSAdmin.Model.FriendViewModel'+'\n')
    sb.append('@{'+'\n')
    sb.append('    ViewBag.title = "'+tnames[key]+'";'+'\n')
    sb.append('    ViewBag.flag = "";'+'\n')
    sb.append('    Layout = "~/Views/Friend/_LeftmenuLayout.cshtml";'+'\n')
    sb.append('}'+'\n')
    sb.append(''+'\n')
    sb.append('<script type="text/javascript" src="~/content/H-UI.Admin/lib/laypage/1.2/laypage.js"></script>'+'\n')
    sb.append('<script src="~/Content/layer/layer.js"></script>'+'\n')
    sb.append(''+'\n')
    sb.append('<style>'+'\n')
    sb.append('    #page div {'+'\n')
    sb.append('        text-align: center;'+'\n')
    sb.append('    }'+'\n')
    sb.append('    th {'+'\n')
    sb.append('        background-color: #f5f5f6;'+'\n')
    sb.append('    }'+'\n')
    sb.append('    .btn {'+'\n')
    sb.append('        margin-top: 5px;'+'\n')
    sb.append('    }'+'\n')
    sb.append('    body {'+'\n')
    sb.append('        height: 100%;'+'\n')
    sb.append('    }'+'\n')
    sb.append('    .p-user-name {'+'\n')
    sb.append('        max-width: 120px;'+'\n')
    sb.append('        overflow: hidden;'+'\n')
    sb.append('        height: 15px;'+'\n')
    sb.append('        text-align: center;'+'\n')
    sb.append('        margin: 8px 5px;'+'\n')
    sb.append('    }'+'\n')
    sb.append('    .text-c img {'+'\n')
    sb.append('        width: 80px;'+'\n')
    sb.append('        height: 80px;'+'\n')
    sb.append('    }'+'\n')
    sb.append('</style>'+'\n')
    sb.append(''+'\n')
    sb.append('<div id="main" class="page-container" style="display:none;" v-show="isCreatedComplete">'+'\n')
    sb.append('    <div>'+'\n')

    for row in rows:
        if row[13] == 'y':
            if row[4] == 'datetime':
                sb.append('        <span>'+'\n')
                sb.append('            &nbsp;&nbsp;'+row[2]+'：'+'\n')
                sb.append(
                    '            <input type="text" id="startTime" placeholder="开始时间" autocomplete="off" style="width:150px" class="input-text" onfocus="WdatePicker({ dateFmt: \'yyyy/MM/dd\', maxDate: \'@DateTime.Now\' })">'+'\n')
                sb.append('        </span>'+'\n')
                sb.append('        <span>'+'\n')
                sb.append('            &nbsp;&nbsp;至：'+'\n')
                sb.append(
                    '            <input type="text" id="endTime" placeholder="结束时间" autocomplete="off" style="width:150px" class="input-text" onfocus="WdatePicker({ dateFmt: \'yyyy/MM/dd\', maxDate: \'@DateTime.Now\' })">'+'\n')
                sb.append('        </span>'+'\n')
            elif row[4] == 'int':
                sb.append('        &nbsp;&nbsp;'+row[2]+'：'+'\n')
                sb.append('        <input type="text" name="'+row[3].lower()+'" id="'+row[3].lower()+'" placeholder="'+row[2] +
                          '" style="width:100px" class="input-text" onkeyup="this.value=this.value.replace(/[^0-9]/g,'')" onafterpaste="this.value=this.value.replace(/[^0-9]/g,'')">'+'\n')
            else:
                sb.append('        &nbsp;&nbsp;'+row[2]+'：'+'\n')
                sb.append('        <input type="text" name="'+row[3].lower()+'" id="'+row[3].lower(
                )+'" placeholder="'+row[2]+'" style="width:100px" class="input-text">'+'\n')

    sb.append('            <button class="btn btn-warning" type="submit" @@click="clearData()" style="margin-top:0px;"><i class="Hui-iconfont">&#xe609;</i> 清空条件</button>'+'\n')
    sb.append('            <button class="btn btn-success" type="submit" @@click="search()" style="margin-top:0px;"><i class="Hui-iconfont">&#xe665;</i> 搜索</button>'+'\n')
    sb.append('    </div>'+'\n')
    sb.append('    <div class="cl pd-5 bg-1 bk-gray mt-20">'+'\n')
    sb.append(
        '        <div style="float: right;margin: 5px 5px 0px 20px;" class="dataTables_length">'+'\n')
    sb.append('            <label>'+'\n')
    sb.append('                显示'+'\n')
    sb.append('                <select @@change="pagesizeChange(this)">'+'\n')
    sb.append('                    <option value="10">10</option>'+'\n')
    sb.append('                    <option value="25">25</option>'+'\n')
    sb.append('                    <option value="50">50</option>'+'\n')
    sb.append('                    <option value="100">100</option>'+'\n')
    sb.append('                </select> 条'+'\n')
    sb.append('            </label>'+'\n')
    sb.append('        </div>'+'\n')
    sb.append('        <span class="r" style="position: relative;top: 5px;">共有数据：<strong id="TotalCount">{{totalCount}}</strong> 条</span>'+'\n')
    sb.append('    </div>'+'\n')
    sb.append(
        '    <div class="mt-20">'+'\n')
    sb.append(
        '        <table class="table table-border table-bordered table-bg table-hover dataTable">'+'\n')
    sb.append('            <thead>'+'\n')
    sb.append('                <tr class="text-c">'+'\n')

    for row in rows:
        if row[14] == 'y':
            sb.append('                    <th>'+row[2]+'</th>'+'\n')

    sb.append('                    <th style="width: 200px;">操作</th>'+'\n')

    sb.append('                </tr>'+'\n')
    sb.append('            </thead>'+'\n')
    sb.append('            <tbody id="pageBody">'+'\n')
    sb.append('                <tr class="text-c" v-for="' +
              key.lower()+' in datalist">'+'\n')

    for row in rows:
        if row[14] == 'y':
            sb.append('                    <td>'+'\n')
            sb.append(
                '                        {{'+key.lower()+'.'+row[3]+'}}'+'\n')
            sb.append('                    </td>'+'\n')

    sb.append('                    <td>'+'\n')
    sb.append('                        <input type="button" value="通过" @@click="passItem(' +
              key.lower()+'.Id)" class="btn btn-primary-outline radius">'+'\n')
    sb.append('                        <input type="button" value="不通过" @@click="notpassItem(' +
              key.lower()+'.Id)" class="btn btn-primary-outline radius">'+'\n')
    sb.append('                       <input type="button" value="删除" @@click="delItem(' +
              key.lower()+'.Id)" class="btn btn-danger-outline radius">'+'\n')
    sb.append('                    </td>'+'\n')
    sb.append('                </tr>'+'\n')
    sb.append('            </tbody>'+'\n')
    sb.append('        </table>'+'\n')
    sb.append(
        '        <div id="page" style="text-align: center;margin-top: 0.5rem;"></div>'+'\n')
    sb.append('        <div id="page-nodata" style="text-align: center;margin: 2rem auto;" v-show="datalist.length < 1">--暂无数据--</div>'+'\n')
    sb.append('    </div>'+'\n')
    sb.append('</div>'+'\n')
    sb.append(''+'\n')
    sb.append(
        '<script src="~/Content/H-UI.Admin/lib/My97DatePicker/WdatePicker.js"></script>'+'\n')
    sb.append(''+'\n')
    sb.append('<script>'+'\n')
    sb.append('    var app = new Vue({'+'\n')
    sb.append('        el: \'#main\','+'\n')
    sb.append('        data: {'+'\n')
    sb.append('            datalist: [],'+'\n')
    sb.append('            isCreatedComplete: false,'+'\n')
    sb.append('            totalCount: 0,'+'\n')
    sb.append('            queryPara:{'+'\n')
    sb.append('                pageindex: 1,'+'\n')
    sb.append('                pagesize: 10,'+'\n')
    sb.append('                startTime: \'\','+'\n')
    sb.append('                endTime: \'\','+'\n')

    for row in rows:
        if row[13] == 'y':
            if row[4] == 'int':
                sb.append('                '+row[3].lower()+': 0,'+'\n')
            else:
                sb.append('                '+row[3].lower()+': \'\','+'\n')

    sb.append('            }'+'\n')
    sb.append('        },'+'\n')
    sb.append('        methods: {'+'\n')
    sb.append('            delItem(id,uid) {'+'\n')
    sb.append(
        '                this.operExecute(id,\'确认删除吗？\', \'删除\',\'delete\');'+'\n')
    sb.append('            },'+'\n')
    sb.append('            passItem(id, uid) {'+'\n')
    sb.append(
        '                this.operExecute(id,\'确认通过吗？\', \'通过\', \'pass\');'+'\n')
    sb.append('            },'+'\n')
    sb.append('            notpassItem(id, uid) {'+'\n')
    sb.append(
        '                this.operExecute(id,\'确认不通过吗？\', \'不通过\', \'notpass\');'+'\n')
    sb.append('            },'+'\n')
    sb.append('            operExecute: function (id,tip,title,status) {'+'\n')
    sb.append('                layer.open({'+'\n')
    sb.append('                    content: tip,'+'\n')
    sb.append('                    btn: [\'确认\', \'取消\'],'+'\n')
    sb.append('                    title: title,'+'\n')
    sb.append('                    yes: function () {'+'\n')
    sb.append('                        $.ajax({'+'\n')
    sb.append('                            type: "POST",'+'\n')
    sb.append(
        '                            url: "/fajax/method/@Model.Minisns.Id",'+'\n')
    sb.append(
        '                            data: { oid: id,status: status },'+'\n')
    sb.append('                            dataType: "json",'+'\n')
    sb.append('                            success: function (data) {'+'\n')
    sb.append('                                layer.closeAll();'+'\n')
    sb.append('                                if (1 === data.code) {'+'\n')
    sb.append(
        '                                    layer.msg("操作成功", { icon: 1 });'+'\n')
    sb.append('                                    app.pageQuery();'+'\n')
    sb.append('                                } else {'+'\n')
    sb.append(
        '                                    layer.msg(data.msg, { icon: 2 });'+'\n')
    sb.append('                                }'+'\n')
    sb.append('                            },'+'\n')
    sb.append(
        '                            error: function (XMLHttpRequest, textStatus, errorThrown) {'+'\n')
    sb.append('                                layer.closeAll();'+'\n')
    sb.append(
        '                                layer.msg("操作失败，网络连接异常", { icon: 0 });'+'\n')
    sb.append('                            }'+'\n')
    sb.append('                        });'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                });'+'\n')
    sb.append('            },'+'\n')
    sb.append('            pageQuery() {'+'\n')
    sb.append(
        '                 $.post("/fajax/Get'+key+'List/@Model.Minisns.Id", this.queryPara, function (data) {'+'\n')
    sb.append('                     if (data != undefined) {'+'\n')
    sb.append('                         if (data.code == 1) {'+'\n')
    sb.append('                             app.datalist = data.list;'+'\n')
    sb.append('                             app.totalCount = data.count;'+'\n')
    sb.append(
        '                             app.resetPage(data.count, app.queryPara.pageindex);'+'\n')
    sb.append('                         }'+'\n')
    sb.append('                         else {'+'\n')
    sb.append('                             app.datalist = [];'+'\n')
    sb.append('                             app.resetPage(0, 1);'+'\n')
    sb.append('                         }'+'\n')
    sb.append('                     } else {'+'\n')
    sb.append('                         app.datalist = [];'+'\n')
    sb.append(
        '                         app.resetPage(0, app.queryPara.pageindex);'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                });'+'\n')
    sb.append('            },'+'\n')
    sb.append('            clearData() {'+'\n')

    for row in rows:
        if row[13] == 'y':
            sb.append('                $("#' +
                      row[3].lower()+'").val(\'\');'+'\n')
            sb.append('                this.queryPara.' +
                      row[3].lower()+' = \'\';'+'\n')
    sb.append('                this.pageQuery();'+'\n')
    sb.append('                this.queryPara.startTime = \'\';'+'\n')
    sb.append('                this.queryPara.endTime = \'\';'+'\n')

    sb.append('            },'+'\n')
    sb.append('            resetPage(recordCount, pageIndex) {'+'\n')
    sb.append('                var pages = recordCount % this.queryPara.pagesize == 0 ? recordCount / this.queryPara.pagesize : recordCount / this.queryPara.pagesize + 1;'+'\n')
    sb.append('                laypage({'+'\n')
    sb.append('                    cont: "page",'+'\n')
    sb.append('                    pages: pages,'+'\n')
    sb.append('                    curr: pageIndex,'+'\n')
    sb.append('                    jump: function (obj, first) {'+'\n')
    sb.append('                        if (!first) {'+'\n')
    sb.append(
        '                            app.queryPara.pageindex = obj.curr;'+'\n')
    sb.append('                            app.pageQuery();'+'\n')
    sb.append('                        }'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                });'+'\n')
    sb.append('                if (recordCount == 0) {'+'\n')
    sb.append('                    $(\'#laypage_1\').hide();'+'\n')
    sb.append('                }'+'\n')
    sb.append('            },'+'\n')
    sb.append('            pagesizeChange(node) {'+'\n')
    sb.append('                this.queryPara.pagesize = $(node).val();'+'\n')
    sb.append('                this.queryPara.pageindex = 1;'+'\n')
    sb.append('                this.pageQuery();'+'\n')
    sb.append('            },'+'\n')
    sb.append('            search() {'+'\n')

    for row in rows:
        if row[13] == 'y':
            if row[4] == 'datetime':
                sb.append('                this.queryPara.startTime = $(\'#startTime\').val().trim();'+'\n')
                sb.append('                this.queryPara.endTime = $(\'#endTime\').val().trim();'+'\n')
                sb.append('                if (this.queryPara.startTime !== \'\' || this.queryPara.endTime !== \'\') {'+'\n')
                sb.append('                    if (this.compareDate(this.queryPara.startTime, this.queryPara.endTime)) {'+'\n')
                sb.append('                        layer.msg(\'结束时间不能小于开始时间\');'+'\n')
                sb.append('                        return;'+'\n')
                sb.append('                    }'+'\n')
                sb.append('                }'+'\n')
            else:
                sb.append('                this.queryPara.' +
                          row[3].lower()+' = $(\'#'+row[3].lower()+'\').val().trim();'+'\n')
    sb.append('                this.pageQuery();'+'\n')

    sb.append('            },'+'\n')
    sb.append('            compareDate(checkStartDate, checkEndDate) {'+'\n')
    sb.append(
        '                if (new Date(checkStartDate) > new Date(checkEndDate)) {'+'\n')
    sb.append('                    return true;'+'\n')
    sb.append('                }'+'\n')
    sb.append('                return false;'+'\n')
    sb.append('            },'+'\n')
    sb.append('            convertTime: function (time) {'+'\n')
    sb.append(
        '                var date = new Date(parseInt(time.substr(6, 13)));'+'\n')
    sb.append('                var y = date.getFullYear();'+'\n')
    sb.append('                var m = date.getMonth() + 1;'+'\n')
    sb.append('                m = m < 10 ? (\'0\' + m) : m;'+'\n')
    sb.append('                var d = date.getDate();'+'\n')
    sb.append('                d = d < 10 ? (\'0\' + d) : d;'+'\n')
    sb.append('                var h = date.getHours();'+'\n')
    sb.append('                h = h < 10 ? (\'0\' + h) : h;'+'\n')
    sb.append('                var minute = date.getMinutes();'+'\n')
    sb.append('                var second = date.getSeconds();'+'\n')
    sb.append(
        '                minute = minute < 10 ? (\'0\' + minute) : minute;'+'\n')
    sb.append(
        '                second = second < 10 ? (\'0\' + second) : second;'+'\n')
    sb.append('                return y + \'-\' + m + \'-\' + d + \' \' + h + \':\' + minute + \':\' + second;'+'\n')
    sb.append('            }'+'\n')
    sb.append('        },'+'\n')
    sb.append('        computed: {'+'\n')
    sb.append('        },'+'\n')
    sb.append('        filters: {'+'\n')
    sb.append('        },'+'\n')
    sb.append('        beforeMount() {'+'\n')
    sb.append('            this.pageQuery();'+'\n')
    sb.append('        },'+'\n')
    sb.append('        mounted() {'+'\n')
    sb.append('        },'+'\n')
    sb.append('        created: function () {'+'\n')
    sb.append('            this.isCreatedComplete = true;'+'\n')
    sb.append('        }'+'\n')
    sb.append('    });'+'\n')
    sb.append('</script>'+'\n')
    fout = open(filepath + '/'+key+'-clientht.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def serverht(rows, key):
    sb = []
    sb.append('        /// <summary>'+'\n')
    sb.append('        /// 获取数据'+'\n')
    sb.append('        /// </summary>'+'\n')
    sb.append('        /// <returns></returns>'+'\n')
    sb.append('        [HttpPost]'+'\n')
    sb.append('        public JsonResult Get'+key+'List(int id)'+'\n')
    sb.append('        {'+'\n')
    sb.append(
        '            var pageIndex = Utils.GetRequestInt("pageindex", 1);'+'\n')
    sb.append('            var pageSize = Utils.GetRequestInt("pagesize", 10);'+'\n')
    sb.append('            var startTime = Utils.GetRequest("startTime", "");'+'\n')
    sb.append('            var endTime = Utils.GetRequest("endTime", "");'+'\n')
    for row in rows:
        if row[13] == 'y':
            if row[4] == 'int':
                sb.append('            var ' + row[3].lower(
                ) + ' = Utils.GetRequestInt("' + row[3].lower() + '", 0);'+'\n')
            else:
                sb.append(
                    '            var ' + row[3].lower() + ' = Utils.GetRequest("' + row[3].lower() + '", "");'+'\n')

    sb.append('            StringBuilder strWhere = new StringBuilder();'+'\n')
    sb.append(
        '            strWhere.Append($"MinisnsId={id} and Status>=0");'+'\n')

    for row in rows:
        if row[13] == 'y':
            if row[4] == 'int':
                sb.append('            if (' + row[3].lower() + ' > 0)'+'\n')
                sb.append('            {'+'\n')
                sb.append(
                    '                strWhere.AppendFormat(" and Id = {0}", ' + row[3].lower() + ');'+'\n')
                sb.append('            }'+'\n')
            elif row[4] == 'datetime':
                sb.append(
                    '            if (!string.IsNullOrEmpty(' + row[3].lower() + '))'+'\n')
                sb.append('            {'+'\n')
                sb.append('                strWhere.AppendFormat(" and ' +
                          row[3] + ' between \'{0}\' and DATE_ADD(\'{1}\',INTERVAL 1 DAY)", startTime, endTime);'+'\n')
                sb.append('            }'+'\n')
            else:
                sb.append(
                    '            if (!string.IsNullOrEmpty(' + row[3].lower() + '))'+'\n')
                sb.append('            {'+'\n')
                sb.append('                strWhere.AppendFormat(" and ' +
                          row[3] + ' = \'{0}\'", ' + row[3].lower() + ');'+'\n')
                sb.append('            }'+'\n')

    sb.append(''+'\n')
    sb.append('            var '+key.lower()+'Bll = new '+key+'BLL();'+'\n')
    sb.append('            var count = '+key.lower()+'Bll.GetCount(strWhere.ToString());'+'\n')
    sb.append('            var list = '+key.lower()+'Bll.GetList(strWhere.ToString(), pageSize, pageIndex, "*", "Id desc");'+'\n')
    sb.append(''+'\n')
    sb.append('            if (list != null && list.Count > 0)'+'\n')
    sb.append('            { '+'\n')
    sb.append('                return Json(new { code = 1, list, count });'+'\n')
    sb.append('            }'+'\n')
    sb.append('            return Json(new { code = 0, msg = "没有数据" });'+'\n')
    sb.append('        }'+'\n')

    fout = open(filepath + '/'+key+'-csht.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def clientht2(rows, key):
    sb = []    
    sb.append('@model WebUI.MiniSNSAdmin.Model.FriendViewModel'+'\n')
    sb.append('@{'+'\n')
    sb.append('    ViewBag.Title = "'+key+'";'+'\n')
    sb.append('    ViewBag.menuIndex = "10-2";'+'\n')
    sb.append('    Layout = "_BaseLayout.cshtml";'+'\n')
    sb.append('}'+'\n')
    sb.append('<style>'+'\n')
    sb.append('    .btn-margin {'+'\n')
    sb.append('        margin: 2px 0;'+'\n')
    sb.append('    }'+'\n')
    sb.append('</style>'+'\n')
    sb.append('<div id="app-view2" style=" display:none" v-show="isCreated">'+'\n')
    sb.append('    <el-form ref="form" :model="queryPara" label-width="80px" inline style="text-align: left;float:right;">'+'\n')
    sb.append('        <div>'+'\n')

    for row in rows:
        if row[13] == 'y':
            if row[4] == 'datetime':
                    sb.append('            <el-date-picker v-model="queryPara.'+ row[3].lower() +'" type="date" placeholder="选择日期"></el-date-picker>'+'\n')
            elif row[4] == 'int':
                    sb.append('            <el-input v-model="queryPara.'+ row[3].lower() +'" placeholder="请输入'+ row[2] +'" style="width:200px;"></el-input>'+'\n')
                    sb.append('            <el-select v-model="queryPara.'+ row[3].lower() +'" placeholder="请选择">'+'\n')
                    sb.append('                <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>'+'\n')
                    sb.append('            </el-select>'+'\n')
            else:            
                sb.append('            <el-input v-model="queryPara.'+ row[3].lower() +'" placeholder="请输入'+ row[2] +'" style="width:200px;"></el-input>'+'\n')

    sb.append('            <el-form-item>'+'\n')
    sb.append('                <el-button type="primary" @@click="search" size="small" icon="el-icon-search">搜索</el-button>'+'\n')
    sb.append('            </el-form-item>'+'\n')
    sb.append('        </div>'+'\n')
    sb.append('    </el-form>'+'\n')
    sb.append('    <el-table :data="list"'+'\n')
    sb.append('              border'+'\n')
    sb.append('              style="width:100%;"'+'\n')
    sb.append('              size="small"'+'\n')
    sb.append('              v-loading="loading">'+'\n')

    sb.append('        <el-table-column label="图片" min-width="100" align="center">'+'\n')
    sb.append('            <template slot-scope="scope">'+'\n')
    sb.append('                <img :src="scope.row.imgurl" style="width:140px;max-height:120px;" />'+'\n')
    sb.append('            </template>'+'\n')
    sb.append('        </el-table-column>'+'\n')
    for row in rows:
        if row[14] == 'y':
            sb.append('        <el-table-column label="'+ row[2] +'" prop="'+ row[3] +'" min-width="100" align="center"></el-table-column>'+'\n')

    
    sb.append('        <el-table-column label="操作" width="130" align="center">'+'\n')
    sb.append('            <template slot-scope="scope">'+'\n')    
    sb.append('                <el-button class="btn-margin" size="mini" @@click="switchPage(1,scope.row.Id)">编辑</el-button>'+'\n')
    sb.append('                <br />'+'\n')
    sb.append('                <el-button class="btn-margin" size="mini" @@click="del'+ key +'(scope.row.Id)">删除</el-button>'+'\n')
    sb.append('            </template>'+'\n')
    sb.append('        </el-table-column>'+'\n')
    sb.append('    </el-table>'+'\n')
    sb.append(''+'\n')
    sb.append('    <div style="margin-top:20px;display:none;" v-show="count>0">'+'\n')
    sb.append('        <el-pagination @@size-change="handleSizeChange"'+'\n')
    sb.append('                       @@current-change="handleCurrentChange"'+'\n')
    sb.append('                       :current-page="queryPara.pageIndex"'+'\n')
    sb.append('                       :page-sizes="[10, 20, 30, 40, 50]"'+'\n')
    sb.append('                       :page-size="10"'+'\n')
    sb.append('                       layout="total, sizes, prev, pager, next, jumper"'+'\n')
    sb.append('                       background'+'\n')
    sb.append('                       :total="count">'+'\n')
    sb.append('        </el-pagination>'+'\n')
    sb.append('    </div>'+'\n')
    sb.append(''+'\n')
    sb.append('    @*弹窗 '+ key +'*@'+'\n')
    sb.append('    <el-dialog :center="true" title="'+ key +'" :visible.sync="dialogVisible" width="70%">'+'\n')
    sb.append('        <div>           '+'\n')
    sb.append('            <el-row>'+'\n')
    sb.append('                <el-table :data="list2"'+'\n')
    sb.append('                          border'+'\n')
    sb.append('                          style="width: 100%"'+'\n')
    sb.append('                          size="small">'+'\n')
    sb.append('                    <el-table-column prop="UserId"'+'\n')
    sb.append('                                     label="用户ID"'+'\n')
    sb.append('                                     width="180">'+'\n')
    sb.append('                    </el-table-column>'+'\n')
    sb.append('                    <el-table-column prop="UserName"'+'\n')
    sb.append('                                     label="用户昵称"'+'\n')
    sb.append('                                     width="180">'+'\n')
    sb.append('                    </el-table-column>'+'\n')
    sb.append('                    <el-table-column prop="ApplyStrInfo"'+'\n')
    sb.append('                                     label="报名信息">'+'\n')
    sb.append('                    </el-table-column>                    '+'\n')
    sb.append('                    <el-table-column prop="AddTime"'+'\n')
    sb.append('                                     label="报名时间"'+'\n')
    sb.append('                                     width="180">'+'\n')
    sb.append('                    </el-table-column>'+'\n')
    sb.append('                </el-table>'+'\n')
    sb.append('            </el-row>'+'\n')
    sb.append('        </div>'+'\n')
    sb.append('        <div slot="footer" class="dialog-footer">'+'\n')
    sb.append('            <el-button @@click="dialogVisible = false" size="small">关闭</el-button>'+'\n')
    sb.append('        </div>'+'\n')
    sb.append('    </el-dialog>'+'\n')
    sb.append('</div>'+'\n')
    sb.append('<script type="text/javascript">'+'\n')
    sb.append('    var vm = new Vue({'+'\n')
    sb.append('        el: "#app-view2",'+'\n')
    sb.append('        data: {'+'\n')
    sb.append('            mid:@Model.Minisns.Id,'+'\n')
    sb.append('            switchBtn: false,'+'\n')
    sb.append('            queryPara: {'+'\n')
    sb.append('                pageIndex: 1,'+'\n')
    sb.append('                pageSize: 10,'+'\n')
    sb.append('                title: ""'+'\n')
    sb.append('            },'+'\n')
    sb.append('            queryPara2: {'+'\n')
    sb.append('                pageIndex: 1,'+'\n')
    sb.append('                pageSize: 30,'+'\n')
    sb.append('                aId: 0'+'\n')
    sb.append('            },'+'\n')
    sb.append('            activity: {'+'\n')
    sb.append('                timerange:"",'+'\n')
    sb.append('            },'+'\n')
    sb.append('            isCreated: false,'+'\n')
    sb.append('            timeArray: "",'+'\n')
    sb.append('            list: [],'+'\n')
    sb.append('            list2: [],'+'\n')
    sb.append('            count: 0,'+'\n')
    sb.append('            dialogVisible: false,'+'\n')
    sb.append('            msgText: "",'+'\n')
    sb.append('            loading: false,'+'\n')
    sb.append('            loading2: false'+'\n')
    sb.append('        },'+'\n')
    sb.append('        methods: {'+'\n')
    sb.append('            loadData() {'+'\n')
    sb.append('                this.loading = true;'+'\n')
    sb.append('                $.post("/friendajax/get'+ key.lower() +'list/" + this.mid, this.queryPara, function (res) {'+'\n')
    sb.append('                    if (res.code === 1) {'+'\n')
    sb.append('                        if (vm.queryPara.pageIndex === 1) {'+'\n')
    sb.append('                            vm.list = [];'+'\n')
    sb.append('                        }'+'\n')
    sb.append('                        vm.list = vm.list.concat(res.data.list || []);'+'\n')
    sb.append('                        vm.count = res.data.count;'+'\n')
    sb.append('                        vm.sortList(1);'+'\n')
    sb.append('                    } else {'+'\n')
    sb.append('                        vm.$message({ showClose: true, message: res.msg, type: "error" });'+'\n')
    sb.append('                    }'+'\n')
    sb.append('                    vm.loading = false;'+'\n')
    sb.append('                });'+'\n')
    sb.append('            },'+'\n')
    sb.append('            handleSizeChange(pageSize) {'+'\n')
    sb.append('                if (pageSize == this.queryPara.pageSize) return;'+'\n')
    sb.append('                this.list = [];'+'\n')
    sb.append('                this.queryPara.pageSize = pageSize;'+'\n')
    sb.append('                this.search();'+'\n')
    sb.append('            },'+'\n')
    sb.append('            handleCurrentChange(pageIndex) {'+'\n')
    sb.append('                if (pageIndex == this.queryPara.pageIndex) return;'+'\n')
    sb.append('                this.list = [];'+'\n')
    sb.append('                this.queryPara.pageIndex = pageIndex;'+'\n')
    sb.append('                this.loadData();'+'\n')
    sb.append('            },'+'\n')
    sb.append('            search() {'+'\n')
    sb.append('                this.list = [];'+'\n')
    sb.append('                this.queryPara.pageIndex = 1;'+'\n')
    sb.append('                this.loadData();'+'\n')
    sb.append('            },'+'\n')
    sb.append('            switchPage(type, id) {'+'\n')
    sb.append('                if (type == 1) {'+'\n')
    sb.append('                    location.href = "/friend/post'+ key.lower() +'/" + this.mid + "?type=a&oid=" + id;'+'\n')
    sb.append('                } else {'+'\n')
    sb.append('                    location.href = "/friend/'+ key.lower() +'/" + this.mid;'+'\n')
    sb.append('                }'+'\n')
    sb.append('            },'+'\n')
    sb.append('            convertData(time) {'+'\n')
    sb.append('                if (time == undefined) {'+'\n')
    sb.append('                    return "";'+'\n')
    sb.append('                }'+'\n')
    sb.append('                var date = new Date(parseInt(time.substr(6, 13))); //时间戳为10位需*1000，时间戳为13位的话不需乘1000'+'\n')
    sb.append('                var y = date.getFullYear();'+'\n')
    sb.append('                var m = date.getMonth() + 1;'+'\n')
    sb.append('                m = m < 10 ? ("0" + m) : m;'+'\n')
    sb.append('                var d = date.getDate();'+'\n')
    sb.append('                d = d < 10 ? ("0" + d) : d;'+'\n')
    sb.append('                var h = date.getHours();'+'\n')
    sb.append('                h = h < 10 ? ("0" + h) : h;'+'\n')
    sb.append('                var minute = date.getMinutes();'+'\n')
    sb.append('                var second = date.getSeconds();'+'\n')
    sb.append('                minute = minute < 10 ? ("0" + minute) : minute;'+'\n')
    sb.append('                second = second < 10 ? ("0" + second) : second;'+'\n')
    sb.append('                var ntime = y + "-" + m + "-" + d + " " + h + ":" + minute;'+'\n')
    sb.append('                if (ntime == "1950-04-24" || ntime == "0001-01-01") {'+'\n')
    sb.append('                    return "------";'+'\n')
    sb.append('                }'+'\n')
    sb.append('                return ntime;'+'\n')
    sb.append('            },'+'\n')
    sb.append('            del'+ key +'(id) {'+'\n')
    sb.append('                var item = this.list.find(function (o) {'+'\n')
    sb.append('                    return o.Id == id;'+'\n')
    sb.append('                });'+'\n')
    sb.append('                if (item) {'+'\n')
    sb.append('                    var str = "确定删除该数据?";'+'\n')
    sb.append('                    if (item.State == 2) {'+'\n')
    sb.append('                        str = "继续确定删除该活动?";'+'\n')
    sb.append('                    } '+'\n')
    sb.append('                    this.$confirm(str, "提示", {'+'\n')
    sb.append('                        confirmButtonText: "确定",'+'\n')
    sb.append('                        cancelButtonText: "取消",'+'\n')
    sb.append('                        type: "warning"'+'\n')
    sb.append('                    }).then(() => {'+'\n')
    sb.append('                        $.post("/friendajax/delete'+ key.lower() +'/" + vm.mid, { oid: id }, function (data) {'+'\n')
    sb.append('                            if (data.isok) {'+'\n')
    sb.append('                                vm.$message({'+'\n')
    sb.append('                                    message: "已删除",'+'\n')
    sb.append('                                    type: "success"'+'\n')
    sb.append('                                });'+'\n')
    sb.append('                                vm.list.splice(vm.list.indexOf(item),1);'+'\n')
    sb.append('                            } else {'+'\n')
    sb.append('                                vm.$message("删除失败");'+'\n')
    sb.append('                            }'+'\n')
    sb.append('                        });'+'\n')
    sb.append('                    }).catch(() => {'+'\n')
    sb.append('                        '+'\n')
    sb.append('                    });                    '+'\n')
    sb.append('                }'+'\n')
    sb.append('            }'+'\n')
    sb.append('        },'+'\n')
    sb.append('        created() {'+'\n')
    sb.append('            this.isCreated = true;'+'\n')
    sb.append('        },'+'\n')
    sb.append('        mounted() {'+'\n')
    sb.append('            this.loadData();'+'\n')
    sb.append('        }'+'\n')
    sb.append('    });'+'\n')
    sb.append('</script>'+'\n')
    sb.append(''+'\n')   

    fout = open(filepath + '/'+key+'-clientht2.txt', "w", encoding='utf-8')
    fout.writelines(sb)
    fout.close()

def serverht2(rows, key):
    sb = []
    

    fout = open(filepath + '/'+key+'-csht2.txt', "w", encoding='utf-8')
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

    # 前端html
    client(items, key)

    # 前端cs
    server(items, key)

    # 后端html
    clientht(items, key)
    
    # 后端cs
    serverht(items, key)

    # 后端html
    clientht2(items, key)
    
    # 后端cs
    serverht2(items, key)

print('end')
