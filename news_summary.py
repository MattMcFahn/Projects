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
guardian_html_RAW = simple_get(r'https://www.theguardian.com/world')
guardian_html = BeautifulSoup(guardian_html_RAW, 'html.parser')

# Using developer tools, we see we want the html slice where 'div class' = "tabs__content js-tabs-content"
# We might need to refine further, but for now we atleast select the chunk needed!
guardian_html_chunk = guardian_html.findAll("div", {"class": "tabs__content js-tabs-content"})

# cut_chunk gets the specific pieces that are needed but I still need to explore what it does
# It picks out the relevant elements, but also appears to select non-relevant elements too
cut_chunk = guardian_html.findAll("h3", { "class": "fc-item__title"})

viewing = [str(cut_chunk[i]) for i in range(0,len(cut_chunk))]


tester_chunk = guardian_html.findAll("li", {"class": "most-popular__item tone-news--most-popular fc-item--pillar-news"})
viewer_two = [str(tester_chunk[i]) for i in range(0,len(tester_chunk))]
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


