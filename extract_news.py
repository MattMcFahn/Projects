# -*- coding: utf-8 -*-
"""
Backup script containing functions to pull most viewed stories from news sites

News sites currently covered:
    - The Guardian;

Created on Fri Nov 22 09:43:18 2019

@author: Matthew.McFahn
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
# Set up supporting functions  - Finished
##################################################################################

##################################################################################
# Functions to pull from webpages
##################################################################################
        
# Guardian

def retrieve_guardian_most_viewed():
    """
    None -> List
    Returns a list of tagged headlines and news links from The Guardian's main page,
    extracting most viewed stories
    """
    guardian_html_RAW = simple_get(r'https://www.theguardian.com/world')
    guardian_html = BeautifulSoup(guardian_html_RAW, 'html.parser')
    
    # Using developer tools on the Guardian webpage, we see we want the section of html where 
    # 'li' - we have list items. And identified by "class" = "most-popular__item tone-news--most-popular fc-item--pillar-news"
    # However, this drops one "long read" included in the collection of 'Most viewed' articles. This one is also kept, seperately.
    guardian_html_chunk = guardian_html.findAll("li", {"class": "most-popular__item tone-news--most-popular fc-item--pillar-news"})
    long_read_html_chunk = guardian_html.findAll("li", {"class": "most-popular__item tone-feature--most-popular fc-item--pillar-news"})
    
    
    
    guardian_extract = []
    for i in range(0,len(guardian_html_chunk)):
        headline = guardian_html_chunk[i].a.span.span.get_text()
        link = guardian_html_chunk[i].a['href']
        # FOR LATER - PULL EXTRA INFO, WEBLINKS, TEXT ETC.
        # Probably want to write something as a seperate function - access guardian link
        # and pull any extra relevant info from there :)
        #temp_html_RAW = simple_get(link)
        #temp_html = BeautifulSoup(temp_html_RAW, 'html.parser')
        ##################### The above has been left in but should be called as sep function 
        # Would be good to extract (1) image, and (2) leading three paras. FOR A FUTURE BUILD
        guardian_extract += [['Most viewed - News',headline, link]]
    for i in range(0,len(long_read_html_chunk)):
        headline = guardian_html_chunk[i].a.span.span.get_text()
        link = guardian_html_chunk[i].a['href']
        guardian_extract += [['Most viewed - Longread',headline, link]]
    return(guardian_extract)
    
# The Times
def retrieve_times_world_page():
    times_html_RAW = simple_get(r'https://www.thetimes.co.uk/#section-world')
    times_html = BeautifulSoup(times_html_RAW, 'html.parser')
    times_html_extr = times_html.body.section.div.section
    
    times_html_chunk = times_html_extr.findAll("div", {"class":"Slice"})
    # Looking at dev tools, we only want first three eles
    times_html_ch_short = times_html_chunk[0:3]
    
    # Bit messy at the moment, but this pulls the first two needed (some duplication)!
    # Looks like we'll need nested for loops to traverse three branches :(
    times_tester = times_html_ch_short[0].div.findAll('div')
    times_tester_2 = times_tester.findAll('div')
    # Would iterate over i instead of 0 below
    testing = times_tester_2[0].div.h3
    for i in range(0,len(times_tester)):
        curr_chunk = times_html_ch_short[i].div.findAll('div')
        curr_chunk_list = curr_chunk.findAll('div')
        for j in 
        headline = curr_chunk.get_text()
        link = times_tester.a['href']
    
    list_times_text = [times_html_ch_short[i].get_text() for i in range(0,len(times_html_ch_short))]
    list_times_eles = [str(times_html_ch_short[i]) for i in range(0,len(times_html_ch_short))]
    for i in range(0,len(times_html_chunk))
    
##################################################################################
# Functions to pull from webpages - END
##################################################################################