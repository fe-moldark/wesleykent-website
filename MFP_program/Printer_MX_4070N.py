import getpass
import csv
import requests

def main(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder):


    login_url='http://'+str(ip)+'/login.html?/sysmgt_storagebackup_csv.html'
    password = 'your_password'

    #need to maintain session since we are logging in
    session = requests.Session()
    login_page_response = session.get(login_url)

    login_data = {
        'ggt_select(10009)': '3',
        'ggt_textbox(10003)': password,
        'action': 'loginbtn',
        'token2': '', #not needed apparently - t
        'ordinate': '0',
        'ggt_hidden(10008)': '5'
    }

    #Login now
    login_response = session.post(login_url, data=login_data)

    # Check if login was successful
    if 'Export' in login_response.text:
        print('  > Successful login.')
        
        settings_url = 'http://'+str(ip)+'/sysmgt_storagebackup_csv.html'
        export_url=str(settings_url)
        settings_response = session.get(settings_url)

    else:
        print('  > Failed login.')
        pingResult=tryPing(ip)
        print('  > Skipping this IP address for now, reference error log for more info.')

        session.close()
        settings_response='Login Failed'

    #keep going
    if settings_response!='Login Failed':

        passThisTime=False
        try_and_get=session.get('http://'+str(ip)+'/storage_backup_csv.html?type=33')
        saveToFileName=str(ip.replace('.','_'))+'.csv'

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

        #open csv file and sift through its data
        if passThisTime is False:

            with open(base_folder+str(usedate)+'/'+saveToFileName,'r') as readCSV:
                csv_reader=csv.reader(readCSV)

                csv_listed=[]
                for row in csv_reader:
                    if len(row)>14:
                        csv_listed.append(row)

                #names
                checkAgainstList=[(row[2],row[1]) for row in csv_listed]
                for name in CheckName:

                    for getname,id in checkAgainstList:
                        if name.lower()==getname.lower():
                            print('  > Matching name found: '+str(name)+' - ID: '+str(id))
                            Logging('  > Matching name found: '+str(name)+' - ID: '+str(id))
                            finalResults.append([ip,name+' - ID: '+str(id),False])
                            break
                    
                #network folder
                checkAgainstList=[(row[15],row[1]) for row in csv_listed]

                for networkNamePath in CheckNetworkFolder:
                    for entireFolderPath,id in checkAgainstList:
                        if networkNamePath.lower() in entireFolderPath.lower(): 
                            print('  > Matching network path found: '+str(networkNamePath)+' - ID: '+str(id))
                            Logging('  > Matching network path found: '+str(networkNamePath)+' - ID: '+str(id))
                            finalResults.append([ip,False,networkNamePath+' - ID: '+str(id)])
                            break

    return finalResults