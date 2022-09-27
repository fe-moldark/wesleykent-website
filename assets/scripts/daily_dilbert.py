#! /usr/bin/python2.7

#Script to send the Dilbert comic of the day to my email
#Coupled with the crontab, sends emails on work days at 9am

#Email modules
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

#Other modules
from datetime import datetime
import requests 
from bs4 import BeautifulSoup
import shutil
 
 
gmail_pass = "Not giving you my password"
user = "my_source_email@gmail.com"
host = "smtp.gmail.com"
port = 465


def send_email_w_attachment(to, subject, body, filename):

    #Message Object
    message = MIMEMultipart()
 
    #Headers
    message['From'] = Header(user)
    message['To'] = Header(to)
    message['Subject'] = Header(subject)
 
    #Include message body (really optional for this part)
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    #Attach file
    _f = open(file_location, 'rb')
    att = MIMEApplication(_f.read(), _subtype="txt")
    _f.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(att)
 
    #Mail server
    server = smtplib.SMTP_SSL(host, port)
    server.login(user, gmail_pass)
 
    #Send mail
    server.sendmail(user, to, message.as_string())
    server.quit()
    

#Get date
date=datetime.now()
today=date.strftime('%Y-%m-%d')

#Today's comic strip
url="https://dilbert.com/strip/"+str(today)

def getdata(url): 
    r = requests.get(url) 
    return r.text


#Use BeautifulSoup module to pull data from the page
htmldata = getdata(url) 
soup = BeautifulSoup(htmldata, 'html.parser') 
for item in soup.find_all('img'):
    #Location for all the images I need to search through always begin with this
    if item['src'][:31]=='https://assets.amuniversal.com/':
        got_this_url=str(item['src'])
        #FYI there are more than one that meet this criteria but the first one is always it
        #Hence the 'break' once it finds one
        break




#Now to download the image
req = requests.get(got_this_url, stream = True)

#where I happen to store this file locally
file_location="/media/pi/MyExternalDrive/save_wk_website/dilbert_0.gif"

#Double check the link is valid
if req.status_code == 200:
    with open(file_location,'wb') as save:
        shutil.copyfileobj(req.raw, save)

    #Recipients of the email
    email_list=["recieving_email@gmail.com","recieving_email2@outlook.com"]

    for email in email_list:

        to = email
        subject = "Daily Dilbert Comic"
        body = "Read this comic, then laugh."
        filename = "dilbert_0.gif"

        #Call the function we first defined in the beginning
        send_email_w_attachment(to, subject, body, filename)






