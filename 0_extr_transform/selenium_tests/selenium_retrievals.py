# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 19:01:25 2019

@author: mattm
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Lets open up our browser and take a look at the economist
driver = webdriver.Chrome("C:/Users/mattm/Documents/local_pyth_config/chromedriver.exe")
driver.get("https://www.economist.com/")
