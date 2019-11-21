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

errors = [] #Initialize string to store a log of errors that arise.

##################################################################################
# Set up supporting functions for main task
##################################################################################

def log_error(current_error):
    """
    (str) -> List addition
    Adds a current error onto the error log list.
    """
    global errors #Call in the global variable as we are about to modify it
    errors += [current_error]

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 #The HTML response status code for 'OK' is 200.
            and content_type is not None  # Non empty return
            and content_type.find('html') > -1)

def simple_get(url):
    """
    (str) -> str
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        error_message = 'Error during requests to {0} : {1}'.format(url, str(e))
        print(error_message)
        log_error(error_message)
        return None




##################################################################################
# Import html data from several webpages
##################################################################################

# TODO - WRITE CODE TO IMPORT PAGES FROM SITES


############################ Guardian
    #Pull html and pass to BeautifulSoup
guardian_html_RAW = simple_get(r'https://www.theguardian.com/world')
guardian_html = BeautifulSoup(guardian_html_RAW, 'html.parser')


# Using developer tools on the Guardian webpage, we see we want the section of html where 
# 'li' - we have list items. And identified by "class" = "most-popular__item tone-news--most-popular fc-item--pillar-news"
# However, this drops one "long read" included in the collection of 'Most viewed' articles. This one is also kept, seperately.
guardian_html_chunk = guardian_html.findAll("li", {"class": "most-popular__item tone-news--most-popular fc-item--pillar-news"})
long_read_html_chunk = guardian_html.findAll("li", {"class": "most-popular__item tone-feature--most-popular fc-item--pillar-news"})
type(guardian_html_chunk) #Displays the type as bs4.element.ResultSet

# EXPLORING DATA - TO REMOVE IN TIDYING
list_of_element_extr = [str(guardian_html_chunk[i]) for i in range(0,len(guardian_html_chunk))]
list_of_text_extr = [guardian_html_chunk[i].get_text() for i in range(0,len(guardian_html_chunk))]

str_of_element_extr = ''
str_of_text_extr = ''
for i in range(0, len(list_of_text_extr),1):
    str_of_element_extr += list_of_element_extr[i]+'\n\n'
    str_of_text_extr += list_of_text_extr[i]+'\n\n'

str_of_element_extr += '\n\n-------------------\n\n'+str(long_read_html_chunk)
str_of_text_extr += '-------------------\n\n'+long_read_html_chunk[0].get_text()
# The above give strings displaying the element, and text data extracted from the page
# EXPLORING DATA - TO REMOVE IN TIDYING

# A bit of exploring pulling out information:
guardian_html_chunk[0].a['href'] #THIS PULLS OUT THE WEBLINK FOR THE ARTICLE 
#(NOTE: .h3 or .a pulls out that tag. THINK OF THESE DATA STRUCTURES LIKE A TREE)
guardian_html_chunk[0].a
guardian_html_chunk[0].span #Check this - it picks the first span in the tree (too much for us)
guardian_html_chunk[0].a.span.span #Et viola! We have the element with the desired text. We have traversed the tree!
###################################

################################## Proper data pull out
guardian_extract = []
for i in range(0,len(guardian_html_chunk)):
    headline = guardian_html_chunk[i].a.span.span.get_text()
    link = guardian_html_chunk[i].a['href']
    # Probably want to write something as a seperate function - access guardian link
    # and pull any extra relevant info from there :)
    #temp_html_RAW = simple_get(link)
    #temp_html = BeautifulSoup(temp_html_RAW, 'html.parser')
    ##################### The above has been left in but should be called as sep function 
    # Would be good to extract (1) image, and (2) leading three paras. FOR A FUTURE BUILD
    guardian_extract += [[headline, link]]

############################ Guardian

##################################################################################
# End of data import section
##################################################################################






##################################################################################
# Extract specific information from html using BeautifulSoup
##################################################################################

# TODO - WRITE CODE FOR DATA EXTRACTION

##################################################################################
# End of data extraction section
##################################################################################






##################################################################################
# Transformation of extracted data into a useful format
##################################################################################

# TODO - WRITE CODE FOR ANY NECESSARY TRANSFORMATION

##################################################################################
# End of data transformation section
##################################################################################






##################################################################################
# Update server information based on daily update. Also weekly email.
##################################################################################

# TODO - WRITE FRONT END CODE TO SET UP AND UPDATE GIVEN SERVER

##################################################################################
# End of server update code section
##################################################################################


