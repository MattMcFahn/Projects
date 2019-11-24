# -*- coding: utf-8 -*-
"""
Backup script containing functions to pull most viewed stories from news sites

News sites currently covered:
    - The Guardian;
    - The Times;
    - The Economist;
    - The Financial Times;
    - The Independent.
    
NOTE: A key 'to-do' will be to go back and extract extra info - i.e. leading paras from the stories, and images
and so forth. To build and kind of decent looking front end, this will all be needed.

BIG NOTE: Need to start randomising User-Agents and IP Addresses to stop getting blocked from scraping.
      This webpage https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
      Is useful in teaching how to do this.

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
import pandas as pd


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
    if get(url, stream=True).status_code == 404:
        try:
            with closing(get(url, stream=True, headers={'User-Agent': 'Custom'})) as resp:
                if is_good_response(resp):
                    return resp.content
                else:
                    return None
        except RequestException as e:
            error_message = 'Error during requests to {0} : {1}'.format(url, str(e))
            print(error_message)
            log_error(error_message)
            return None
    else:
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
    
    
    guardian_extract = pd.DataFrame()
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
        guardian_frame = pd.DataFrame(data = ['Guardian','Most viewed - News',str(headline), str(link)]).T
        guardian_extract = guardian_extract.append(guardian_frame)
    for i in range(0,len(long_read_html_chunk)):
        headline = guardian_html_chunk[i].a.span.span.get_text()
        link = guardian_html_chunk[i].a['href']
        guardian_frame = pd.DataFrame(data = ['Guardian','Most viewed - Longread',str(headline), str(link)]).T
        guardian_extract = guardian_extract.append(guardian_frame)
    guardian_extract = guardian_extract.rename(columns = {0:'Source', 1:'Type', 2:'Headline', 3:'Link'})
    return(guardian_extract)
    
# The Times
def retrieve_times_world_page():
    """
    None -> pd.DataFrame
    Returns information about the top stories on The Times' homepage.
    NOTE: This could probably do with being tidied. The Times source code has a weird layout
    """
    times_html_RAW = simple_get(r'https://www.thetimes.co.uk/#section-world')
    times_html = BeautifulSoup(times_html_RAW, 'html.parser')
    
    temp = times_html.body.section.div.section
    temp = temp.findAll("div", {"class":"SliceCollection"})[0]
    times_html_extr = temp.findAll("div", {"class":"Slice"})[0:2]
        
    times_extract = pd.DataFrame()
    for i in range(0,len(times_html_extr)):
        curr_chunk = times_html_extr[i].contents #NOTE: .contents finds the children of a node! :)
        for j in range(0,len(curr_chunk)):
            #full_text = curr_chunk[j].get_text() # Unused for now - We can extract intro para text here (for i=0 only)
            if i == 0:
                headline = curr_chunk[j].a.get_text() #First section of the nested for-loop has a diff structure
            else:
                headline = curr_chunk[j].get_text()
            link = curr_chunk[j].a['href']
            times_frame = pd.DataFrame(data = ['Times', 'Headlines', str(headline), str(link)]).T
            times_extract = times_extract.append(times_frame)
    times_extract = times_extract.rename(columns = {0:'Source', 1:'Type', 2:'Headline', 3:'Link'})
    return(times_extract)


def retrieve_economist_most_viewed():
    """
    None -> pd.DataFrame
    Pulls out top 4 articles for now, and their links
    """
    economist_html_RAW = simple_get(r'https://www.economist.com/')
    economist_html = BeautifulSoup(economist_html_RAW, 'html.parser')


    temp = economist_html.body.div.div
    temp2 = temp.findAll('div', {"class": "standout-content"})[0].div.main.div.div.div.div.div.div.ul
    economist_html_extr = temp2.findAll('li')
    
    economist_extract = pd.DataFrame()
    for i in range(0,len(economist_html_extr)):
        curr_chunk = economist_html_extr[i]
        full_text = curr_chunk.get_text()
        text_extr_ele_1 = curr_chunk.findAll('span', {'class':'flytitle-and-title__flytitle'})[0].get_text()
        text_extr_ele_2 = curr_chunk.findAll('span', {'class':'flytitle-and-title__title'})[0].get_text()
        headline = text_extr_ele_1 +': \n' +text_extr_ele_2
        link = curr_chunk.article.a['href']
        economist_frame = pd.DataFrame(data = ['Economist', 'Headlines', str(headline), str(link)]).T
        economist_extract = economist_extract.append(economist_frame)
    economist_extract = economist_extract.rename(columns = {0:'Source', 1:'Type', 2:'Headline', 3:'Link'})
    return(economist_extract)
    
def retrieve_FT_most_viewed():
    """
    None -> pd.DataFrame
    Extracts the top 5 "most viewed" from the world home page, from the sidebar.
    """
    ft_html_RAW = simple_get(r'https://www.ft.com/world')
    ft_html = BeautifulSoup(ft_html_RAW, 'html.parser')
    ######### NOTE - These temps show the main ones, not sidebar where "most viewed is"
    #temp = ft_html.findAll('div', {'class' :'css-grid__container'})[0].div.div
    #temp2 = temp.findAll('div', {'class':'o-teaser__content'})
    #############
    
    ft_html_extr = ft_html.findAll('div', {'class' :'css-grid__sidebar-item'})[1].div.div
    temp = ft_html_extr.findAll('li')
    ft_extract = pd.DataFrame()
    for i in range(0,len(temp)):
        curr_chunk = temp[i]
        headline = curr_chunk.get_text()
        link = curr_chunk.div.div.div.a['href']
        ft_frame = pd.DataFrame(data = ['Financial Times', 'Most Viewed', str(headline), str(link)]).T
        ft_extract = ft_extract.append(ft_frame)
    ft_extract = ft_extract.rename(columns = {0:'Source', 1:'Type', 2:'Headline', 3:'Link'})
    return(ft_extract)

def retrieve_independent_top_stories():
    """
    None -> pd.DataFrame
    Extracts top stories from homepage.
    """
    indep_html_RAW= simple_get(r'https://www.independent.co.uk')
    # NOTE - I had to mess with simple_get because requests.get(url) returns a 404. It's a weak fix for now.
    # This was because of independent.co.uk blocking User-Agent as python.
    # Longer term, need to randomise User-Agent and ID that are sent. It'd be good if I could actually learn what is happening behind this!
    indep_html = BeautifulSoup(indep_html_RAW, 'html.parser')

    indep_html_cut = indep_html.body.section    
    
    indep_html_extr_8_block = indep_html_cut.findAll('div', {'class':'eight-articles-dmpu position-left'})[0]
    indep_html_top = indep_html_cut.findAll('div', {'class':'splash-row'})[0]
    indep_html_extr = [indep_html_extr_8_block, indep_html_top]
    # Have given up for now - too bored doing the same old scraping! :) 
    
    
    
##################################################################################
# Functions to pull from webpages - END
##################################################################################