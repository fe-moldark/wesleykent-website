#! /usr/bin/python2.7
import sys, os

import requests
import wget

import hashlib
import datetime

import shutil
import zipfile


#default locations
thezip="/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages.zip"
thefolder="/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages/"

#if the zip file / unzipped folder exists - remove it
if os.path.exists(thezip):
    os.remove(thezip)
if os.path.exists(thefolder):
    shutil.rmtree(thefolder)


#get file and save locally
url="https://github.com/fe-moldark/wesleykent-website/archive/refs/heads/gh-pages.zip"
filetowrite=open(thezip,"wb")
filetowrite.write(requests.get(url).content)
filetowrite.close()


#try to unzip
try:
    with zipfile.ZipFile(thezip) as z:
        z.extractall("/media/pi/MyExternalDrive/save_wk_website/")
        print "Succesfully unzipped the file."
except:
    print "Invalid file type to unzip / failed to unzip."
    sys.exit()


#will need these variables for folder paths later on
current_time = datetime.datetime.now()
folderPath="/media/pi/MyExternalDrive/save_wk_website/"
dateToday=str(current_time.year)+"-"+str(current_time.month)+"-"+str(current_time.day)+"/"
timeToday=str(current_time.hour)+"-"+str(current_time.minute)+"/"


#for this script, gets all image locations from the site and saves it to 'full_list'
main="/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages/assets/"
full_list=[]
for path, subdirs, files in os.walk(main):
    for name in files:
        location=os.path.join(path, name)
        if str(location)[-4:] in [".png",".jpg"]:
            full_list.append(location)


#'bashhashes' list will record incorrect / different hashes from known good copy
badhashes=[]

for item in full_list:

    #compare hash from saved location below
    tohash1=str(item)

    #good copy for hash here
    tohash2=str(item).replace("wesleykent-website-gh-pages","good_copy_wk_site")


    #hash stuff now
    hasher=hashlib.md5()
    with open(tohash1, 'rb') as test_new:
        buf=test_new.read()
        hasher.update(buf)
        NEW_HASH=hasher.hexdigest()

    #needs 'try' since file might not exist
    try:
        hasher=hashlib.md5()
        with open(tohash2, 'rb') as test_good:
            buf=test_good.read()
            hasher.update(buf)
            GOOD_HASH=hasher.hexdigest()
    except IOError:
        GOOD_HASH="anewfilehasbeenloaded"

    print NEW_HASH==GOOD_HASH, tohash1
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

    if NEW_HASH!=GOOD_HASH:
        badhashes.append([str(tohash1).replace("/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages",""),NEW_HASH,GOOD_HASH])
    
#begin mail_body
message=""


print "END of hashing ===============================\n"
print "Number of bad hashes: ", len(badhashes)
for item in badhashes:
    print "Item "+str(badhashes.index(item))+": "+str(item[0])

    
#document notes to message variable
message+="\n"+"Total number of changes: "+str(len(badhashes))+"\n"
for item in badhashes:

    if item[2]!="anewfilehasbeenloaded":
        message+="\n"+"Changed image at: "+str(item[0])
        message+="\n"+"Last known good hash: "+str(item[2])
        message+="\n"+"Current hash: "+str(item[1])
    else:
        message+="\n"+"A suspected new image has been added at: "+str(item[0])+"\n"
        

#now write completed message to mail_body.txt file
now_save=open("/media/pi/MyExternalDrive/save_wk_website/mail_body.txt","w")
now_save.write(message)
now_save.close()


#there was a better way to do this next part, and save status to send / not send email
if len(badhashes)==0:
    query=['False']
else:
    query=['True']
yesno=open("/media/pi/MyExternalDrive/save_wk_website/send_message_query.txt","w")
yesno.writelines(query)
yesno.close()



#delete old folder saves now
dateToday=str(current_time.year)+"-"+str(current_time.month)+"-"+str(current_time.day)+"/"


#base path
base="/media/pi/MyExternalDrive/save_wk_website/"
theList=os.listdir(base)


#permanentlist are folders NOT to delete
permanentlist=["good_copy_wk_site","wesleykent-website-gh-pages",str(dateToday)[:-1]]
print permanentlist

for files in theList:
    if os.path.isdir(os.path.join(base, files)):
        if str(files) not in permanentlist:
            shutil.rmtree(os.path.join(base, files))









    


