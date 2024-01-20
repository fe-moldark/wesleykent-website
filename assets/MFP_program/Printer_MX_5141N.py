import getpass
import csv
import requests
import sys
import xml.etree.ElementTree as ET

def main(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder):

    login_url='http://'+str(ip)+'/login.html?/storagebackup.html'
    password = 'admin'

    #Need to maintain session since we are logging in
    session = requests.Session()
    login_page_response = session.get(login_url)

    login_data = {
        'ggt_select(10009)': '3', #default and only option in this case
        'ggt_textbox(10003)': password,
        'action': 'loginbtn',
        'ordinate': '0',
        'ggt_hidden(10008)': '5'
    }

    #Login
    login_response = session.post(login_url, data=login_data)

    #Check if login was successful
    if 'Export' in login_response.text:
        print('  > Successful login.')
        settings_url = 'http://'+str(ip)+'/storagebackup.html'
        export_url=str(settings_url)
        settings_response = session.get(settings_url)
    else:
        print('  > Failed login.')
        pingResult=tryPing(ip)
        print('  > Skipping this IP address for now, reference error log for more info.')

        session.close()
        settings_response='Login Failed'


    if settings_response!='Login Failed':
        passThisTime=False

        #POST: ggt_checkbox%281%29=1&ggt_textbox%287%29=&action=executebtn&ordinate=
        #GET: GET /storage_backup.html?000000000000064 HTTP/1.1
        try_and_get=session.get('http://'+str(ip)+'/storage_backup.html?000000000000064')
        saveToFileName=str(ip.replace('.','_'))+'.xml'

        if try_and_get.status_code==200:
            Logging(' * StatusCode: 200 for IP: '+str(ip)+'\n')
            print('  > Status code: 200')

            try:
                with open(base_folder+str(usedate)+'/'+saveToFileName,'w') as saveTo:
                    saveTo.write(try_and_get.text)
                saveTo.close()
                print('  > Successful download of addressbook, saved to:',str(saveToFileName))
            except:
                print('  > Error saving data to csv file.')
                Logging(' ! Error writing content to file.\n')

                passThisTime=True

        else:
            Logging(' ! StatusCode: '+str(try_and_get.status_code)+' for IP: '+str(ip)+'\n')
            print('  > Status code:',str(try_and_get.status_code))

        session.close()


        #open csv file and sift through it
        if passThisTime is False:

            tree = ET.parse(base_folder+str(usedate)+'/'+saveToFileName)
            root = tree.getroot()
            checkAgainstList=[]

            count0=0
            for address_name in root.iter('address'):#display-name'):
                count0+=1

                #Parse through the xml data here
                value_elem = address_name.find('./display-name/data/value')

                if value_elem is not None:

                    value = str(value_elem.text)

                    for name in CheckName:
                        if name.lower()==value.lower():
                            print('  > Matching name found: '+str(name)+' - ID: '+str(address_name.find('./id/data/value').text))
                            Logging('  > Matching name found: '+str(name)+' - ID: '+str(address_name.find('./id/data/value').text))
                            finalResults.append([ip,name+' - ID: '+str(address_name.find('./id/data/value').text),False])  
                            break          
                                
                networkloc_elem = address_name.find('./smb/directory/data/value')
                
                if networkloc_elem is not None:

                    value = str(networkloc_elem.text)
                    for name in CheckNetworkFolder:
                        if name.lower() in value.lower():
                            print('  > Matching network path found: '+str(name)+' - ID: '+str(address_name.find('./id/data/value').text))
                            Logging('  > Matching network path found: '+str(name)+' - ID: '+str(address_name.find('./id/data/value').text))
                            finalResults.append([ip,False,name+' - ID: '+str(address_name.find('./id/data/value').text)]) 
                            break
                
    return finalResults