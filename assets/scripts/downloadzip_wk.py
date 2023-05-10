#! /usr/bin/python2.7
import sys, os
import requests

import hashlib
import datetime

import shutil
import zipfile


thezip="/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages.zip"
thefolder="/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages/"

if os.path.exists(thezip):
    os.remove(thezip)
if os.path.exists(thefolder):
    shutil.rmtree(thefolder)



url="https://github.com/fe-moldark/wesleykent-website/archive/refs/heads/gh-pages.zip"

try:
    filetowrite=open(thezip,"wb")
    filetowrite.write(requests.get(url).content)
    filetowrite.close()

    zip_name="wesleykent-website-gh-pages.zip"

    try:
        with zipfile.ZipFile(thezip) as z:#zip_name
            z.extractall("/media/pi/MyExternalDrive/save_wk_website/")#+"wesleykent-website-gh-pages")
            print "Unzipped file successfully."
    except:
        print "Invalid file type to unzip or just failed somehow. Get it fixed."
        sys.exit()



    current_time = datetime.datetime.now()
    folderPath="/media/pi/MyExternalDrive/save_wk_website/"

    dateToday=str(current_time.year)+"-"+str(current_time.month)+"-"+str(current_time.day)+"/"
    timeToday=str(current_time.hour)+"-"+str(current_time.minute)+"/"

    main="/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages/"
    full_list=[]

    
    total_count=0
    for path, subdirs, files in os.walk(main):
        for name in files:
            total_count+=1
            location=os.path.join(path, name)
            full_list.append(location)

    print "Total count of files: ", total_count #delete this later, just for checking rn


    badhashes=[]
    for item in full_list:

        #compare hash from location below
        tohash1=str(item)

        #good copy here
        tohash2=str(item).replace("wesleykent-website-gh-pages","good_copy_wk_site")


        #hash stuff now
        hasher=hashlib.md5()
        with open(tohash1, 'rb') as test_new:
            buf=test_new.read()
            hasher.update(buf)
            NEW_HASH=hasher.hexdigest()
            #print "From the web: ", NEW_HASH

        try: #might not exist
            hasher=hashlib.md5()
            with open(tohash2, 'rb') as test_good:
                buf=test_good.read()
                hasher.update(buf)
                GOOD_HASH=hasher.hexdigest()
        except IOError:
            GOOD_HASH="anewfilehasbeenloaded"

        #print NEW_HASH==GOOD_HASH, tohash1
        #print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

        if NEW_HASH!=GOOD_HASH:
            badhashes.append([str(tohash1).replace("/media/pi/MyExternalDrive/save_wk_website/wesleykent-website-gh-pages",""),NEW_HASH,GOOD_HASH])
        

    message=""


    print "END========================\n"
    print "Number of bad hashes: ", len(badhashes)
    for item in badhashes:
        print "Item "+str(badhashes.index(item))+": "+str(item[0])

        

    message+="\nTotal number of changes: "+str(len(badhashes))+"\n"
    for item in badhashes:

        if item[2]!="anewfilehasbeenloaded":
            message+="\n"+"New file at: "+str(item[0])
            message+="\n"+"Last known good hash: "+str(item[2])
            message+="\n"+"Current hash: "+str(item[1])
        else:
            message+="\n"+"A suspected new file has been added at: "+str(item[0])+"\n"
            
        
    now_save=open("/media/pi/MyExternalDrive/save_wk_website/mail_body.txt","w")
    now_save.write(message)
    now_save.close()

    #this is a poor way to do things, just fix it later once merged with the mail script
    if len(badhashes)==0:
        query=['False']
    else:
        query=['True']
        

    yesno=open("/media/pi/MyExternalDrive/save_wk_website/send_message_query.txt","w")
    yesno.writelines(query)
    yesno.close()



    #delete old folder saves now
    current_time = datetime.datetime.now()
    dateToday=str(current_time.year)+"-"+str(current_time.month)+"-"+str(current_time.day)+"/"


    base="/media/pi/MyExternalDrive/save_wk_website/"
    theList=os.listdir(base)


    print "Got this far."
    permanentlist=["good_copy_wk_site","wesleykent-website-gh-pages",str(dateToday)[:-1]]
    #print permanentlist

    for files in theList:
        if os.path.isdir(os.path.join(base, files)):
            if str(files) not in permanentlist:
                print("try1")
                shutil.rmtree(os.path.join(base, files))
                print("try2") #used for error testing now, remove "trys" later



except: #internet outage caused this one time
    yesno=open("/media/pi/MyExternalDrive/save_wk_website/send_message_query.txt","w")
    yesno.writelines(['Internet likely out.'])
    yesno.close()





    


