from time import sleep
from time import time
import os
import wiringpi as wpi
from subprocess import Popen


wpi.wiringPiSetup()
wpi.pinMode(24, 0)
wpi.pinMode(5, 0)
wpi.pinMode(6, 0)
wpi.pinMode(3, 0)
wpi.pinMode(21, 0)

wpi.pinMode(25, 1)
wpi.pinMode(27, 1)
wpi.pinMode(29, 1)
wpi.pinMode(26, 1)

wpi.digitalWrite(25, 0)
wpi.digitalWrite(27, 0)
wpi.digitalWrite(29, 0)
wpi.digitalWrite(26, 0)

# no LEDs on
defineLEDs = [25, 27, 29, 26]
for LED in defineLEDs:
    wpi.digitalWrite(LED, 0)


def LEDsequence():
    increment = .1
    print("Test LED sequence...")
    for LED in defineLEDs:
        wpi.digitalWrite(LED, 1)
        sleep(increment)
    for LED in defineLEDs:
        wpi.digitalWrite(LED, 0)
        sleep(increment)
    for LED in defineLEDs[::-1]:
        wpi.digitalWrite(LED, 1)
        sleep(increment)
    for LED in defineLEDs[::-1]:
        wpi.digitalWrite(LED, 0)
        sleep(increment)
    print("...and end.")


LEDsequence()

start_time = time()

pygameProgram='showcasev2.py'


def startMyProgramCheck():
    isRunning = os.popen('ps aux | grep '+str(pygameProgram)).read()
    print(len(isRunning))
    print(isRunning)
    mod = str(isRunning)
    modList = mod.split("\n")
    finalPID=[]

    for item in modList:
        
        try:

            #okay I changed this method so it is now searching for that python keyword
            #the rest of the string WILL be found as a result of the 'ps aux' command
            #this method is working, and better than filtering by the user running the process as done before

            #if str(item).find('python /home/pi/showcasev2.py'):# and str(item)[0:4]!=str("root"):#modList=mod.split("\n")
            if 'python' in str(item):
                #print('CHECKIN: ',str(item)[0:4])
                getPID=str(item)
                addToList=''
                while getPID[0] not in [str(i) for i in range(10)]:#ie a num
                    getPID=getPID[1:]
                while getPID[0] in [str(i) for i in range(10)]:#is is a num
                    addToList+=str(getPID[0])
                    getPID=getPID[1:]
                    
                #print('finalPID: ',addToList)
                finalPID.append(addToList)
                                        
            #print('possible: ', item)

        except IndexError:
            pass #print('failure!',getPID)

    if finalPID!=[]: #means program is ALREADY running
        #print('killing program(s) now!')
        for toKill in finalPID:
            #print('Killing: ',toKill)
            os.system('kill '+str(toKill))
    else:
        #print('not yet started, so program will start')
        os.popen('python /home/pi/'+str(pygameProgram)) #start the new instance of the program
        #sys.exit()

    start_time = time()
    
    


while True:

    #my program check
    if wpi.digitalRead(24) == 0:
        if float(time()-start_time) > float(1):
            startMyProgramCheck()

    if wpi.digitalRead(5) == 0:
        if float(time()-start_time) > float(1):
            print("5")
            start_time = time()
    if wpi.digitalRead(6) == 0:
        if float(time()-start_time) > float(1):
            os.system("sudo shutdown -h now")
            start_time = time()
    if wpi.digitalRead(3) == 0:
        if float(time()-start_time) > float(1):
            os.system("sudo shutdown -r now")
            start_time = time()

    # battery monitor - not currently working
    if wpi.digitalRead(21) == 0:
        if float(time()-start_time) > float(1):
            # batteryStatus=os.popen('python3 /home/pi/UPS_HAT_B/INA219.py').read()
            print('trying battery')
            start_time = time()

    sleep(.1)
