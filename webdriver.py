from selenium import webdriver
driver = webdriver.Firefox(executable_path = r'D:\geckodriver\geckodriver.exe')
driver.get("http://www.santostang.com/2018/07/04/hello-world/")