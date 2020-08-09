//注入
var vueMixin = {
    data: {
        types: "default", 
        mImgType: "default",
        mImgCount: 1,
        mImgList: [],
        cityInfoId: 0,
        uploaderObj: {
            checkupload: 0,
            accessid: '',
            accesskey: '',
            host: '',
            vzanHost: '',
            policyBase64: '',
            signature: '',
            callbackbody: '',
            filename: '',
            key: '',
            expire: 0,
            g_object_name: '',
            g_object_name_type: 'random_name',//local_name  random_name
            timestamp: Date.parse(new Date()) / 1000,
            now: Date.parse(new Date()) / 1000,
            videopercent:0
        },
        smsInfo: {
            isVaildPhone: true,
            isShowVaild: false,
            constTime: 60,
            time: 60,
            phone: '',
            vcode: ''
        }       
    },
    methods: {
        convertTime: function (time) {
            var date = new Date(parseInt(time.substr(6, 13))); //时间戳为10位需*1000，时间戳为13位的话不需乘1000
            var y = date.getFullYear();
            var m = date.getMonth() + 1;
            m = m < 10 ? ('0' + m) : m;
            var d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            var h = date.getHours();
            h = h < 10 ? ('0' + h) : h;
            var minute = date.getMinutes();
            var second = date.getSeconds();
            minute = minute < 10 ? ('0' + minute) : minute;
            second = second < 10 ? ('0' + second) : second;
            return y + '-' + m + '-' + d + ' ' + h + ':' + minute + ':' + second;
        },
        convertDate: function (time) {
            var date = new Date(parseInt(time.substr(6, 13))); //时间戳为10位需*1000，时间戳为13位的话不需乘1000
            var y = date.getFullYear();
            var m = date.getMonth() + 1;
            m = m < 10 ? ('0' + m) : m;
            var d = date.getDate();
            d = d < 10 ? ('0' + d) : d;
            var h = date.getHours();
            h = h < 10 ? ('0' + h) : h;
            var minute = date.getMinutes();
            var second = date.getSeconds();
            minute = minute < 10 ? ('0' + minute) : minute;
            second = second < 10 ? ('0' + second) : second;
            return y + '-' + m + '-' + d;
        },
        getQueryString(name, def) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
            var r = window.location.search.substr(1).match(reg);
            if (r != null)
                return unescape(r[2]);
            return def || "";
        },
        //上传图片
        uploadImage(type) {
            var self = this;
            var totalCount = self.mImgCount;
            var _imgcount = totalCount - self.mImgList.length;
            if (_imgcount <= 0) {
                TipMsg("最多上传" + totalCount + "张图片");
                return;
            }
            if (!type) type = this.mImgType;
            wx.chooseImage({
                count: _imgcount > 9 ? 9 : _imgcount,
                success: function (res) {
                    //记录选择的图片
                    var images = {
                        localId: [],
                        serverId: []
                    };
                    images.localId = res.localIds;
                    var i = 0, length = images.localId.length, flag = 0;
                    images.serverId = [];
                    //上传图片
                    function upload() {
                        wx.uploadImage({
                            localId: images.localId[i],
                            success: function (res) {
                                i++;
                                images.serverId.push(res.serverId);
                                $.ajax({
                                    type: "post",
                                    url: "/sc/uploadcityimagepost-0",
                                    data: { mediaId: res.serverId, itemType: 2, cityInfoId: self.cityInfoId, awm: 0 },
                                    dataType: "JSON",
                                    success: function (data) {
                                        if (data && data.id != -1) {
                                            self.mImgList.push({ id: data.id, filepath: data.path });
                                            TipMsg("上传成功");
                                            flag++;
                                            //全部上传完成
                                            if (flag == length) {
                                                self.uploadComplete(type, self.mImgList);
                                            }
                                        } else {
                                            TipMsg(data.Msg)
                                        }
                                    },
                                    error: function () {
                                        TipMsg("error");
                                    }
                                });
                                if (i < length) {
                                    upload();
                                }
                            },
                            fail: function (res) {
                                TipMsg("图片上传失败");
                            }
                        });
                    }
                    upload();
                },
                fail: function (res) {
                    TipMsg("请在微信端打开");
                }
            });
        },
        //上传完成，可以重写方法
        uploadComplete(type, imgs) {
        },
        //上传视频
        initUploader() {
            var self = this;
            function send_request() {
                var xmlhttp = null;
                if (window.XMLHttpRequest) {
                    xmlhttp = new XMLHttpRequest();
                }
                else if (window.ActiveXObject) {
                    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
                }
                if (xmlhttp != null) {
                    serverUrl = '/sc/InitUpload'
                    xmlhttp.open("POST", serverUrl, false);
                    xmlhttp.send(null);
                    return xmlhttp.responseText
                }
                else {
                    alert("Your browser does not support XMLHTTP.");
                }
            };
            function get_signature() {
                //可以判断当前expire是否超过了当前时间,如果超过了当前时间,就重新取一下.3s 做为缓冲
                self.uploaderObj.now = self.uploaderObj.timestamp = Date.parse(new Date()) / 1000;
                if (self.uploaderObj.expire < self.uploaderObj.now + 3) {
                    body = send_request()
                    var obj = eval("(" + body + ")");
                    self.uploaderObj.host = obj['host'];
                    self.uploaderObj.vzanHost = obj['ossfiledomain'];
                    self.uploaderObj.policyBase64 = obj['policy'];
                    self.uploaderObj.accessid = obj['accessid'];
                    self.uploaderObj.signature = obj['signature'];
                    self.uploaderObj.expire = parseInt(obj['expire']);
                    self.uploaderObj.callbackbody = obj['callback'];
                    self.uploaderObj.key = obj['dir'];
                    return true;
                }
                return false;
            };
            function random_string(len) {
                len = len || 32;
                var chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
                var maxPos = chars.length;
                var pwd = '';
                for (i = 0; i < len; i++) {
                    pwd += chars.charAt(Math.floor(Math.random() * maxPos));
                }
                return pwd;
            };
            function get_suffix(filename) {
                pos = filename.lastIndexOf('.')
                suffix = ''
                if (pos != -1) {
                    suffix = filename.substring(pos)
                }
                return suffix;
            };
            function calculate_object_name(filename) {
                if (self.uploaderObj.g_object_name_type == 'local_name') {
                    self.uploaderObj.g_object_name += "${filename}"
                }
                else if (self.uploaderObj.g_object_name_type == 'random_name') {
                    suffix = get_suffix(filename)
                    self.uploaderObj.g_object_name = self.uploaderObj.key + random_string(20) + suffix
                }
                return ''
            };
            function get_uploaded_object_name(filename) {
                if (self.uploaderObj.g_object_name_type == 'local_name') {
                    tmp_name = self.uploaderObj.g_object_name
                    tmp_name = tmp_name.replace("${filename}", filename);
                    return tmp_name
                }
                else if (self.uploaderObj.g_object_name_type == 'random_name') {
                    return self.uploaderObj.g_object_name
                }
            };
            function set_upload_param(up, filename, ret) {
                if (ret == false) {
                    ret = get_signature()
                }
                self.uploaderObj.g_object_name = self.uploaderObj.key;
                if (filename != '') {
                    suffix = get_suffix(filename)
                    calculate_object_name(filename)
                }
                new_multipart_params = {
                    'key': self.uploaderObj.g_object_name,
                    'policy': self.uploaderObj.policyBase64,
                    'OSSAccessKeyId': self.uploaderObj.accessid,
                    'success_action_status': '200', //让服务端返回200,不然，默认会返回204
                    'callback': self.uploaderObj.callbackbody,
                    'signature': self.uploaderObj.signature,
                };
                console.log("upload", up);
                up.setOption({
                    'url': self.uploaderObj.host,
                    'multipart_params': new_multipart_params
                });
                up.start();
            }
            var uploader = new plupload.Uploader({
                runtimes: 'html5,flash,silverlight,html4',
                browse_button: 'savevideofile',
                container: document.getElementById('div-video'),
                url: 'https://oss.aliyuncs.com',
                filters: {
                    mime_types: [
                        {
                            title: "video files",
                            extensions: "mp4,mpeg4,mov,avi,wmv,odd,3gp"
                        },
                    ],
                    max_file_size: '100mb', //最大只能上传10mb的文件
                    prevent_duplicates: false //不允许选取重复文件
                },
                init: {
                    FilesAdded: function (up, files) {
                        console.log("up", up)
                        self.uploaderObj.checkupload = 1;
                        plupload.each(files, function (file) {
                            self.uploaderObj.videopercent = 0;
                            set_upload_param(up, '', false);
                            console.log('Added');
                        });
                    },
                    BeforeUpload: function (up, file) {
                        set_upload_param(up, file.name, true);
                        console.log('BeforeUpload');
                    },
                    UploadProgress: function (up, file) {
                        self.uploaderObj.videopercent = file.percent;
                        console.log('UploadProgress');
                    },
                    FileUploaded: function (up, file, info) {
                        if (info.status == 200) {
                            console.log(file);
                            self.uploaderObj.checkupload = 2;
                            var e = get_uploaded_object_name(file.name), g;
                            var url = self.uploaderObj.vzanHost + e;
                            self.uploadVideoCompleted(url);
                            console.log(e);
                            self.uploaderObj.videopercent = 0;
                        } else {
                            self.uploaderObj.videopercent = info.response;
                        }
                        console.log('Uploaded');
                    },
                    Error: function (up, err) {
                        if (err.code == -600) {
                            TipMsg("视频大小不能超过100M");
                        }
                        else if (err.code == -601) {
                            TipMsg("只能上传mp4,mov格式视频");
                        }
                        else if (err.code == -602) {
                            TipMsg("这个文件已经上传过一遍了");
                        }
                        else {
                            TipMsg("err_code:" + err.code + err.response);
                        }
                        console.log('Error');
                    }
                }
            });
            uploader.init();
        },
        //上传完成，可以重写方法
        uploadVideoCompleted(url) {

        },
        isPhone(phone) {
            var bValidate = RegExp(/^(0|86|17951)?(13[0-9]|15[012356789]|18[0-9]|17[0-9]|19[0-9]|14[57])[0-9]{8}$/).test(phone);
            if (bValidate) {
                return true;
            } else {
                return false;
            }
        },
        //验证码
        getCode() {
            var self = this;
            if (self.smsInfo.time !== self.smsInfo.constTime) {
                return;
            }
            var phone = self.smsInfo.phone;
            if (phone === '' || !self.isPhone(phone)) {
                TipMsg("请输入正确的手机号");
                return;
            }
            $.post("/store/senduserauth", { id: self.cityInfoId, tel: phone, sendtype: 8 }, function (data) {
                if (data.isok) {
                    self.countNum();
                }
                TipMsg(data.Msg);
            });
        },
        //倒计时
        countNum() {
            var self = this;
            var timer = setInterval(function () {
                if (self.smsInfo.time > 0) {
                    self.smsInfo.time--;
                } else {
                    self.smsInfo.time = 60;
                    clearInterval(timer);
                }
            }, 1000);
        },
        vaildCode() {
            var self = this;
            if (self.smsInfo.phone == '' || self.smsInfo.vcode == '') {
                TipMsg("请输入手机号和验证码");
                return;
            }
            $.post("/store/submitauth", { tel: self.smsInfo.phone, authCode: self.smsInfo.vcode }, function (data) {
                if (data.isok) {
                    self.smsInfo.isVaildPhone = true;
                    self.smsInfo.isShowVaild = false;
                }
                TipMsg(data.Msg);
            });
        },
        isNullOrEmpty(str) {
            if (str == '' || str == null) {
                return true;
            }
            return false;
        },
        
    }
};