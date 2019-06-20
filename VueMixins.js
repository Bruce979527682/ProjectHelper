//注入
var vueMixin = {
    data: {
        types: "default",        
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
        switchTabWin(url, title) {
            $("#min_title_list > li.active > span", window.parent.document).html(title);
            $("#min_title_list > li.active > span", window.parent.document).data('href', url);
            location.href = url;
        }
    }
};