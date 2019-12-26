# -*- coding: utf-8 -*-
"""
SQL helper to read and write to SQL 

Created on Thu Dec 26 15:56:16 2019

@author: mattm
"""

# ------------------------------------------------------------------------------------------------#

import psycopg2 as pg2
import config
 

##################################################################################
# Supporting functions
##################################################################################

def __cut_duplicate_primary_keys(dataframe, primary_key):
    """
    Dataframe -> Dataframe
    Functionality: Recursive logic
    
    Cuts duplicate rows from a dataframe based on a primary key, as specified
    If the whole record is non unique, but has a duplicated primary key:
        - A warning is issued;
        - Both entries are passed, with a ' (1)' appended to the second instance's primary key
    
    """
    dataframe['Row dupe'] = dataframe.duplicated()
    dataframe['Dupe primary'] = dataframe.duplicated(subset = primary_key)
    
    if all(not dataframe['Row dupe'][i] for i in range(0, len(dataframe))): # No row duplicates
        if all(not dataframe['Dupe primary'][i] for i in range(0, len(dataframe))): # No primary_key duplicates either
            pass 
            print('<<< No duplicates in data pulled>>')
        else: # All rows unique, but some primary keys duped
            dataframe.loc[dataframe['Dupe primary'] == True, [primary_key]] += [' (1)']
            print("<<<WARNING: Duplicate story pulled with some differences. Review today's upload>>>")
            pass
    else: # i.e. there was a full row duplicate, which is dropped
        dataframe = dataframe.loc[dataframe['Row Dupe'] == True]
        dataframe.drop(columns = {'Row dupe','Dupe primary'})
        __cut_duplicate_primary_keys(dataframe, primary_key) # Recursion on the function. Next call will have no row dupes
    
    deduped_df = dataframe.drop(columns = {'Row dupe','Dupe primary'})
    return deduped_df


##################################################################################
# Supporting functions - Close
##################################################################################



##################################################################################
# Main ETL routines
##################################################################################

def update_server(dataframe):
    """
    (Load routine) Updates the SQL server set up with data from the (daily) news extract.
    Postgres SQL database currently called news_summary, with the following tables:
        daily_headlines: primary key is: datetime | source | headline;
                         tracks the headlines pulled daily as unique rows for each instance
        headlines_unique: primary key is: source | headline;
                          keeps track of unique headlines appearing (and how often)
    
    This function may be superseded by multiple others on the load phase as other tables are added.
    """
    # Prep the data extract to remove dupes
    print('<<< Checking for duplicates in the daily_headlines primary key >>>')
    daily_headlines_df = __cut_duplicate_primary_keys(dataframe, 'dated_article_key')
    
    # Connect to the database
    conn = pg2.connect(database='news_summary', 
                       user="postgres", 
                       host = 'localhost', 
                       password = config.passwords['postgresql'])
    # Retrieve the cursor
    cur = conn.cursor()
    # general query to append daily headlines data
    daily_headlines_insert = '''INSERT INTO daily_headlines 
                                (dated_article_key, article_key, datetime, newssource, article_type, headline, weblink)
                                VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    # iter through rows and append
    for row in range(0, len(daily_headlines_df),1):
        cur.execute(daily_headlines_insert, (daily_headlines_df['dated_article_key'][row],
                                             daily_headlines_df['article_key'][row],
                                             daily_headlines_df['datetime'][row],
                                             daily_headlines_df['newssource'][row],
                                             daily_headlines_df['article_type'][row],
                                             daily_headlines_df['headline'][row],
                                             daily_headlines_df['weblink'][row]))
    
    # Close connections
    conn.commit()
    cur.close()
    conn.close()
    
    
def extract_weekly_highlights():
    """
    (Extract routine) Extracts weekly highlights from the server.
    """

##################################################################################
# ETL routines finished
##################################################################################
