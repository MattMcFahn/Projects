# -*- coding: utf-8 -*-
"""
This script will run as a background task, to track top stories from each day through the week from several news sites.
It will then host the information on the web so that a summary of each week can be viewed.
A weekly email alert with top stories will also be sent.

News sites currently covered:
    - The Guardian;
    - The Times & Sunday Times;
    - The Economist;
    - The Financial Times;
    - The New York Times;
    - The Independent.

Created on Sun Nov 17 19:44:39 2019

@author: mattm

TO DO (short term):
    - Extract other info from the last 5 papers;
    - Build out cleaning and gathering process to send data to;
    - Implement as background process daily;
    - Build in error warnings & stats;
    - Build front end of notification & web display.

TO DO (long term):
    - Build functions & functionality to extract the images, and first three paras of the article;
    - Review and refine popularity tags and stats to implement smart searching;
    - Figure out when sites are updated and time stamp information;
    - Build higher quality front end.
    
"""

# Import libraries. 
# - requests: For HTTP requests (pulls html into a bytes data type for wrangling); 
# - BeautifulSoup: For webscraping. Works with bytes/html pulled via requests;
# - closing: For good practice to ensure closing of connections to webpage on exiting with commands.
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import extract_news


##################################################################################
# Import html data from several webpages
##################################################################################

guardian_extract = extract_news.retrieve_guardian_most_viewed()
times_extract = extract_news.retrieve_times_world_page()
economist_extract = extract_news.retrieve_economist_most_viewed()
ft_extract = extract_news.retrieve_FT_most_viewed()


###########################

##################################################################################
# End of data import section
##################################################################################





##################################################################################
# Update server information based on daily update. Also weekly email.
##################################################################################

# TODO - WRITE FRONT END CODE TO SET UP AND UPDATE GIVEN SERVER

##################################################################################
# End of server update code section
##################################################################################


