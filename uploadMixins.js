//注入
var uploadMixin = {
    data: {
        types: "default",
        count: 1,
        images: [],
        mid: 0,
        imgtype: 'default',
        imgposition:''
    },
    methods: {
        //上传图片
        uploadImage(type) {
            var self = this;
            var totalCount = this.count;
            var _imgcount = totalCount - this.images.length;
            if (_imgcount <= 0) {
                PopMsg("最多上传" + totalCount + "张图片");
                return;
            }
            if (!type) type = this.types;
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
                                    url: "/fajax/uploadImagesByWx",
                                    data: { mediaId: res.serverId, types: type, fid: self.mid },
                                    dataType: "JSON",
                                    success: function (data) {
                                        if (data && data.isok) {
                                            self.images.push({ id: data.Id, filepath: data.Msg });
                                            PopMsg("上传成功");
                                            flag++;
                                            //全部上传完成
                                            if (flag == length) {
                                                self.uploadComplete(type, self.images);
                                            }
                                        } else {
                                            PopMsg(data.Msg)
                                        }
                                    },
                                    error: function () {
                                        PopMsg("error");
                                    }
                                });
                                if (i < length) {
                                    upload();
                                }
                            },
                            fail: function (res) {
                                PopMsg("图片上传失败");
                            }
                        });
                    }
                    upload();
                },
                fail: function (res) {
                    PopMsg("请在微信端打开");
                }
            });
        },
        //上传完成，可以重写方法
        uploadComplete(type,imgs) {
        },
        //微信上传64位图片
        uploadBaseImage(type) {
            var self = this;
            var totalCount = this.count;
            var _imgcount = totalCount - this.images.length;
            if (_imgcount <= 0) {
                PopMsg("最多上传" + totalCount + "张图片");
                return;
            }
            if (!type) type = this.types;
            wx.chooseImage({
                count: _imgcount > 9 ? 9 : _imgcount,
                success: function (res) {
                    //记录选择的图片
                    var localId = res.localIds;
                    var i = 0, length = localId.length, flag = 0;
                    //上传图片
                    function upload() {
                        //console.log(localId[i], wx);
                        //获取本地图片
                        wx.getLocalImgData({
                            localId: localId[i],//图片的本地ID
                            success: function (res) {
                                i++;
                                var localData = res.localData;
                                console.log(localData)
                                if (localData.indexOf('data:image') != 0) {
                                    //判断是否有这样的头部                                               
                                    localData = 'data:image/jpeg;base64,' + localData
                                }
                                localData = localData.replace(/\r|\n/g, '').replace('data:image/jgp', 'data:image/jpeg')
                                //将base64图片路径传给后台然后返回我们一个全域名路径的图片，用于其它操作
                                var submitData = {
                                    base64String: localData,
                                    iscut: true,
                                    id: self.mid,
                                    type: self.imgtype,
                                    position: self.imgposition
                                };
                                $.ajax({
                                    type: "POST",
                                    url: "/fajax/uploadimgofmark",
                                    data: submitData,
                                    dataType: "json",
                                    success: function (data) {
                                        layer.closeAll();
                                        if (1 == data.code) {
                                            self.images.push({ id: null, filepath: data.url });
                                            flag++;
                                            //全部上传完成
                                            if (flag == length) {
                                                PopMsg("上传成功");
                                                self.uploadComplete(type, self.images);
                                            }
                                        } else {
                                            PopMsg('上传图片失败，请重新再试');
                                        }
                                    },
                                    error: function (XMLHttpRequest, textStatus, errorThrown) {
                                        layer.closeAll();
                                        PopMsg('上传图片失败，网络连接失败');
                                    }
                                });
                                if (i < length) {
                                    upload();
                                }
                            },
                            fail: function (res) {
                                PopMsg("获取图片失败");
                            }
                        });
                    }
                    upload();
                },
                fail: function (res) {
                    PopMsg("请在微信端打开");
                }
            });
        },
        uploadImage(type, baseImg) {
            var localData = baseImg.replace(/\r|\n/g, '').replace('data:image/jgp', 'data:image/jpeg');
            var self = this;
            //将base64图片路径传给后台然后返回我们一个全域名路径的图片，用于其它操作
            var submitData = {
                base64String: localData,
                iscut: true,
                id: self.mid,
                type: self.imgtype,
                position: self.imgposition
            };
            $.ajax({
                type: "POST",
                url: "/fajax/uploadimgofmark",
                data: submitData,
                dataType: "json",
                success: function (data) {
                    layer.closeAll();
                    if (1 == data.code) {
                        self.images.push({ id: null, filepath: data.url });
                        //PopMsg("上传成功");
                        self.uploadComplete(type, self.images);
                    } else {
                        PopMsg('上传图片失败，请重新再试');
                    }
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    layer.closeAll();
                    PopMsg('上传图片失败，网络连接失败');
                }
            });
        }

    }
};