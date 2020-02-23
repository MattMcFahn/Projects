# -*- coding: utf-8 -*-
"""
SQL helper to read and write to SQL 

Created on Thu Dec 26 15:56:16 2019

@author: mattm
"""

import psycopg2 as pg2
import pandas.io.sql as sqlio
import config

##################################################################################
# Helper functions
##################################################################################

def __cut_duplicates(dataframe, table_name):
    """
    Pd.DataFrame -> pd.DataFrame
    
    Tests the data retrieved against the existing sql table, and drops duplicate keys
    """
    print('<<<Removing duplicates from data retrieved ...>>>')
    # Connect to the database
    conn = pg2.connect(database='news_summary', 
                       user="postgres", 
                       host = 'localhost', 
                       password = config.passwords['postgresql'])
    # Pull table data for checking
    select_call = '''SELECT * FROM {}'''.format(table_name)
    existing_df = sqlio.read_sql_query(select_call, conn)
    
    # Combine to look for dupes
    full_df = existing_df.append(dataframe)
    full_df['duplicated'] = full_df.duplicated(['headline','newssource','weblink'], keep=False)
    
    # Cut back to retrieved data, split into dupes & dedupes
    n = len(full_df)
    original_df = full_df[n-len(dataframe):n]
    
    
    unique_df = original_df.loc[original_df['duplicated'] == False]
    unique_df.drop(columns=['duplicated'], inplace=True)
    
    duplicates_df = original_df.loc[original_df['duplicated'] == True]
    duplicates_df.drop(columns=['duplicated'], inplace=True)    
    
    new_stories_num = len(dataframe) - len(unique_df)
    print('Of {} stories retrieved in this call, {} were unique'.format(len(dataframe),
                                                                        new_stories_num))
    print('<<<Removing duplicates from data retrieved ... COMPLETE>>>')
    return (unique_df, duplicates_df)
  
def __insert_data_sql(insert, dataframe, cur, table):
    """
    Simple helper to add data to existing sql tables
    """
    # iter through rows and append 
    for row in range(0, len(dataframe),1):
        if table == 'daily_headlines':
            cur.execute(insert, (dataframe['dated_article_key'][row],
                                 dataframe['article_key'][row],
                                 dataframe['datetime'][row],
                                 dataframe['newssource'][row],
                                 dataframe['article_type'][row],
                                 dataframe['headline'][row],
                                 dataframe['weblink'][row]))    
        elif table == 'headlines_unique':
            cur.execute(insert, (dataframe['article_key'][row],
                                 dataframe['datetime'][row],
                                 dataframe['newssource'][row],
                                 dataframe['article_type'][row],
                                 dataframe['headline'][row],
                                 dataframe['weblink'][row]))    


##################################################################################
# Helper functions
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
    unique_df, dupes_df = __cut_duplicates(dataframe, 'daily_headlines')
    
    # Connect to the database
    conn = pg2.connect(database='news_summary', 
                       user="postgres", 
                       host = 'localhost', 
                       password = config.passwords['postgresql'])
    # Retrieve the cursor
    cur = conn.cursor()
    
    # Inserting unique records
    insert_temp = '''INSERT INTO {} 
                    (dated_article_key, article_key, datetime, newssource, article_type, headline, weblink)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    
    ## Table: daily_headlines
    insert_daily = insert_temp.format('daily_headlines')
    __insert_data_sql(insert_daily, unique_df, cur, 'daily_headlines')    
    # Table: headlines_unique
    insert_unique = insert_temp.format('headlines_unique')    
    __insert_data_sql(insert_unique, unique_df, cur, 'headlines_unique')

    # Add counts for dupes
    # TODO    
    
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
