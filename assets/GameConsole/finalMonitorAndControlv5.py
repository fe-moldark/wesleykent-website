# This script monitors input from 4 or 5 different buttons connected over gpio pins (NOT the usb joystick). Button 1 starts a pygame window with the game I am writing,
# the second starts a media interface / player thing (also pygame), the third sets the wireless interface up or down, and the fourth conducts a clean shutdown of the system
# Hardware pertinent to this script includes a RPi Model 4 board and four buttons
#
# Author: Wesley Kent
# Created: 06/17/2023
#
# https://github.com/fe-moldark/wesleykent-website/tree/gh-pages/assets/GameConsole
#
# Instructions: Press buttons


from time import sleep
from time import time
import os
#import wiringpi as wpi
from subprocess import Popen
from subprocess import check_output as EXECUTE #why not? no one can stop me
import requests
import RPi.GPIO as GPIO
import hashlib



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)



defineLEDs = [26, 16, 21, 12]

for LED in defineLEDs:
    GPIO.setup(LED,GPIO.OUT)
    GPIO.output(LED,GPIO.LOW)


def LEDsequence():
    increment = .1
    print("Test LED sequence...")
    for LED in defineLEDs:
        GPIO.output(LED,GPIO.HIGH)
        sleep(increment)
    for LED in defineLEDs:
        GPIO.output(LED,GPIO.LOW)
        sleep(increment)
    for LED in defineLEDs[::-1]:
        GPIO.output(LED,GPIO.HIGH)
        sleep(increment)
    for LED in defineLEDs[::-1]:
        GPIO.output(LED,GPIO.LOW)
        sleep(increment)
    print("...and end.")


LEDsequence()

start_time = time()


def areHashesDifferent(defaultPath,newPath):
    hasher=hashlib.md5()
    with open(defaultPath,'rb') as testOld:
        buf=testOld.read()
        hasher.update(buf)
        OLDHASH=hasher.hexdigest()

    hasher=hashlib.md5()
    with open(newPath,'rb') as testNew:
        buf=testNew.read()
        hasher.update(buf)
        NEWHASH=hasher.hexdigest()

    if OLDHASH!=NEWHASH:
        return True
    else:
        return False


def ledOnOff(num):
    for i in range(3):
        sleep(0.1)
        GPIO.output(num,GPIO.HIGH)
        sleep(0.1)
        GPIO.output(num,GPIO.LOW)


def getLatestScript():

    #get listing of sharedFolder and get the most recent file from there
    listDir='/home/pi/sharedWithPi/'
    allFiles=os.listdir(listDir)
    allFiles=[item for item in allFiles if os.path.isfile(os.path.join(listDir, item))]
    allFiles.sort(key=lambda x: os.path.getmtime(os.path.join(listDir,x)))

    #cached file
    cachedFileAt='/home/pi/showcasev3.py'
    lastModified=os.path.getmtime(cachedFileAt)

    print('lastModified: ',lastModified)

    if len(allFiles)==0: #mpty directory
        messageBegin='NAS not mounted or folder is empty. Using cached script last edited: '+str(time.strftime('%m/%d/%Y',time.gmtime(lastModified)))
    else: #at very least there are some files in there
        #get latest file and hash it
        latestFilename=os.path.join(listDir,allFiles[-1])
        latestModified=os.path.getmtime(latestFilename)

        if latestModified > lastModified:
            messageBegin='There is a more recent script called '+str(allFiles[-1])

            #okay, so more recent one, but are they different?
            if areHashesDifferent(cachedFileAt,latestFilename)==True:
                #different, more recent file so copy contents over
                os.system('cp '+str(latestFilename)+' '+str(cachedFileAt))
                messageBegin='Program has been updated with a more recent file from mounted NAS called '+str(allFiles[-1])
            else:
                messageBegin='File is up to date, using cached version last edited: '+str(time.strftime('%m/%d/%Y',time.gmtime(lastModified)))

            
        else: #current version is more recent
            messageBegin='Local file is more up to date than anything in the shared drive.'

        writeMessageTo=open('/home/pi/message.txt','w')
        getSplit=len(messageBegin)//2
        while messageBegin[getSplit]!=' ':
            getSplit-=1
        writeMessageTo.writelines([messageBegin[:getSplit]+'\n',messageBegin[1+getSplit:]]) #str(messageBegin)
        writeMessageTo.close()

    print('messageBegin: ',messageBegin)
    return messageBegin


def startMyProgramCheck(pygameProgram,justStop):
    isRunning = os.popen('ps aux | grep '+str(pygameProgram)).read()
    print(len(isRunning),isRunning)
    mod = str(isRunning)
    modList = mod.split("\n")
    finalPID=[]

    for item in modList:
        
        try:

            #okay I changed this method so it is now searching for that python keyword
            #the rest of the string WILL be found as a result of the 'ps aux' command
            #this method is working, and better than filtering by the user running the process as done before

            if 'python' in str(item):
                getPID=str(item)
                addToList=''
                while getPID[0] not in [str(i) for i in range(10)]:#ie a num
                    getPID=getPID[1:]
                while getPID[0] in [str(i) for i in range(10)]:#is is a num
                    addToList+=str(getPID[0])
                    getPID=getPID[1:] 
                finalPID.append(addToList)
                                        
        except IndexError:
            pass #print('failure!',getPID)

    if finalPID!=[]: #means program is ALREADY running
        print('killing program(s) now!')
        ledOnOff(12)
        for toKill in finalPID:
            os.system('sudo kill '+str(toKill))
    else:
        if justStop is False:
            ledOnOff(21)
            print('not yet started, so program will start')
            #Popen(['/usr/bin/env', 'python','/home/pi/'+str(pygameProgram)])
            Popen(['sudo','python','/home/pi/'+str(pygameProgram)])
    
pause=float(1)


while True:

    #my program check
    if GPIO.input(19)==False:
        if float(time()-start_time) > float(pause):
            returnMessage=getLatestScript() #will update file first
            startMyProgramCheck('mediaCenterv3.py',True)
            startMyProgramCheck('showcasev3.py',False)
            start_time = time()

    #media center
    if GPIO.input(24)==False:
        if float(time()-start_time) > float(pause):
            startMyProgramCheck('showcasev3.py',True)
            startMyProgramCheck('mediaCenterv3.py',False)
            start_time = time()

    #WiFi on/off
    if GPIO.input(25)==False:
        if float(time()-start_time) > float(pause):
            checkWiFi=str(EXECUTE(['ifconfig','wlan0']))
            if "inet" in checkWiFi: #kill the wifi
                os.system('sudo ifconfig wlan0 down')
                ledOnOff(12)
            else:
                os.system('sudo ifconfig wlan0 up')
                #check if connected to LAN
                connectedState=False

                for i in range(int(15*5/2)): #.2 inverse==5/1, so 15 sec (but on/off so durch 2)
                    sleep(0.2)
                    GPIO.output(26,GPIO.HIGH)
                    GPIO.output(16,GPIO.LOW)

                    sleep(0.2)
                    GPIO.output(26,GPIO.LOW)
                    GPIO.output(16,GPIO.HIGH)

                    #try local NAS for LAN connection only, not looking to get outside the network necessarily
                    getResponse = os.system('ping -c 1 192.168.11.19')

                    if getResponse==0: #successful connection
                        connectedState=True
                        print('GOOOTTTTT EEEEMMMMM')
                        break
                    else:
                        pass #for now, we're still in the loop afterall
                        
                GPIO.output(16,GPIO.LOW)

                print('connectedState: ',connectedState)
                if connectedState==True:
                    ledOnOff(21)
                else:
                    ledOnOff(12)
                
            start_time = time()
    
    #shutdown      
    if GPIO.input(22)==False:
        if float(time()-start_time) > float(pause):
            ledOnOff(12)
            os.system("sudo shutdown -h now")
            start_time = time()

    sleep(.1)