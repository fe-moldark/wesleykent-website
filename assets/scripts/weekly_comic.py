#! /usr/bin/python2.7

gmail_pass = "password"
user = "source_email@gmail.com"
host = "smtp.gmail.com"
port = 465



import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
 

def send_email_w_attachment(to, subject, body, filename):
    # create message object
    message = MIMEMultipart()

    message['From'] = Header(user)
    message['To'] = Header(to)
    message['Subject'] = Header(subject)    
    message.attach(MIMEText(body, 'plain', 'utf-8'))

    _f = open(file_location, 'rb')
    att = MIMEApplication(_f.read(), _subtype="txt")
    _f.close()
    att.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(att)
 
    # setup email server
    server = smtplib.SMTP_SSL(host, port)
    server.login(user, gmail_pass)
 
    server.sendmail(user, to, message.as_string())
    server.quit()


#main
try:

    from datetime import datetime

    date=datetime.now()
    today=date.strftime('%Y/%m/%d')
    #today='2023/04/30' #good test
    url="https://foxtrot.com/"+today+"/"

    print("Url: "+url)

    import requests 
    from bs4 import BeautifulSoup
    import shutil
    import sys
        
    def getdata(url):
        with requests.Session() as session1: #requires user agent
            session1.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en"
            }

        r=session1.get(url)
        return r.text

    htmldata = getdata(url) 
    soup = BeautifulSoup(htmldata, 'html.parser') 

    mydivs = soup.find_all("div", {"class": "entry-container"})

    print(mydivs)
    bahh=str(mydivs[0])

    def seize(original,preface,index_mod):
        
        index=original.find(preface)+index_mod
        mod_url=""
        while original[index]!="\"":
            mod_url+=original[index]
            index+=1
        return mod_url

    new_url=seize(bahh,'<a href=',9)

    print("New url: "+new_url)

    #round two
    htmldata = getdata(new_url) 
    soup = BeautifulSoup(htmldata, 'html.parser')
    print("\n\n=================================================\n\n")
    find_figure=str(soup.find_all('figure', {"class":"wp-block-image size-full"})[0])


    get_img=seize(find_figure,'src="',5)
    print("Get_img url: ",get_img)


    #now to download the image
    res = requests.get(get_img, stream=True)
    file_location="/media/pi/MyExternalDrive/save_wk_website/foxtrot.png"

    if res.status_code == 200:
        with open(file_location,'wb') as save:
            shutil.copyfileobj(res.raw, save)


        email_list=["recieving_email1@gmail.com","recieving_email2@outlook.com"]

        for email in email_list:
            to = email
            subject = "Weekly FoxTrot Comic"
            body = "Original source: "+str(new_url)+"\n\n"+"Date: "+str(today)
            filename = "foxtrot.png"

            send_email_w_attachment(to, subject, body, filename)

except IndexError:
    pass #maybe add some error logging here later on
