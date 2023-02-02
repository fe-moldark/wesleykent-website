#!/usr/bin/python3.9
import time
from time import sleep
import sys, os
import subprocess
import psutil


#GPIO stuff
import board
import RPi.GPIO as GPIO


#Camera stuff
from picamera import PiCamera
import picamera

import datetime






def getStorage(): #this function simply returns the amouint of free space in gigabytes
    
    path = '/'
    bytes_avail = psutil.disk_usage(path).free
    gigabytes_avail = bytes_avail / 1024 / 1024 / 1024 #convert to Gb
    return gigabytes_avail


def areWeGoodOnStorage():
    
    gigabytes_avail=getStorage()

    if gigabytes_avail<=2: #2Gb is the current absolute bare minimum in place
        return False
    else:
        return True




camera=picamera.PiCamera()
camera.resolution=(640,480) #decent enough resolution
camera.framerate=24

#test start###########
#camera.start_preview()
#time.sleep(5)
#camera.stop_preview()
#sys.exit()
#end test#############


def startNewRecording():
    count_file=open("/home/pi/Desktop/count.txt","r") #this file easily tracks the number for the recording
    getVideoFileNumber = int(count_file.readlines()[0])
    count_file.close()
    
    count_file2=open("/home/pi/Desktop/count.txt","w") #adjust +=1
    count_file2.write(str(getVideoFileNumber+1))
    count_file2.close()

    newName="dashcam"+str(getVideoFileNumber+1) #new recording name

    camera.start_recording('/home/pi/Desktop/save/'+newName+'.h264')




#initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


#LED number assignment
blueLED=23
orangeLED=8


#when the script first starts the LEDs will be turned on here
GPIO.setup(blueLED,GPIO.OUT)
GPIO.output(blueLED,GPIO.HIGH)
GPIO.setup(orangeLED,GPIO.OUT)
GPIO.output(orangeLED,GPIO.HIGH)
time.sleep(1)

#and now back to off
GPIO.output(blueLED,GPIO.LOW)
GPIO.output(orangeLED,GPIO.LOW)
#sys.exit()



#these are our two main switches
dashSwitch=18
statusSwitch=7

GPIO.setup(dashSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(statusSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)




#delete function for old recordings
def delete_recordings():

    #remove all files in the folder where recordings are saved
    checkDir = "/home/pi/Desktop/save/"
    for f in os.listdir(checkDir):
        os.remove(os.path.join(checkDir, f))

    #reset the counter for naming files
    with open('/home/pi/Desktop/count.txt', 'w') as resetCount:
        resetCount.write('0')
        resetCount.close()

    #at the end signal we are done with two quick flashes
    GPIO.output(orangeLED,GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(orangeLED,GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(orangeLED,GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(orangeLED,GPIO.HIGH)
    
    #this will only revert back to 'LOW' again once the switch has been flipped back off

    
    
    
#buttons
buttonDelete=16
GPIO.setup(buttonDelete,GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonShutdown=25
GPIO.setup(buttonShutdown,GPIO.IN, pull_up_down=GPIO.PUD_UP)

buttonWebserver=14
GPIO.setup(buttonWebserver,GPIO.IN, pull_up_down=GPIO.PUD_UP)




readyForRemoval=False
dashCam=False
countForNoStorage=0



#this will perform a status notification on how much storage we have left
time.sleep(1.5)

#1 blink = low storage
#2 -3 blinks = mid-range left
#4 blinks = good amount of storage
gigabytes_avail=getStorage()

#I am using a 32Gb card, the OS does not take up too much space
#24Gigs would roughly be considered maximum storage available
blink=int(gigabytes_avail)/float(6)#this would split maximum space

#need an int / rounded #
blink=round(blink)


#handle any exceptions
if int(blink)>=5:
    blink=int(4) #max
elif int(blink)<1:
    blink=int(1) #min
    
    
#will blink that number of times
for i in range(blink):
    GPIO.output(orangeLED,GPIO.LOW)
    time.sleep(0.3)
    GPIO.output(orangeLED,GPIO.HIGH)
    time.sleep(0.3)

GPIO.output(orangeLED,GPIO.LOW)
time.sleep(1.5)

    

countDash=0
countStatus=0
countWeb=0

WebServer=False


while True:
    

    trueOrFalse=areWeGoodOnStorage()



    if trueOrFalse is True:
        #if the dashcam switch is up and the status is off
        if GPIO.input(dashSwitch) is GPIO.LOW and GPIO.input(statusSwitch) is GPIO.HIGH:
            #countDash+=1
            if dashCam is False: #new recording not yet started
                startNewRecording()
                dashCam=True
            else: #already running, no harm no foul
                pass


        #blueLED
        if dashCam is True:
            GPIO.output(blueLED,GPIO.HIGH)
        else:
            GPIO.output(blueLED,GPIO.LOW)
            

        ##means we were recording, but now we shut it off
        if GPIO.input(dashSwitch) is GPIO.HIGH and dashCam is True:
            countDash+=1
            if countDash>=14:
                print('stop dash recording')
                camera.stop_recording()
                dashCam=False #next loop through this will shut off the blueLED
                countDash=0
        else:
            countDash=0


        if GPIO.input(dashSwitch) is GPIO.HIGH and GPIO.input(statusSwitch) is GPIO.LOW:
            readyForRemoval=True
             
             
        if GPIO.input(statusSwitch) is GPIO.HIGH and readyForRemoval is True: #ie above will only be done if the dashcam is also off
            countStatus+=1
            if countStatus>=14:
                print('turn status LED off')
                countStatus=0
                readyForRemoval=False
        else:
            countStatus=0
            
            
        if readyForRemoval is True:
            GPIO.output(orangeLED,GPIO.HIGH) #statusLED on
        else:
            GPIO.output(orangeLED,GPIO.LOW) #statusLED on

        #button has been pressed
        if GPIO.input(buttonDelete)==GPIO.LOW:
            if readyForRemoval is True: #ie status switch is up
                delete_recordings()
                
                
        #web server check
        if GPIO.input(buttonWebserver)==GPIO.LOW:
            countWeb+=1 #loop running 10x per second, need to limit how often below is checked
            if WebServer is True and countWeb==1:
                print('Stop server')
                WebServer=False
                process.terminate()
                #processWeb=subprocess.check_output(['ps', 'aux', '|', 'grep', 'http.server'], shell=True)
                
                
            elif WebServer is False and countWeb==1:
                print('Start server')
                WebServer=True
                process=subprocess.Popen(['python', '-m', 'http.server', '7777'])
                #os.system('python -m http.server 7777 &') #old
        else:
            countWeb=0
            

    else: #means little to no storage

        try: #this will save whatever is currently recording, if it is
            camera.stop_recording()
        except:
            pass


        #regardless of any of the switches' states
        if GPIO.input(buttonDelete)==GPIO.LOW:
            print('button press on blinking')
            delete_recordings()

            

        #alternate blinking to let me know the current issue
        if countForNoStorage==0:
            GPIO.output(orangeLED,GPIO.LOW)
            GPIO.output(blueLED,GPIO.HIGH)
            countForNoStorage+=1
        elif countForNoStorage==1:
            GPIO.output(orangeLED,GPIO.HIGH)
            GPIO.output(blueLED,GPIO.LOW)
            countForNoStorage-=1

        time.sleep(0.3)

    

    
    #shutdown
    if GPIO.input(buttonShutdown)==GPIO.LOW:
        try:
            camera.stop_recording()
        except:
            pass
        
        print('begin shutdown')
        os.system('sudo shutdown -h now')
        print('I should not be reading this')
    

    #add at least _some_ general limits on the while loop
    time.sleep(0.1)