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
    return (resp.status_code == 200 
            and content_type is not None 
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


