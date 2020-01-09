# News Summary

This repo is a current work in progress, developed as a personal project to use the power of web scraping via python to track trends in the news for multiple purposes:

 - Automatic customised highlights of news from the week;
 - Recording a log of top news stories over time, day by day;
 - Using the database of stories for analysis.
 
At present, the back end of the package has been developed, extracting news from a selection of top UK newspapers, and the load routines into a local PostgreSQL database have been built out.
 
## Table of contents
 
 * [Dependencies](#dependencies)
 * [Useage](#useage)
 * [Issues](#issues)
 
## Dependencies
 
**Note:** This repo hasn't been designed to work as a distributed package, although the logic may be of use for any web scraping and storage task. 
 
  * **Python**
    * contextlib
    * bs4 (BeautifulSoup)
    * pandas
    * selenium
    * psycopg2
  * **SQL**
    * PostgreSQL

## Useage
 
### How to scrape news data and save it in a SQL database
 
**Creating a local SQL server**
If you have PostgreSQL set up locally, initialise a new database called "news_summary", and run the init_tables.sql file to initalise tables within the database for storing scraped data.

*Note:* The postgres_helper.py script could be customised using a different library other than psycopg2 to interact with a different SQL platform.

**Interacting with your local SQL database via python**

A local config.py file must be set up within a **directory that is not under version control** within the  PythonPath, to be referenced as a password manager for your SQL database. Within it should be the following piece of code:
 ``` python
root = 'C:/Users/.../' # INSERT YOUR ROOT PATH 

passwords = {'postgresql':'MY SECRET PASSWORD', #Reference your password to access the local sql database you've set up
             # Any other passwords you may wish to add
             }
 ```

This allows the postgres_helper script to retrieve your PostgreSQL password and make a connection to the news_summary database.

**Basic functionality**

Once the correct SQL server has been initalised, and your local python environment can access this server, daily_server_update.py, when run, will update this server with the current data of the selected webpages.

**Automating the webscraping**

To scrape information from the sites regularly, you have a number of options that you may follow. I have opted for windows Task Scheduler, running a .bat file to execute the daily_server_update.py file at specified times. I found the following tutorial helpful in this: "[Automate your Python Scripts with Task Scheduler](https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279)"

## Issues

There are a number of issues still to be resolved.

* Changing HTTP structures of webpages being scraped (and the dreaded injection of JavaScript)
* Potential security issues for storing passwords locally - is there a better option?
* Lack of depth to data being retreived
* And many more to be added...
