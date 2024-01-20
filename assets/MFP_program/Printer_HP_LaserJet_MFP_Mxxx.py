import getpass
import csv
import requests
from bs4 import BeautifulSoup
import sys

def main(finalResults,ip,tryPing,Logging,base_folder,usedate,CheckName,CheckNetworkFolder):

    base_url='http://'+str(ip)+'/set_config_scantoConfiguration.html?tab=Scan&menu=ScantoCfg'

    scan_page = requests.get(base_url)

    #These printers did not actually require a login, so some steps here are not needed, but I kept them to not disrupt the formatting
    if scan_page.status_code==200:
        print('  > Successful retrieval.')
        settings_response = 'Continue...'
    else:
        print('  > Failed error code check.')
        pingResult=tryPing(ip)
        print('  > Skipping this IP address for now, reference error log for more info.')
        settings_response='Login Failed'


    if settings_response!='Login Failed':
        passThisTime=False

        saveToFileName=str(ip.replace('.','_'))+'.html'

        if scan_page.status_code==200:
            Logging(' * StatusCode: 200 for IP: '+str(ip)+'\n')
            print('  > Status code: 200')

            try:
                with open(base_folder+str(usedate)+'/'+saveToFileName,'w') as saveTo:
                    saveTo.write(scan_page.text)
                saveTo.close()                
                print('  > Successful download of addressbook, saved to:',str(saveToFileName))
            except:
                print('  > Error saving data to csv file.')
                Logging(' ! Error writing content to file.\n')
                passThisTime=True

        else:
            Logging(' ! StatusCode: '+str(scan_page.status_code)+' for IP: '+str(ip)+'\n')
            print('  > Status code:',str(scan_page.status_code))


        if passThisTime is False:

            with open(base_folder+str(usedate)+'/'+saveToFileName,'r') as readHTML:
                
                soup=BeautifulSoup(readHTML,'html.parser')

                rows = soup.select('table.mainContentArea tr')

                data=[]
                checkAgainstListNames=[]
                checkAgainstListNetwork=[]

                for row in rows[1:]:  #Skip the header row
                    columns = row.find_all('td')
                    if columns:
                        if len(columns) >= 3: #'good' line is actually ~15+ elements in the list, this'll just avoid those that are 0-1 in len()
                            display_name = columns[1].get_text(strip=True)
                            network_path = columns[2].get_text(strip=True)

                            if display_name!='' and network_path!='':
                                checkAgainstListNames.append(display_name)
                                checkAgainstListNetwork.append(network_path)
                                data.append({'Display Name': display_name, 'Network Path': network_path})

                for name in CheckName:
                    for getname in checkAgainstListNames:
                        if name.lower()==getname.lower():

                            print('  > Matching name found: '+str(name)+' - ID: <none>')
                            Logging('  > Matching name found: '+str(name)+' - ID: <none>')
                            finalResults.append([ip,name+' - ID: <none>',False])
                            break

                for networkNamePath in CheckNetworkFolder:
                    for entireFolderPath in checkAgainstListNetwork:
                        if networkNamePath.lower() in entireFolderPath.lower(): 
                            print('  > Matching network path found: '+str(networkNamePath)+' - ID: <none>')
                            Logging('  > Matching network path found: '+str(networkNamePath)+' - ID: <none>')
                            finalResults.append([ip,False,networkNamePath+' - ID: <none>'])
                            break
                        
    return finalResults