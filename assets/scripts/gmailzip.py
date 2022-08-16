#! /usr/bin/python3.9
import smtplib
import ssl


#set variables that will be needed to send an email
ctx = ssl.create_default_context()
password = "sorry, not stupid enough to give you my password" #Your app password goes here
sender = "my_source_email@gmail.com"    # Your e-mail address
receiver = "recieving_email@gmail.com" # Recipient's address
message =  """\
From: "Alert" <my_source_email@gmail.com>
To: "Wesley Kent" <recieving_email@gmail.com>
Subject: Alert - images changed on wesleykent domain


Changes detected for wesleykent.com:

"""


#open what was saved in the previous script - a log of all "bad" hashes and their locations
now_save=open("/media/pi/MyExternalDrive/save_wk_website/mail_body.txt","r")
all_lines=now_save.readlines()
now_save.close()



#again, better way to have saved this setting but it works
yesno=open("/media/pi/MyExternalDrive/save_wk_website/send_message_query.txt","r")
result=yesno.readlines()[0]
yesno.close()


#If false, no email needed since no new alerts
if result=="False":
    pass
else:
    all_lines.pop(0)

    #this is the mail_body.txt file here
    for line in all_lines:
        message+=str(line)+"\n"


    #this sends the actual email
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
