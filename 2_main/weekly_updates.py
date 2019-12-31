# -*- coding: utf-8 -*-
"""
Automatically run script to update server and summaries, based on weekly reviews

@author: mattm
"""

import postgres_helper as pg_help
import config
import smtplib

##################################################################################
# Run weekly server extract
##################################################################################

# Add code pulling from postgres_helper.py

##################################################################################
# Weekly server extract
##################################################################################


##################################################################################
# Email functionality
##################################################################################


def weekly_email_update():
    """
    Sends an email with the latest weekly server data pulled out, reminding me to jump onto the webpage.
    """
    # TODO - Properly write the ETL server routines so the following line can be uncommented
    # weekly_highlight_df = weekly_highlight()
    smtpObj = smtplib.SMTP('smtp.mail.yahoo.com', 587) # Connect to outlooks stmp provider, 'smtp-mail.outlook.com'
    smtpObj.ehlo() # Say "hello" to the server
    smtpObj.starttls() # Connect to port 587 (TLS encryption)
    smtpObj.login('mattmcfahnn@yahoo.com', config.email_yahoo) #Log in to access email
    #Send the mail
    smtpObj.sendmail('mattmcfahnn@yahoo.com','matthew.mcfahn@li.com',
                     '''SUbject: Weekly News Update\n
                     TODO: Fill out the body text of the weekly news email update, pulling in server data.\n\n
                     \n See the following webpage for the more regular news update: exaplewebpage@domain.com''')
    # TODO - Put data formatted into email

##################################################################################
# 
##################################################################################
