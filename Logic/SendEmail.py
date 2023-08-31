# **********************************************************************************************************************
# **********************************************************************************************************************
# Author:           Erika Brooks
# Lab:              Sprint 1 - CIS234A - PCC Spring 2023
# Date:             04.24.2023
# Description:      Logic Surrounding Sending Notifications
# Sources:          STORY - Send Notification
#
# Change Log:       - xx.xx.2023:
#
# **********************************************************************************************************************
# **********************************************************************************************************************

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Data.Database import Database
from Logic.Notification import Notification


# as called from send_email
# will send the email with the defined information.
# if this function somehow fires outside of being called by send_email
#    backup "stock text" exists so that the program will not fail
def sendnote_sendemail(recipients, subject_line, body):
    from_addr = 'OnyxOrderofProgrammers@gmail.com'
    to_addr = ['']
    recipients = recipients
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ", ".join(to_addr)
    msg['Subject'] = subject_line

    body = body

    msg.attach(MIMEText(body, 'plain'))

    # Specify Gmail Mail server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    # Send mandatory 'hello' message to SMTP server
    smtp_server.ehlo()
    # Start TLS Encryption as we're not using SSL.
    smtp_server.starttls()

    # Login to gmail: Account | Password
    smtp_server.login('OnyxOrderofProgrammers@gmail.com', 'cutulgaxrnqdxwcs')

    text = msg.as_string()

    # Compile email: From, To, Email body
    # smtp_server.sendmail(from_addr, [to_addr] + recipients, text)

    # Compile email: From, BCC ONLY , Email body
    smtp_server.sendmail(from_addr, recipients, text)

    smtp_server.quit()
    print('Email has sent successfully....\nattempting to write to DB....')


# retrieve the email addresses we will send to
# count the number of emails we will send to
# return a list and an int
def get_recipient_list():
    active_email_list = Database.get_all_emails()
    email_count = len(active_email_list)
    return active_email_list, email_count

# as called from SendNotificationUI.py
# gathers the recipient list and count of recipients
# calls sendnote_sendemail to send the email
# returns the count of recipients
def send_email(subject_line, body):
    my_recipients, recipient_count = get_recipient_list()
    sendnote_sendemail(my_recipients, subject_line, body)
    return recipient_count


# hard coded data required for the program to not error out in the event of a logic failure
# in the event that sendnote_sendemail fires without being called by send_email
# gather a list and count of recipient email addresses (will eventually need to be SQL data)
recip_list, count_of_list = ['OnyxOrderofProgrammers+test01@gmail.com', 'OnyxOrderof.Programmers@gmail.com',
                             'OnyxOrderofProgrammers+test02@gmail.com', 'Onyx.Orderof.Programmers@gmail.com'], 4

recipients = recip_list

subject_line = '******Test Automation Email Failure******'

body = """
        This is a stock email that is designed to be sent in the event of a logic failure.

    """

# **********************************************************************************************************************
# **********************************************************************************************************************
