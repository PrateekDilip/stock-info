import urllib2
import smtplib
import time
import os,sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

to_list = []
data_dict = {}
fromaddr = "stock-updates@abc.com"
toaddr = "abc@xyz.com"
err_list = ["Err String"]
log_list = ["Log String"]
subject = "stock-update run info"

def start_server():
    """Initializes a SMTP server to be used later.
    Arguements: None
    Returns: Server object"""
    server = ""
    logging.info("start_server")
    try:
        logging.debug("Initializing SMTP Server Client")
        server = smtplib.SMTP(host = "<put your hostIP>")

    except Exception as E:
        print "Exception"
        print E
        logging.info("Server Initialization failed")
        logging.debug(E)
        err_list.append("start_server:" + str(E))
    log_list.append("start_server:" + str(server))
    return server

mail_server = start_server()

def send_mail(server,toaddr,subject,msg_text,mode):
    """Sends mail using the server based on the passed arguements.
    send_mail(server,toaddr,subject,msg_text)

        server: SMTP server
        toaddr: list of aliases or email-ids
        subject: string
        msg_text: plain-text"""
    logging.info("send_mail()")
    msg = MIMEMultipart()
    global fromaddr
    logging.debug("Parameters:"+ fromaddr + "," +str( toaddr )+"," + subject)
    msg['From'] = fromaddr
    msg['To'] = ",".join(toaddr)
    msg['Subject'] = subject
    msg.attach(MIMEText(msg_text,mode))
    try:
        logging.info("sending mail")
        print "Send Email"
        server.sendmail(fromaddr,msg['to'].split(","),msg.as_string())
    except Exception as E:
        print "Exception occured"
        print E
    print "Mail Sent"

    log_list.append("send_mail:" + str(msg['From'])+" "+ str(msg['To']) + " " + str(msg['Subject']))


def build_url(symbol):
	url1 = "https://www.nasdaq.com/symbol/"
	url2 = "/real-time"
        return (url1 + symbol.rstrip('\n') + url2)

f = open('company','r')
for line in f:
	url_post = build_url(line)
	r = requests.post(url_post)
	url_soup = BeautifulSoup(r.text, 'html.parser')
	cur_price = url_soup.find_all(['div'], attrs = {'class':'qwidget-dollar', 'id':'qwidget_lastsale'})[0].text.encode('utf-8')
        company = line
        print(company.rstrip('\n')+" " + cur_price)
        data_dict[company.rstrip('\n')] = cur_price
print data_dict
df = pd.DataFrame(data_dict.items(), columns = ['Company','Current price'])
table_data=df.to_html('result.html')
f1 = open('result.html','r')
table = ""
for item in f1:
        print item
	table += item
table = "<h2>Stock prices</h2>" + table
to_list.append("abc@xyz.com")
send_mail(mail_server, to_list, str('Stock update info'), table, 'html')
