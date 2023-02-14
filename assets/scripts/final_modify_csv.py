import os, sys
from time import sleep
import csv


#introduction to script
print('This script will modify responses from a google form to bulk update new users into the Google Admin Console.\n')
sleep(1)
print('This script assumes the following:\n')
sleep(0.5)
print('--> The downloaded google form (csv file) will be located at "C:\\Users\\<Current User>\Downloads\\New Users.csv\\New Users.csv"')
sleep(0.5)
print('--> An updated csv file of already existing users will be located at "C:\\Users\\<Current User>\Downloads\\Existing Users.csv"')
sleep(0.5)
print("--> If either of these are not true, the script will not run. The latter file can be found on the Google Admin 'Users' page, and the former will need to be made by yourself for your company's needs.")
sleep(1.5)


#check if file exists
print('\n\nAttempting to read files:')
print('\nNew User file...')
path="C:\\Users\\"+str(os.getlogin())+"\\Downloads\\New Users.csv\\New Users.csv"
if not os.path.isfile(path):
    print('Given path: ', path, ' is not valid.')
    print('Please confirm the file exists where it should and restart this program to try again. Goodbye.')
    exit_now=input('<Press any key to exit>')
    if exit_now:
        sys.exit()
else:
    print("File path is valid.")




#check for existing users file
print('\nExisting Users file...')
path_old="C:\\Users\\"+str(os.getlogin())+"\\Downloads\\Existing Users.csv"
if not os.path.isfile(path):
    print('Given path: ', path, ' is not valid.')
    print('Please confirm the file exists where it should and restart this program to try again. Goodbye.')
    exit_now2=input('Press any key to exit')
    if exit_now2:
        sys.exit()
else:
    print("File path is valid.")


#now to get the emails within
existing_email_list=[]

#file should always download with the emails in the third column
with open(path_old, 'r') as existing_users:
    csvreader_old=csv.reader(existing_users)
    fields=next(csvreader_old)
    for row in csvreader_old:
        existing_email_list.append(row[2])



#now open up the contents of google form
fields=[]
rows=[]
with open(path, 'r') as csvfile:
    csvreader=csv.reader(csvfile)
    fields=next(csvreader)
    for row in csvreader:
        rows.append(row)

#how google forms formats their entries, needs reversing
rows.reverse()

# we will only ever need to be working with the top 10 entries
while len(rows)>10:
    rows.pop() #delete anything older


print('\n\nThe latest 10 entries are shown below, "0" is the most recent:\n')
for row in rows:
    print("("+str(rows.index(row))+') '+row[0]+' by '+row[1])

#get the submission via input
select_submission=input('Enter the corresponding number from 0-9 for the form submission you wish to interact with: ')

while str(select_submission) not in [str(i) for i in range(0,len(rows))]:
    select_submission=input('Enter the corresponding number from 0-9 for the form submission you wish to interact with: ')


#save the number
final_choice=int(select_submission)


#grab info only specific to that entry
UserInfo=rows[final_choice]
while str(UserInfo[-1])==str(""):
    UserInfo.pop()
TimeDate=UserInfo[0]
EnteredBy=UserInfo[1]
Location=UserInfo[2]

num_of_new_users=int(int(len(UserInfo)-3)/int(2))

print('\n\nNumber of new users to be entered: '+str(num_of_new_users))

#default values below, MKE is the outlier
EmailExtension='@<your domain here>'
Department='Whatever you choose'
EmployeeType='E.g. Teacher'
ChangePasswordatNextSign_In="False"
DefaultFalse="False"


if str(Location)=="Example1":
    BuildingID='BLDG1'
    Domain='/subdomain1' #NOTE: This automatically includes the your main / parent domain --> do NOT add
elif str(Location)=="Example2":
    BuildingID='BLDG2'
    Domain='/subdomain2'
elif str(Location)=="Example3":
    BuildingID='BLDG4'
    Domain='/subdomain3'
elif str(Location)=="Example4":
    BuildingID='BLDG4'
    Domain='/subdomain4'
    EmailExtension='Change email'
    Department='Change department'
    EmployeeType='Change employee type'
else:
    print("Check form submissions... something has been changed with these values that needs to reflect in the script.")
    print("Location error with: ",str(Location)
    exit_now3=input('<Press any key to exit>')
    if exit_now3:
        sys.exit()


#used to write to new csv file
GenerateInfo=[]


#gather up needed info
for j in range(3):
    UserInfo.pop(0)
for i in range(num_of_new_users):
    grouping=int(i*2)
    name=UserInfo[grouping].split(" ")
    attribute_from_form=str(UserInfo[grouping+1])

    #print(attribute_from_form)


    first,last=str(name[0]),str(name[1])
    password=str(attribute_from_form)
    email=str(str(first[0].lower())+str(last.lower())+EmailExtension)

    final=[first,last,email,password,Domain,EmployeeType,Department,BuildingID,ChangePasswordatNextSign_In,DefaultFalse]

    GenerateInfo.append(final)

#main write to new file function
def generate_csv(GenerateInfo):
    write_fields=['First Name [Required]','Last Name [Required]','Email Address [Required]','Password [Required]','Password Hash Function [UPLOAD ONLY]','Org Unit Path [Required]','New Primary Email [UPLOAD ONLY]','Recovery Email','Home Secondary Email','Work Secondary Email','Recovery Phone [MUST BE IN THE E.164 FORMAT]','Work Phone','Home Phone','Mobile Phone','Work Address','Home Address','Employee ID','Employee Type','Employee Title','Manager Email','Department','Cost Center','Building ID','Floor Name','Floor Section','Change Password at Next Sign-In','New Status [UPLOAD ONLY]','Advanced Protection Program enrollment']
    write_rows=[]
    add_i=0
    while os.path.isfile("C:\\Users\\"+str(os.getlogin())+"\\Downloads\\UPLOAD_ME_"+str(add_i)+".csv"):
        add_i+=1

    determined_path="C:\\Users\\"+str(os.getlogin())+"\\Downloads\\UPLOAD_ME_"+str(add_i)+".csv"



    with open(str(determined_path), "w") as new_csv:

        for item in GenerateInfo:

            #check if email already exists first
            if str(item[2]) not in existing_email_list: #loaded earlier

                temp_row=['' for i in range(len(write_fields))]

                temp_row[0]=str(item[0]) #first name
                temp_row[1]=str(item[1]) #last name
                temp_row[2]=str(item[2]) #email
                temp_row[3]=str(item[3]) #password
                temp_row[5]=str(item[4]) #organizational unit
                temp_row[17]=str(item[5]) #employee type
                temp_row[20]=str(item[6]) #department
                temp_row[22]=str(item[7]) #building ID
                temp_row[25]=str(item[8]) #change password
                temp_row[27]=str(item[9]) #'false' for advanced protection program enrollment

                write_rows.append(temp_row)
            else:
                print("Email: ",str(item[2])," already in use.\n")

        # creating a csv writer object 
        csvwriter = csv.writer(new_csv) 
        csvwriter.writerow(write_fields) 
        csvwriter.writerows(write_rows)

        new_csv.close()

    return determined_path
            



determined_path=generate_csv(GenerateInfo)

print('Your new file for upload will be located at: '+str(determined_path)+'\n')
print("NOTE: The Google Admin Console does not allow for automatic assignment of users into GROUPS, this will need to be done manually.")
sleep(1)
print("To do this navigate to 'Directory>Groups>All Users' and then manually enter in the following emails you generated.\n")
sleep(1)
#for item in GenerateInfo:
#    if str(item[2]) not in existing_email_list:
#        print(item[2])

print("\nAs a final note, be aware that emails that were already taken will need to be redone, and the above steps should be completed manually instead this time.")
sleep(1)
press_enter=input('<Press any key to exit>')
sys.exit()
