# -*- coding: utf-8 -*-

from selenium.webdriver.firefox.webdriver import WebDriver

b = WebDriver()

b.get("http://localhost:8000/apply/")

# 填写姓名
b.find_element_by_id("id_name").send_keys(u'蒋文林')
# 性别
gender = b.find_element_by_name("gender")
gender.click()

#b.close()