# from selenium import webdriver
# driver = webdriver.Firefox(executable_path = r'D:\geckodriver\geckodriver.exe')
# driver.get("http://www.santostang.com/2018/07/04/hello-world/")


#!/usr/bin/python
#coding:UTF-8

from selenium import webdriver
# from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

# 控制 css
fp = webdriver.FirefoxProfile()
fp.set_preference("permissions.default.stylesheet",2)

# 限制图片的加载
fp.set_preference("permissions.default.image",2)

#把上述地址改成你电脑中geckodriver.exe程序的地址
driver = webdriver.Firefox(firefox_profile=fp, executable_path = r'D:\geckodriver\geckodriver.exe')

# 隐性等待，最长等20秒
driver.implicitly_wait(20)

#使用selenium打开浏览器和一个网页
driver.get("https://zh.airbnb.com/s/Shenzhen--China?page=1")

#而selenium grid根据测试脚本构建的DesiredCapabilities参数来决定将您的测试脚本分发到哪台机器或设备进行测试
#本质就是基于selenium grid 构建分布式自动化测试
# caps=webdriver.DesiredCapabilities().FIREFOX
#Marionette是Mozilla GeCo引擎的自动化驱动程序，它可以远程控制GECKO平台的UI或内部JavaScript，如Firefox。
# 它可以控制Chrome（即菜单和功能）或内容（网页加载在浏览上下文中），提供高级别的控制和复制用户动作的能力。
# 除了在浏览器上执行操作之外，Marionette程序还可以读取DOM的属性和属性。
# caps["marionette"]=True
#把上述地址改成你电脑中Firefox程序的地址
# binary=FirefoxBinary(r'D:\firefox\Firefox-latest.exe')
#用 selenium 的 driver 来启动 firefox
# driver=webdriver.Firefox(firefox_binary=binary,capabilities=caps)
#在虚拟浏览器中打开 Airbnb 页面
# driver.get("https://zh.airbnb.com/s/Shenzhen--China?page=1")

#找到页面中所有的出租房
rent_list=driver.find_elements_by_css_selector('div._tlfe97v')
#对于每一个出租房
for index,eachhouse in enumerate(rent_list):
    #处理程序中的异常,可以把多个 except 语句连接在一起, 处理一个 try 块中可能发生的多种异常,尝试执行 try 子句, 如果没有错误, 忽略所有的 except 从句继续执行.
    #找到评论数量
    try:
        comment=eachhouse.find_element_by_css_selector('span._69pvqtq')
        comment=comment.text
    except:
        comment = 0

    #找到价格
    prices=eachhouse.find_element_by_css_selector('._1dfubau0>._1dfubau0')
    #L[0:3]表示，从索引0开始取，直到索引3为止，但不包括索引3。即索引0，1，2，正好是3个元素。
    price=prices.text
    if (price!=''):
        price01=price.split('￥',-1)[1]
    else:
        print(index)
        print('这里获取了页面上不可见的隐藏的内容，所以下面会报错')
        price01='0'

    #找到名称
    name=eachhouse.find_element_by_css_selector('div._qhtkbey')
    name=name.text

    #找到房屋类型，大小
    try:
        details=eachhouse.find_elements_by_css_selector('span._fk7kh10>span')
        details=details[0].text
        house_type=details.split('·',-1)[0]
        bed_number=details.split('·',-1)[1]
    except:
        house_type=''
        bed_number=''

    print (comment,price01,name,house_type,bed_number)

    
    

















