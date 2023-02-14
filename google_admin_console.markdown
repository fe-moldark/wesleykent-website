---
layout: page
title: Generating a CSV file to bulk update the Google Admin Console from Google Form Submissions
subtitle:
permalink: /scripts/google_admin_console/
description: Using a Google Form to generate a CSV file that can bulk update into the Google Admin Console.
---



# What this script does
At the time of writing this I am working in an IT Support role, and part of the responsibilities there include creating and managing user accounts from the Google Admin Console. Creating one or two accounts on occasion is quite simple, however, when large bunches of new users need to be added it can be quite time consuming.
<br><br>
So, I decided to automate parts of this process, because what better way to spend your time than writing a program that takes even more time to write than it will likely end up saving. What this script does is it reads entries from a Google Form sheet and generates a CSV file that I can use to bulk update / create new users on the Admin Console. 
<br><br><br>

# What you will need to change
There are several parts you will need to change if you want to implement this yourself, for instance replacing the \<your domain goes here> sections with your actual domain name, and changing how you want to generate things like emails and passwords. It is not uncommon for a company to create their emails using some form of "firstlast@..." or "firstinitiallast@...", and for passwords to either be set to some default password that needs to be changed or generate one based on their information automatically. I'm hoping that the script is readable enough that you will be able to replicate this easily enough for your own domain.
<br><br><br>

# Before running the script
As always, link the full script can be found <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/scripts/final_modify_csv.py" target="_blank" rel="noopener noreferrer">here</a>. I wrote this knowing I won't always be at the company I currently am at, so this script provides some step-by-step instructions with limited user interaction as well as useful error messages throughout when applicable.
<br><br>
To start off, this script requires an updated file with every user's information (only email required) in your domain from the Admin Console. This can be found at `Directory>Users` and then selecting `Download Users`. Save this to your Downloads folder. This script pulls the information for the CSV file it will generate from a Google Form titled "New Users". Once someone (e.g. HR) populates the form with entries you may (as the owner of the form), navigate to the form's `Responses` heading and download the file from there, also saving it to your Downloads folder. That screen should look like this:<br>
<center>
  <img width="1000" src="/assets/scripts/adminconsole.jpg">
</center>
<br><br><br>

# The script itself
As seen with other scripts I will not be covering every single line, rather just the sections I think need explanations. The first 50 or so lines are validating that files are where they should be. In the event that the format is different than what is expected, you will either run into errors or generate a corrupt / incorrect file.
<br><br>
The first interaction the user will have is choosing which submission they will use from the Google Form spreadsheet. The way the form saves the entries is just by continually appending rows for each new session, so the way I sorted this is by displaying the last ten submissions _Note: each session (row) can have up to x amount of new users each, that number is up to you._ The latest ten submissions will also display who it was that submitted it to more easily locate the session you are trying to find. All that is below:<br>
```python
#now open up the contents of the google form spreadsheet
fields=[]
rows=[]
with open(path, 'r') as csvfile:
    csvreader=csv.reader(csvfile)
    fields=next(csvreader)
    for row in csvreader:
        rows.append(row)

#because of how google forms formats their entries, needs reversing
rows.reverse()

#we will only ever need to be working with the top 10 entries
while len(rows)>10:
    rows.pop() #delete anything older

print('\n\nThe latest 10 entries are shown below, "0" is the most recent:\n')
for row in rows:
    print("("+str(rows.index(row))+') '+row[0]+' by '+row[1])

#get the submission via input
select_submission=input('Enter the corresponding number from 0-9 for the form submission you wish to interact with: ')

while str(select_submission) not in [str(i) for i in range(0,len(rows))]:
    select_submission=input('Enter the corresponding number from 0-9 for the form submission you wish to interact with: ')

#save that number
final_choice=int(select_submission)
```
<br>
Lines 100-130 from the script need to be modified to your particular situation. These changes include the primary domain, different subdomains, and everything else that can be specific to each New User instance. This includes, but is not limited to, Employee ID, Employee Type, Building ID, Phone Numbers, etc. There are a total of 28 different columns you can modify, to see the full list click the `Download Blank CSV Template` on that same `Bulk Update Users` page.
<br><br>
For the example I am using in this script the Google Form accepts only two choices for each new user, and one that applies to all of of the users. The first choice is the first and last names (later split apart), and the third is what will be used to create their password - this can be whatever you set; last 4 of social, birthday, answer to a challenge question, or just do away with this and designate a password like "CHANGETHISPASSWORD" to everyone. The final entry that applies to all users of that submission is their location, e.g. "BLDG2".
<br><br>
The email is generated using the first initial of the first name combined with the last name, the password is whatever other attribute was submitted, and with the other gathered information a list containing all pertinent data is appended to the `GenerateInfo` list for each user:<br>
```python
#used to write to new csv file
GenerateInfo=[]

#gather up needed info
for j in range(3):
    UserInfo.pop(0)
	
for i in range(num_of_new_users):
    grouping=int(i*2)
    name=UserInfo[grouping].split(" ")
    attribute_from_form=str(UserInfo[grouping+1])

    first,last=str(name[0]),str(name[1])
    password=str(attribute_from_form)
    email=str(str(first[0].lower())+str(last.lower())+EmailExtension)

    final=[first,last,email,password,Domain,EmployeeType,Department,BuildingID,ChangePasswordatNextSign_In,DefaultFalse]

    GenerateInfo.append(final)
```
<br>
Finally, we can use this information to create that CSV file you've been hearing about this whole time:<br>
```python
#main write to new file function
def generate_csv(GenerateInfo):
    write_fields=['First Name [Required]','Last Name [Required]','Email Address [Required]','Password [Required]','Password Hash Function [UPLOAD ONLY]','Org Unit Path [Required]','New Primary Email [UPLOAD ONLY]','Recovery Email','Home Secondary Email','Work Secondary Email','Recovery Phone [MUST BE IN THE E.164 FORMAT]','Work Phone','Home Phone','Mobile Phone','Work Address','Home Address','Employee ID','Employee Type','Employee Title','Manager Email','Department','Cost Center','Building ID','Floor Name','Floor Section','Change Password at Next Sign-In','New Status [UPLOAD ONLY]','Advanced Protection Program enrollment'] #headers
    write_rows=[]
    add_i=0
    while os.path.isfile("C:\\Users\\"+str(os.getlogin())+"\\Downloads\\UPLOAD_ME_"+str(add_i)+".csv"):
        add_i+=1 #don't overwrite, just increase the file number

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

            else: #this will not add that user to the CSV file
                print("Email: ",str(item[2])," already in use.\n")

        # creating a csv writer object 
        csvwriter = csv.writer(new_csv) 
        csvwriter.writerow(write_fields) 
        csvwriter.writerows(write_rows)

        new_csv.close()

    return determined_path
            
            
determined_path=generate_csv(GenerateInfo)
```
<br>
That `else` condition is handling any instance where you are trying to create an email that already exists in the user database. Catching this is important because instead of creating a new user you would end up "updating" the existing user with all new information, including a password change which would now give someone else access to the initial person's email, google drive, and more. That's practically the end of the script, the only remaining steps are for you to upload that document and watch it ~~fail~~ work flawlessly the first time around.
<br><br><br>

# Final thoughts
There are obvious pitfalls to this. An easy example would be someone submitting a middle name as well which would result in an incorrect email and first / last name, but there are more. I would recommend you restructure this in a way that makes sense for your particular situation since you will no doubt want to assign different and/or more attributes than I did, or you want to generate the email names differently, etc. Do whatever works for you, and if you need me to explain something more in depth [I would be happy to get back to you](/contact). Before bulk updating new users I would recommend confirming one or two test users are working as expected, and then move into the 20+ people at a time range.
<br><br>
