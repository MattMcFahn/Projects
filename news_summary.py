# -*- coding: utf-8 -*-
"""
This script is designed to run as a background task (via the Task Scheduler app). It tracks top stories from each day through the week from several news sites.
It will then host the information on the web so that a summary of each week can be viewed. (TODO)
A weekly email alert with top stories will also be sent. (TODO)

News sites currently covered:
    - The Guardian; The Times & Sunday Times; The Economist; The Financial Times; The Independent.

TO DO (short term):
    - Build out cleaning process to format data for sending and displaying;
    - Build in error warnings & stats;
    - Build front end of notification & web display.

TO DO (long term):
    - Build functions & functionality to extract the images, and first three paras of the article;
    - Review and refine popularity tags and stats to implement smart searching;
    - Figure out when sites are updated and time stamp information;
    - Pull key info from retrievals;
    - Sentiment analysis of articles;
    - Test whether factor (cluster) analysis groups the newspaper articles as you'd expect;
    - Build higher quality front end.
    
@author: Matt McFahn
"""

############## Import libraries
import extract_news # Self authored script - using BeautifulSoup, requests, closing, pandas
import pandas as pd # For data storage


##################################################################################
# Import html data from several webpages
##################################################################################

guardian_extract = extract_news.retrieve_guardian_most_viewed()
times_extract = extract_news.retrieve_times_world_page()
economist_extract = extract_news.retrieve_economist_most_viewed()
ft_extract = extract_news.retrieve_FT_most_viewed()
# indep_extract = extract_news.retrieve_independent_top_stories()

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


