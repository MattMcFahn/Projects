# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 19:01:25 2019

@author: mattm
"""

# This is a pretty weak exploratory code for now - to pull economist stories
# No extra submodules are yet used to prevent breakdown on errors
# Still not fully worked out

from selenium import webdriver

# Lets open up our browser and take a look at the economist
driver = webdriver.Chrome("C:/Users/mattm/Documents/local_pyth_config/chromedriver.exe")
driver.get("https://www.economist.com/")

# Inspect the html of the full page - Not necessary
html = driver.page_source

test = driver.find_element_by_xpath('//*[@id="content"]/section[1]/div/div[1]/div[1]/div[1]/h3/a')
a = test.text
#Write something to see full html as text for this element.

# Xpath navigation to news analysis (top couple)
ele__news_analysis__ = driver.find_element_by_xpath('//*[@id="content"]/section[1]/div/div[1]')
news_ana_text = ele__news_analysis__.get_attribute('outerHTML') #Show the HTML

ele__na_children__ = ele__news_analysis__.find_elements_by_xpath('//*[@id="content"]/section[1]/div/div[1]/div')
# Drop irrelevant 'related' story
del ele__na_children__[1] 

# Still need to figure out how to navigate the tree from here properly to get a couple levels down to pull out the desired stories
# See the webdocs for selenium.webdriver.remote.webelement objects for useful info on how to work with these

# Xpath navigation to highlights
ele__highlights__ = driver.find_element_by_xpath('//*[@id="content"]/section[1]/div/div[2]')

# Xpath navigation to today picks
ele__today_sele__ = driver.find_element_by_xpath('//*[@id="content"]/section[1]/div/div[3]')

driver.close()
