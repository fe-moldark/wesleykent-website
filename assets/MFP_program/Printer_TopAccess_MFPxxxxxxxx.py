import getpass
import csv
import requests
from bs4 import BeautifulSoup
import sys


#note for this printer / scanner:
#the location of users that can scan to network folders is NOT under Registratino>Address Book
#it is also NOT under User Management
#instead, it is under Administration>Registration




#login page: /?MAIN=LOGIN

#export address button at Admin>Main>Export>Create new file>template


"""
<DeviceInformationModel>
  <SetValue overrideDelta="false">
    <Payload>
      <path>
        TopAccess/SessionInfo/USERCRED
      </path>
      <value>
        ,USERNAME:admin,
      </value>
    </Payload>
  </SetValue>
</DeviceInformationModel>
"""
"""
<DeviceInformationModel><GetValue><Authentication><UserCredential></UserCredential></Authentication></GetValue><GetValue><Panel><DiagnosticMode><Mode_08><Code_8913></Code_8913></Mode_08></DiagnosticMode></Panel></GetValue><SetValue><Authentication><UserCredential><userName>admin</userName><passwd>123456</passwd><ipaddress>10.0.60.187</ipaddress><DepartmentManagement isEnable='false'><requireDepartment></requireDepartment></DepartmentManagement><domainName></domainName></UserCredential></Authentication></SetValue><Command><Login><commandNode>Authentication/UserCredential</commandNode><Params><appName>TOPACCESS</appName></Params></Login></Command><SaveSessionInformation><SessionInfo><Information><type>LoginPassword</type><data>123456</data></Information><Information><type>LoginUser</type><data>admin</data></Information></SessionInfo></SaveSessionInformation></DeviceInformationModel>
"""
"""
<DeviceInformationModel><SetValue overrideDelta="false"><Payload><path>TopAccess/SessionInfo/USERCRED</path><value>,USERNAME:admin,USERID:10002,</value></Payload></SetValue></DeviceInformationModel>
"""
"""
<DeviceInformationModel><SetValue overrideDelta="false"><Payload><path>TopAccess/SessionInfo/USERROLE</path><value>:⇔Administrator:⇔AccountManager:⇔CopyOperator:⇔ScanOperator:⇔Print:⇔PrintOperator:⇔eFilingOperator:⇔ColorPrintCopyOperator:⇔FaxOperator:⇔Auditor:⇔Fax:⇔</value></Payload></SetValue></DeviceInformationModel>
"""
"""
<DeviceInformationModel><SetValue overrideDelta="false"><Payload><path>TopAccess/SessionInfo/SESSID</path><value>123456789</value></Payload></SetValue></DeviceInformationModel>
"""
"""
<DeviceInformationModel><SetValue overrideDelta="false"><Payload><path>TopAccess/SessionInfo/TAPERMISSIONS</path><value>ColorPrint,CopyJob,DeviceSetting,EWBAccess,FaxReceivedPrint,FaxTransmission,InternetFaxTransmission,JobOperation,LogExport,LogRead,PrintJob,PrintManagement,RemoteScan,SendEmail,StoreToLocalStorage,StoreToRemoteServer,StoreToUSBDevice,USBDirectPrint,UserDepartmentManagement,WSScanPush,eFilingAccess</value></Payload></SetValue></DeviceInformationModel>
"""
"""
<DeviceInformationModel><SetValue overrideDelta="false"><Payload><path>TopAccess/SessionInfo/DOMAINAME</path><value></value></Payload></SetValue></DeviceInformationModel>
"""
"""
<DeviceInformationModel><SetValue overrideDelta="false"><Payload><path>TopAccess/SessionInfo/LOGINSTATUS</path><value>Authenticated</value></Payload></SetValue></DeviceInformationModel>
"""


def main(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder):

    login_url='http://'+str(ip)+'/?MAIN=LOGIN'
    #'admin'
    #password = '123456'

    #just curl webpage

    session = requests.Session()
    login_page_response = session.get(login_url)

    print(login_page_response.status_code)

    #sys.exit()

    with open(base_folder+'get_html.html','w',encoding='utf-8') as brieflyopen:
        brieflyopen.write(login_page_response.text)
    brieflyopen.close()

    sys.exit()

    #with open()



    #need to maintain session since we are logging in
    #session = requests.Session()
    scan_page = requests.get(base_url)


    # Check if login was successful
    if scan_page.status_code==200:
        print('  > Successful retrieval.')
        
        settings_response = 'Continue...'

        # Process the content of the settings page as needed
        #print(settings_response.text)
    else:
        print('  > Failed error code check.')
        pingResult=tryPing(ip)
        print('  > Skipping this IP address for now, reference error log for more info.')

        settings_response='Login Failed'


    if settings_response!='Login Failed':
        passThisTime=False




        saveToFileName=str(ip.replace('.','_'))+'.html'


        if scan_page.status_code==200: #just do it and check again... no point
            Logging(' * StatusCode: 200 for IP: '+str(ip)+'\n')
            print('  > Status code: 200')

            try:
                with open(base_folder+str(usedate)+'/'+saveToFileName,'w') as saveTo:
                    saveTo.write(scan_page.text)
                saveTo.close()
                
                print('  > Successful download of addressbook, saved to:',str(saveToFileName))
                #saveTo.close()
            except:
                print('  > Error saving data to csv file.')
                Logging(' ! Error writing content to file.\n')

                passThisTime=True

        else:
            Logging(' ! StatusCode: '+str(scan_page.status_code)+' for IP: '+str(ip)+'\n')
            print('  > Status code:',str(scan_page.status_code))



        #open csv file and sift through it
        if passThisTime is False:

            
            with open(base_folder+str(usedate)+'/'+saveToFileName,'r') as readHTML:
                
                soup=BeautifulSoup(readHTML,'html.parser')

                rows = soup.select('table.mainContentArea tr')

                data=[]
                checkAgainstListNames=[]
                checkAgainstListNetwork=[]

                for row in rows[1:]:  # Skip the header row
                    columns = row.find_all('td')
                    if columns:  # Ensure it's not an empty row
                        if len(columns) >= 3:
                            #print(columns)
                            display_name = columns[1].get_text(strip=True)
                            network_path = columns[2].get_text(strip=True)

                            if display_name!='' and network_path!='':
                                checkAgainstListNames.append(display_name)
                                checkAgainstListNetwork.append(network_path)
                                data.append({'Display Name': display_name, 'Network Path': network_path})

                # Print the extracted data
                #for entry in data:
                    #print('saved entry: ',entry)






                #print(len(csv_listed))
                #print(len(csv_listed[0]))
                

                #names
                #checkAgainstListNames=[(row[2],row[1]) for row in csv_listed]#+[row[3] for row in csv_listed]
                for name in CheckName:

                    for getname in checkAgainstListNames:
                        if name.lower()==getname.lower():

                            #pull ID real quick
                            #checkAgainstList.index(name)

                            print('  > Matching name found: '+str(name)+' - ID: <none>')
                            Logging('  > Matching name found: '+str(name)+' - ID: <none>')
                            finalResults.append([ip,name+' - ID: <none>',False])
                            break
                    
                #network folder
                #checkAgainstListNetwork=[(row[15],row[1]) for row in csv_listed]
                #print(checkAgainstList)
                #for row in csv_reader:
                    #print('[]',row)
                for networkNamePath in CheckNetworkFolder:
                    for entireFolderPath in checkAgainstListNetwork:
                        if networkNamePath.lower() in entireFolderPath.lower(): 
                            print('  > Matching network path found: '+str(networkNamePath)+' - ID: <none>')
                            Logging('  > Matching network path found: '+str(networkNamePath)+' - ID: <none>')
                            finalResults.append([ip,False,networkNamePath+' - ID: <none>'])
                            break
    return finalResults