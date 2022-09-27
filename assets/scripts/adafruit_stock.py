#! /usr/bin/python3.9

#Script to web scrape info about RPi availability from Adafruit's Website

import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
import sys



log_adafruit=[]


#Page for RPi4
urlA_4='https://www.adafruit.com/product/4295'

r=requests.get(urlA_4)

soup=BeautifulSoup(r.text,'html.parser')
prodTable=soup.find('ol',{'class':'meta_pid_boxes'})
for line in prodTable: #cycle through and find em
    line=str(line)
    if line !='\n': #some are empty lines...
        newline=line.split('\n')
        _type=newline[3][:3]
        _stock=newline[5][:-8]

        if _stock!='Out of stock':
            log_adafruit.append(('Adafruit',str(_type),urlA_4))




#Pages for RPi 3B+, 3B, Pi Zero (Not W, Pi Zero, Pi Zero 2 -->4 digit number is the product ID
adafruit_single_products_list=[('3775','RPi 3B+'),('3055','RPi 3B'),('2885','RPi Zero (Not W)'),('3400','RPi Zero W'),('5291','RPi Zero 2')]

def single_prod_at_adafruit(_url,_type,log_adafruit):
    r=requests.get(_url)

    soup=BeautifulSoup(r.text,'html.parser')
    prod=soup.find('div',{'class':'oos-header'})
    for line in prod:
        _stock=str(line)


        if _stock!='Out of stock':
            log_adafruit.append(('Adafruit',_type,_url))

    return log_adafruit

#Cycle through them now
for url in adafruit_single_products_list:
    log_adafruit=single_prod_at_adafruit(str('https://www.adafruit.com/product/'+url[0]),url[1],log_adafruit)

#Keep below for testing reasons
#log_adafruit=[('Test Website','Test RPi 4','www.example.com'),('Test2 Website','Test RPi 3','www.example.com')]
        
if log_adafruit!=[]: #something is in stock
    ctx = ssl.create_default_context()
    password = "Still not giving you my password..."    # Your app password goes here
    sender = "my_source_email@gmail.com"    # Your e-mail address
    receiver = "recieving_email@gmail.com" # Recipient's address
    message =  """\
    From: "RPi in Stock" <my_source_email@gmail.com>
    To: "Wesley Kent" <recieving_email@gmail.com>
    Subject: One or more RPi Boards appear to be in stock\n

    """

    for log in log_adafruit:
        message+="RPi Board: "+log[1]+"\nSite: " +log[0]+"\n"+"Link: "+log[2]+"\n"+"\n"

    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)





