import requests
from bs4 import BeautifulSoup
import sys, os
import csv
import time
from datetime import datetime
import getpass
import subprocess

sys.path.append('directory/hosting/your/printer/profiles/')
from Printer_MX_5070N import main as MX_5070N
from Printer_MX_4070N import main as MX_4070N
from Printer_MX_4141N import main as MX_4141N
from Printer_MX_5141N import main as MX_5141N
from Printer_HP_LaserJet_MFP_Mxxx import main as HP_LaserJet_MFP_Mxxx
from Printer_TopAccess_MFPxxxxxxxx import main as TopAccess_MFP
from Printer_KYOCERA_CS_4501i import main as KYOCERA_CS_4501i


current_time = datetime.now()
usedate = current_time.strftime('%Y-%m-%d_%H-%M-%S')
user=getpass.getuser()
base_folder='directory/hosting/your/printer/profiles/csvsForScanners/'


def Logging(text_to_write):
    try:
        logit=open('directory/hosting/your/printer/profiles/csvsForScanners/combinedLogAndErrorFile.txt','a')
        logit.write(text_to_write)
        logit.close()
    except FileNotFoundError:
        logit=open('directory/hosting/your/printer/profiles/csvsForScanners/combinedLogAndErrorFile.txt','w')
        logit.write(text_to_write)
        logit.close()

Logging('\n\nNew Error / Event Log // User: '+str(user)+' // Date/time: @'+str(current_time)+':\n\n ---- Begin Program ----\n')


print('This program will identify which scanners a user has been added to. Some more information is needed, and letter case is irrelevant.\n')

first=input('Enter their first name now: ')
last=input('Enter their last name now: ')
nickname=input('Optional nickname entry, press enter to skip: ')
username=input('Enter expected Username (commonly FirstInitialLastName) where their H: drive saves to: ')

time.sleep(0.5)
Logging(' * Targeting User - First Name: '+str(first)+', Last Name: '+str(last)+', Nickname: '+str(nickname)+', and Expected Username: '+str(username)+'\n')


def generateInfoFromNames(first,last,nickname,username):

    possibleFullNames=[]
    possibleNetworkFolder=[]

    if len(first)>0 and len(last)>0:

        #some of below may be obsolete after adding a generic .lower() check in the printer profiles
        possibleFullNames.append(first[0].upper()+' '+last[:1].upper()+last[1:].lower())
        possibleFullNames.append(first[0].upper()+'. '+last[:1].upper()+last[1:].lower())
        possibleFullNames.append(first[0].upper()+first[1:].lower()+' '+last[:1].upper())

        possibleFullNames.append(first+' '+last[0]+'.')
        possibleFullNames.append(first)

        possibleFullNames.append(first+' '+last)
        possibleFullNames.append(last[:1].upper()+last[1:].lower()+', '+first[0].upper()+first[1:].lower())
        possibleFullNames.append(first[:1].upper()+first[1:].lower()+' '+last[:1].upper()+last[1:].lower())

        possibleFullNames.append(nickname)
        possibleFullNames.append(nickname.lower())
        possibleFullNames.append(nickname[:1].upper()+nickname[1:].lower())

        possibleNetworkFolder.append(username)
        possibleNetworkFolder.append(first[0].lower()+last.lower())
        
    return possibleFullNames,possibleNetworkFolder


CheckName,CheckNetworkFolder=generateInfoFromNames(first,last,nickname,username)

#Remove duplicates
CheckName=set(CheckName)
CheckNetworkFolder=set(CheckNetworkFolder)

print(CheckName,CheckNetworkFolder)
Logging(' * Generated CheckNames list: '+str(CheckName)+'\n')
Logging(' * Generated CheckNetworkFolder list: '+str(CheckNetworkFolder)+'\n')

#Check scanners for user to delete from
locations=['Location1','Location2','<Check All Locations>']

print('Thanks. Now enter the number for the location you wish to search:\n')
for i in range(len(locations)):
    time.sleep(0.3)
    print(str(i+1)+' : '+str(locations[i]))
time.sleep(0.5)

badInput="1"
print('Chosen location: '+str(locations[int(badInput)-1])+'\n')
Logging(' * Chosen location for checks at: '+str(locations[int(badInput)-1])+'\n')


dictLocationsToIPLists={
    #replace below x.x.x.x with actual IP addresses
    'Location1':[('x.x.x.x','MX_5070N'),('x.x.x.x','MX_4141N'),('x.x.x.x','MX_5141N'),('x.x.x.x','MX_4070N'),('x.x.x.x','HP_LaserJet_MFP_Mxxx'),('x.x.x.x','HP_LaserJet_MFP_Mxxx'),('x.x.x.x','HP_LaserJet_MFP_Mxxx'),('x.x.x.x','HP_LaserJet_MFP_Mxxx'),('x.x.x.x','HP_LaserJet_MFP_Mxxx'),('x.x.x.x','HP_LaserJet_MFP_Mxxx'),('x.x.x.x','HP_LaserJet_MFP_Mxxx'),('x.x.x.x','HP_LaserJet_MFP_Mxxx')],
    'Location2':[]
}

CheckAll = []
for key, value in dictLocationsToIPLists.items():
    for elem in value:
        CheckAll.append(elem)


checkTheseIPs=dictLocationsToIPLists[locations[int(badInput)-1]]
Logging(' * Testing IPs: '+str(checkTheseIPs)+'\n')


#make folders, check if they exist, etc
if os.path.exists(base_folder) and os.path.isdir(base_folder):
    pass
else:
    os.makedirs(base_folder)

#create subfolder
try:
    os.makedirs(base_folder+str(usedate))
except:
    Logging(' ! Error creating subfolder in base_folder. Program exited.\n')


######################################################
#start web stuff now
######################################################

def tryPing(ip_address):
    try:
        result = subprocess.run(['ping', '-c', '4', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print(f"  > Ping successful, there is another issue.")
            Logging(' ! Login failed: test credentials.\n')
        else:
            print("  > Ping failed, printer may be offline.")
            Logging(' ! Login failed: ping was successful.\n')

    except Exception as e:
        print(f"  > A different error occurred: {str(e)}")
        Logging(f"A different error occurred: {str(e)}"+'\n')

print('\n\nSaving to base folder: '+base_folder+'\n')


finalResults=[]

for ip_and_type in checkTheseIPs:

    ip=ip_and_type[0]
    type=ip_and_type[1]
    print('\nChecking IP:',ip)

    if type=="MX_5070N":
        MX_5070N(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder)
    elif type=="MX_4141N":
        MX_4141N(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder)
    elif type=="MX_5141N":
        MX_5141N(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder)
    elif type=="MX_4070N":
        MX_4070N(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder)
    elif type=="HP_LaserJet_MFP_Mxxx":
        HP_LaserJet_MFP_Mxxx(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder)
    elif type=="TopAccess_MFP":
        TopAccess_MFP(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder)
    else:
        print('No profile for this printer type yet:',type)


print('\n\n\nFor the network printers that were online and accessible (reference error log for those that were not), the following matches to the below user were found:')
print('\n>> Using Parameters - First:',first,'/ Last:',last,'/ Nickname:',nickname,'/ Username:',username,'<<\n')

def networkOrName(result):
    if result[1]==False:
        return 'Network Path: '+str(result[2])
    elif result[2]==False:
        return 'Name: '+str(result[1])
    else:
        print('how da hell did you mess this up?')
        time.sleep(5)
        sys.exit()

for result in finalResults:
    print('  > Match found at IP:',ip,'using',networkOrName(result))

if finalResults==[]:
    print('\n  > No matches were found with those parameters.\n')
    Logging(' ! No matches were found.\n')

Logging(' ---- Program Complete ----\n')

exitProgram=input('\nPress [ENTER] now to exit the program.')