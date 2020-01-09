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
####### Within local repo
import extract_news # Front end - Extract. Dependencies = BeautifulSoup, requests, closing, pandas
import postgres_helper as pg_help # Back end - Load. Dependencies = config (local), psycopg2
####### Third party
import pandas as pd # For data storage
import smtplib # For sending emails, which follow the SMTP protocol



##################################################################################
# Function to retrieve news info (Extract & Transform)
##################################################################################
def retreive_daily_news_summary():
    news_list_df = [] #Initalise blank list to append to
    try:
        guardian_extract = extract_news.retrieve_guardian_most_viewed()
        news_list_df += [guardian_extract]
    except:
        print('<<<Issue extracting Guardian data. Check functionality>>>')
    try:    
        times_extract = extract_news.retrieve_times_world_page()
        news_list_df += [times_extract]
    except:
        print('<<<Issue extracting Times data. Check functionality>>>')
    try:
        economist_extract = extract_news.retrieve_economist_most_viewed()
        news_list_df += [economist_extract]
    except:
        print('<<<Issue extracting Economist data. Check functionality>>>')
    try:
        ft_extract = extract_news.retrieve_FT_most_viewed()
        news_list_df += [ft_extract]
    except:
        print('<<<Issue extracting FT data. Check functionality>>>')
    
    # indep_extract = extract_news.retrieve_independent_top_stories()
    
    # Combine all
    news_df = pd.concat(news_list_df)
    # TODO - Add a check for any null values being pulled through and throw up error / warning
    news_df = news_df.rename(columns = {'Date & Time': 'datetime', 'Source': 'newssource', 
                                        'Type': 'article_type', 'Headline': 'headline', 'Link': 'weblink'}) 
                                        # Should really replace in the retrieve functions
    # Reset index
    news_df = news_df.reset_index(drop = True)
    # Add primary and (perhaps) foreign keys
    news_df['dated_article_key'] = news_df['datetime'] + ' | ' + news_df['newssource'] + ' | ' + news_df['headline']
    news_df['article_key'] = news_df['newssource'] + ' | ' + news_df['headline']
    return news_df

##################################################################################
# End of data extract & tranform
##################################################################################

##################################################################################
# Send weekly email
##################################################################################


def weekly_email_update():
    """
    Sends an email with the latest weekly server data pulled out, reminding me to jump onto the webpage.
    """
    # TODO - Properly write the ETL server routines so the following line can be uncommented
    # weekly_highlight_df = weekly_highlight()
    smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587) # Connect to outlooks stmp provider, 'smtp-mail.outlook.com'
    smtpObj.ehlo() # Say "hello" to the server
    smtpObj.starttls() # Connect to port 587 (TLS encryption)
    secret_password = input('''Please input your password to Yahoo email to send an automatic email.\n
                            The email is a news summary, being sent to yourself.''')
    smtpObj.login('mattmcfahn161@hotmail.co.uk', secret_password) #Log in to access email
    #Send the mail
    smtpObj.sendmail('mattmcfahn161@hotmail.co.uk','matthew.mcfahn@li.com',
                     '''SUbject: Weekly News Update\n
                     TODO: Fill out the body text of the weekly news email update, pulling in server data.\n\n
                     \n See the following webpage for the more regular news update: exaplewebpage@domain.com''')


##################################################################################
# Weekly email - end
##################################################################################


