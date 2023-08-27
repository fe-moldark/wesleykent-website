gmail_pass = "your_password"
user = "your_email@gmail.com"
host = "smtp.gmail.com"
port = 465



import smtplib, ssl, os
from subprocess import run
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import time
 

def send_email_w_attachment(to, subject, body, filename):
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

reboot=False

#time.sleep(90) #this script runs at boot, so give it some time to load everything up first
#sleep function now done with /bin/sleep 90 from the crontab with the "@reboot"



try:

    from datetime import datetime

    date=datetime.now()
    today=date.strftime('%Y/%m/%d')
    file_location="/home/pi/wesleykent-website-gh-pages/assets/icon.png"

    #all the below print() statements are just for debugging - ignore
    if True: #res.status_code == 200:
        if len(os.listdir('/media/pi/MyExternalDrive/'))!=0:
            log="Nothing to worry about - load successful on: "+today
            print("1")
        else:
            log="Failed to load external hard drive: "+today
            print("2")

            try:
                os.system('sudo mount /dev/sda1 /media/pi/MyExternalDrive/') #if not at sda1 won't work but won't stop the script either
                time.sleep(5)
                print("3")
                if len(os.listdir('/media/pi/MyExternalDrive/'))!=0:
                    log+='\n-->Successfully reloaded external drive (type #1)'
                    print("4")
                else:
                    log+='\n-->Fail type #1 to remount external drive. Reboot in progress.'
                    reboot=True
                    print("5")
            except:
                log+='\n-->Fail type #2 to remount external drive.'
                #this might require more debugging later on



        email_list=["recieving_email@gmail.com"]

        for email in email_list:
            to = email
            subject = 'Weekly check of file server'
            body = log
            filename = "icon.png"

            send_email_w_attachment(to, subject, body, filename)

        print("6")
        if reboot is True:
            print("7")
            time.sleep(10)
            os.system('sudo shutdown -r now')

except IndexError:

    print("honestly I forget what was causing this but I'm also not getting the error anymore, so...")
    pass
