# -*- coding: utf-8 -*-
"""
Daily server update script (to run through task manager)

@author: mattm
"""

import news_summary
import postgres_helper as pg_help


if __name__ == '__main__':
    ## Extract news data from web
    news_df = news_summary.retreive_daily_news_summary()
    
    ## Update server with daily info
    pg_help.update_server(news_df)
