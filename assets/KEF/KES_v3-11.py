# Program name  :  Kent Encryption Standard
# Author        :  Wesley Kent
# Date          :  02/09/2025
# Version       :  3.11
# Link          :  https://wesleykent.com/about/
# Link          :  https://github.com/fe-moldark
# Description   :  Converts a six column csv file, delimited by a semicolon, into an encrypted password wallet.
#               :  Allows the user to modify, add, delete and display data once the wallet is decrypted.


import hashlib, random
import os, sys, time
import getpass
import csv

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header

import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom
from datetime import datetime

import tkinter as tk
from tkinter import filedialog
import re


global newFile
newFile=False

global version, revision
version='3'
revision='11'

# pyinstaller --onefile --icon=icon2.png filename.py

# This will produce the primary hash and the 128x128 hash array used to encode individual chars
# This design limits the input file to ~16,000 ascii chars, which is more than enough for a password file
def generate_hash_stuff(password,logModifier): # The logModifier is the logMod, or the mod value pulled from the initial file or subsequent saves

    # Adding the logModifier ensures multiple versions of the wallet cannot be used to identifier key pairs where the total adds to a consistent value with the same hashed password
    # This would be difficult to accomplish in practice and require probably 3+ past versions of the wallet, but it's a theoretical vulnerability I'm avoiding
    password_clear=str(password)+str(logModifier)
    sha512_hash=str(hashlib.sha512(password_clear.encode()).hexdigest()) # 128 ascii character length
    sha512_hash_reverse=sha512_hash[::-1]

    hash_array_128x128=[[char for char in sha512_hash]]
    for row in range(1,128):
        modifier=sha512_hash_reverse[row]
        new_list=[modifier]

        def combine_hex(hex1, hex2):
            total = (int(hex1, 16) + int(hex2, 16)) % 16
            return hex(total)[-1]

        for col in range(1,128):
            new_val=combine_hex(modifier,sha512_hash[col])
            new_list.append(new_val)

        hash_array_128x128.append(new_list)

    # Use below as just a single string of the hash array
    hash_array_as_one_string=''.join([item for sublist in hash_array_128x128 for item in sublist])

    return sha512_hash,sha512_hash_reverse,hash_array_128x128,hash_array_as_one_string


# 'W' in this case is going to be the index of the current letter that is being encoded
def get_locations_within_an_array(sha512_hash,hash_array_as_one_string,w):

    original_hash=str(sha512_hash)
    new_hash=str(hash_array_as_one_string[0:w])
    md5_this=original_hash+new_hash # Used to create a unique hash for each char in the 16x16 array

    md5_hash=hashlib.md5(md5_this.encode()).hexdigest()

    # This section could be a lot prettier...
    # The locations' uses are explained later
    location1=(md5_hash[0],md5_hash[1])
    base_pair=(2,3)
    location2=(md5_hash[base_pair[0]],md5_hash[base_pair[1]])
    while location2==location1:
        base_pair=(base_pair[0]+2,base_pair[1]+2)
        location2=(md5_hash[base_pair[0]],md5_hash[base_pair[1]])

    base_pair=(base_pair[0]+2,base_pair[1]+2)
    location3=(md5_hash[base_pair[0]],md5_hash[base_pair[1]])
    while location3 in [location1,location2]:
        base_pair=(base_pair[0]+2,base_pair[1]+2)
        location3=(md5_hash[base_pair[0]],md5_hash[base_pair[1]])

    base_pair=(base_pair[0]+2,base_pair[1]+2)
    location4=(md5_hash[base_pair[0]],md5_hash[base_pair[1]])
    while location4 in [location1,location2,location3]:
        base_pair=(base_pair[0]+2,base_pair[1]+2)
        location4=(md5_hash[base_pair[0]],md5_hash[base_pair[1]])
    
    return location1,location2,location3,location4


one=1 # Stupid formatting issues with color fml
two=2
scroll=['\nWelcome to the \033[34mKent Encryption Standard\033[0m. Please select from the following options:',f'\n  \033[34m{one}\033[0m - Encrypt a file',f'  \033[34m{two}\033[0m - Decrypt a file\n\n']
for line in scroll:
    time.sleep(0.5)
    print(line)
time.sleep(1)


program_choice=input('>> ')
while program_choice not in ['1','2']:
    print(f" ! \033[31mOptions are either \033[34m{one}\033[31m or \033[34m{two}\033[0m. Try again.")
    program_choice=input('>> ')
print('')


# This will take two hex chars and 'combine' them to a hex char (e.g. '3' + 'a' = 'e')
def combine_hex_values(hex1, hex2):
        
    int1 = int(hex1, 16)
    int2 = int(hex2, 16)
    result = (int1 + int2) % 16

    return hex(result)[2:] # Don't need those leading values for this


def requestPassword():

    EMOTIONAL_DAMAGE=True # May Steven He levels of shame be upon you the longer this stays True
    while EMOTIONAL_DAMAGE:

        new_password=getpass.getpass('\033[32m>> \033[0m')

        confirm_password=getpass.getpass('\033[32mConfirm >> \033[0m')
        count_errors=0
        while new_password!=confirm_password:
            
            count_errors+=1
            if count_errors>=2: # Bro failed twice on confirm, so likely mistyped the initial password and needs the process restarted
                print("\n ! Well, someone failed their typing classes from the 2000s in the 4th grade. You'll be prompted to enter in the password all over again now.\n")
                break
            
            print(" ! \033[31mPasswords do not match. Try again.\033[0m")
            confirm_password=getpass.getpass('\033[32mConfirm >> \033[0m')
        
        if new_password==confirm_password:
            print('\n + Passwords match.\n')
            EMOTIONAL_DAMAGE=False # Well thank goodness

    if len(new_password)<=8: # NIST folks. Cmon
        print("\n + Bruh, like you do you and all, but why are you choosing such a short password.\n")
    
    return new_password,confirm_password


# This is used to encrypt a new csv file or re-encrypt the contents of a modified KEF wallet
def encryptFileFunction(file_path,text_to_encode_in_a_list,generate_hash_stuff,entered_password,logMod): #cleartext password,logMod at the end

    if len(text_to_encode_in_a_list)>=16383: # Too long to encode. A password file should never get close to exceeding this value, so quitting the function/program entirely
        print(' ! \033[31mYou are trying to encode more characters than the algorthim is designed to handle (~16,000 or 128^2).\033[0m The current total is: '+str(len(text_to_encode_in_a_list))+'. You must condense the contents of the file before trying again. The program will quit now.')
        time.sleep(10)
        sys.exit()

    if newFile is True:
        newLogMod='0'

        print("\n + Since this is a new file you will now be prompted to enter in a password to encrypt the contents, don't forget it.\n")
        entered_password,confirm_password=requestPassword()
        time.sleep(1)
        print("\n ! \033[31mOnce you confirm the encrypted file was created correctly, don't forget to delete the cleartext csv file.\033[0m\n")
        time.sleep(2)
    else:
        newLogMod=str(int(logMod)+1)
        confirm_password=str(entered_password)
        

    # Using a target hex goal, generate two values that will 'combine' to it
    def random_hex_pair(goal_hex):
        goal = int(goal_hex, 16)

        first = random.randint(0, 15)
        second = (goal - first) % 16

        first_hex = hex(first)[2:]
        second_hex = hex(second)[2:]

        return first_hex, second_hex
    
    
    # See the function comments for what this does
    sha512_hash,sha512_hash_reverse,hash_array_128x128,hash_array_as_one_string=generate_hash_stuff(confirm_password,newLogMod) # newLogMod uses '0' for a new file or increases value by '1' for normal saves

    # Create a large, encoded 16 row array
    full_array_to_save_to_text_file=[]

    for i in range(len(text_to_encode_in_a_list)):
        char=text_to_encode_in_a_list[i]

        # Initial check to make sure it is an ascii char
        if ord(char) <= 0x7F:

            # Brief note - after added this if/else any odd formatting should be caught by the else. The try's and other if's are redundant now

            try: # Ensure the char is able to be encoded
                char_as_hex=f'{ord(char):02x}' # Encodes each ascii char into its hex equivalent
            except:
                print(" ! \033[31mThe character \033[0m"+str(char)+"\033[31m was unable to be encoded into an acceptable hex value (Err1).\033[0m The rest of the program will proceed with the character replaced by a \033[34m?\033[0m.")
                char_as_hex=f'{ord("?"):02x}'
            
            # In some cases loads rare characters outside the normal scope of expected hex values, need to account for this here like above exception
            if len(char_as_hex)>2:
                print(" ! \033[31mThe character \033[0m"+str(char)+"\033[31m was unable to be encoded into an acceptable hex value (Err2).\033[0m The rest of the program will proceed with the character replaced by a \033[34m?\033[0m.")
                char_as_hex=f'{ord("?"):02x}'

        else: # Not an ascii char, not encodable with my algortihm
            print(" ! \033[31mThe character \033[0m"+str(char)+"\033[31m is not an encodable ascii character in hex.\033[0m The rest of the program will proceed with the character replaced by a \033[34m?\033[0m.")
            char_as_hex=f'{ord("?"):02x}'


        # Create a random 16x16 array w/ hex chars
        useList=[str(q) for q in range(10)]+['a','b','c','d','e','f']
        new_16x16_array=[[random.choice(useList) for m in range(16)] for l in range(16)]

        # Okay, using a hash of the password and its indexed location a unique hash is create for each array
        # From that unique hash, locations are generated (this works because the individual arrays are limited to 16x16 in size)
        # Locations 1 and 2 encode the (manipulated) value of the first character of the ascii char encoded into hex
        # Locations 3 and 4 encode the same, but for the second character of the ascii char encoded into hex
        # Eventually, 1+2 are merged and unconfigured and then added to the same for 3+4
        # At the very end the character is converted back to ascii from the two character length hex key
        location1,location2,location3,location4=get_locations_within_an_array(sha512_hash,hash_array_as_one_string,i)

        first_hex,second_hex=random_hex_pair(str(char_as_hex[0]))
        third_hex,fourth_hex=random_hex_pair(str(char_as_hex[1]))

        # The data is encoded into each array using the locations and the values of the hex parts
        new_16x16_array[int(location1[1],16)][int(location1[0],16)]=str(first_hex)
        new_16x16_array[int(location2[1],16)][int(location2[0],16)]=str(second_hex)
        
        new_16x16_array[int(location3[1],16)][int(location3[0],16)]=str(third_hex)
        new_16x16_array[int(location4[1],16)][int(location4[0],16)]=str(fourth_hex)

        full_array_to_save_to_text_file.append(new_16x16_array)
        




    # Final manipulations to the data before saving to a KEF wallet
    all_16_lines=[]
    for z in range(16):
        current_line=''

        for array in full_array_to_save_to_text_file:
            current_line+=''.join(array[z])
        
        # Long story short, each of the 16 lines are shifted a fixed number of characters using the original sha512 hash
        resorting_hash=hashlib.sha512(str(str(z)+str(sha512_hash)).encode()).hexdigest()
        resorting_num=sum(int(resorting_hash[i], 16) for i in range(4))

        current_line=current_line[resorting_num:] + current_line[:resorting_num]
        
        if z!=15: # Avoid adding a blank line to the last element of the list. Messes with reading the file later on
            current_line+='\n'
        all_16_lines.append(current_line)


    kef_filepath=str(file_path)[:-4]+'.kef' # Just replace .csv with .kef now, the other checks have gone away

    # This is the xml-looking format the KEF wallet saves to
    root = ET.Element("kef")
    attr = ET.SubElement(root, "attr")
    ET.SubElement(attr, "fileType").text="Kent Encrypted File"
    ET.SubElement(attr, "description").text="The Kent Encrypted File is created and manipulated under the Kent Encryption Standard for use as a password wallet"
    ET.SubElement(attr, "author").text="Wesley Kent"
    ET.SubElement(attr, "version").text=str(version)
    ET.SubElement(attr, "revision").text=str(revision)
    ET.SubElement(attr, "link").text="https://wesleykent.com"
    ET.SubElement(attr, "github").text="https://github.com/fe-moldark"
    ET.SubElement(attr, "lastUpdated").text=str(datetime.now().strftime("%m/%d/%Y"))
    ET.SubElement(attr, "logMod").text=str(newLogMod) # This value is now extremely important
    data = ET.SubElement(root, "data")
    ET.SubElement(data, "encryptedData").text=''.join(all_16_lines)

    rough_string = ET.tostring(root, encoding="utf-8")
    parsed = xml.dom.minidom.parseString(rough_string)
    pretty_xml = parsed.documentElement.toprettyxml(indent="  ")  # Indent w/ two spaces
    with open(kef_filepath, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f" + \033[32mFile saved!\033[0m If you chose option \033[34m{one}\033[0m at the beginning the program will close out now.\n")
    time.sleep(8)
    #sys.exit() # Only make this happen when encrypting a brand new csv, not when saving changes in the loop for an existing (and opened) KEF wallet


# Choice '1' is to encrypt a new file
if program_choice=='1':
    
    newFile=True

    scroll=['\n + The file to be encrypted MUST be formatted as a .csv file with \033[34m;\033[0m as the field delimiter, and exactly 6 columns.',' + Files with more than ~16,000 (128^2) characters will not work.',' + You will select the file in the next screen.\n']
    for line in scroll:
        time.sleep(0.5)
        print(line)
    time.sleep(1)

    
    # Initialize Tkinter (w/out opening a full window)
    root = tk.Tk()
    root.withdraw()

    # Open file dialog
    file_path = filedialog.askopenfilename(title="Select the csv file now")

    # The os.path.exists check is redundant now, but at least confirming the file is in fact a csv
    while (os.path.exists(file_path), file_path[-4:]==".csv")!=(True,True):

        if not os.path.exists(file_path):
            print("\n ! \033[31mFile path does not exist. Try again.\033[0m")
        if file_path[-4:]==".csv":
            print("\n ! \033[31mFile type is not a '.csv'. Try again.\033[0m")

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select the csv file now:")

    # Like the exception explains, I was trying to break this during testing and noticed certain weird characters can make this error out. At least now you know why
    try:
        readOpen=open(file_path,'r')
        readLines=readOpen.read()
        readOpen.close()
    except:
        print(' ! \033[31mError reading the contents of the csv file!\033[0m This likely has to do with unsupported characters. Please review the file, then try again later. Closing out now.')
        time.sleep(8)
        sys.exit()

    text_to_encode_in_a_list=list(readLines)

    encryptFileFunction(file_path,text_to_encode_in_a_list,generate_hash_stuff,None,None)


# Choice '2' is to decrypt a new file
elif program_choice=='2':

    scroll=['\n\033[31m !!! \033[0mNOTE:\033[31m since this is loading the data in an \033[0mUNENCRYPTED\033[31m format, remnants may linger in memory even after the program closes.\033[0m', '\033[31m !!! \033[0mONLY\033[31m run this program from a computer you own and trust.\033[0m\n\n']
    for line in scroll:
        time.sleep(0.5)
        print(line)
    time.sleep(5)

    print(' + The encrypted file \033[34mMUST\033[0m be an established KEF wallet. You will select the file in the next screen.\n')

    # Initialize Tkinter (w/out opening a full window)
    root = tk.Tk()
    root.withdraw()

    # Open file dialog
    file_path = filedialog.askopenfilename(title="Select the KEF wallet now")
    
    while (os.path.exists(file_path),file_path[-4:]==".kef")!=(True,True):

        if not os.path.exists(file_path):
            print("\n ! \033[31mFilepath does not exist.\033[0m Try again.")
        if file_path[-4:]!=".kef":
            print("\n ! \033[31mFile type is not a '.kef'.\033[0m Try again.")
        file_path=input('\n>> ')

        time.sleep(2)

        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title="Select the KEF wallet now")

    print("\n + \033[34mValid file path.\033[0m You will now be prompted to enter in a password to decrypt its contents.\n")
    
    # If the you are working with an older version or the KEF wallet has been corrupted somehow, this'll catch it
    # Otherwise it's just reading the necessary info like the encryptedData and logMod elements
    try:

        tree=ET.parse(file_path)
        root = tree.getroot()

        # Extract attributes
        fileType = root.find("./attr/fileType").text
        description = root.find("./attr/description").text
        author = root.find("./attr/author").text
        version = root.find("./attr/version").text
        revision = root.find("./attr/revision").text
        link = root.find("./attr/link").text
        lastUpdated = root.find("./attr/lastUpdated").text
        logMod = root.find("./attr/logMod").text

        # Extract encrypted data
        encryptedData = root.find("./data/encryptedData").text

        data0=str('      \033[0mLoaded: \033[34m'+str(fileType)+'\033[0m - \033[32mv'+str(version)+'.'+str(revision)+'      ')
        data1=str('\033[0mReference: \033[34m'+str(link))
        data2=str("\033[0mFile last Updated: \033[34m"+str(lastUpdated)+'\033[0m // Mod: \033[34m'+str(logMod))
        data_out=[data0,data1,data2]

        def strip_ansi(s):
            ansi_escape = re.compile(r'\033\[[0-9;]*m')
            return ansi_escape.sub('', s)

        def center_ansi(strings):
            max_length = max(len(strip_ansi(s)) for s in strings)
            centered_strings = []
            
            for s in strings:
                visible_length = len(strip_ansi(s))
                padding = (max_length - visible_length) // 2
                centered_strings.append(' ' * padding + s)
            
            return centered_strings,max_length


        centered_strings,max_length = center_ansi(data_out)

        centered_strings.insert(0,''.join(['\033[36m=' for d in range(max_length)]))
        centered_strings.append(''.join(['\033[36m=' for d in range(max_length)]))
        
        print('\033[0m\n')
        for line in centered_strings:
            print(line)
            time.sleep(0.5)
        time.sleep(1)


    except:

        print(' ! \033[31mError parsing elements from the KEF wallet.\033[0m You are using a wrong KEF version or the file is corrupted. The program will close now.')
        time.sleep(8)
        sys.exit()

    # Basically a successful decryption will have a correctly formatted csv data delimited by five semicolons per row, which are delimited by a '\n'
    # If it does not meet those requirements it'll throw out God knows how many errors, so it'll re-prompt for the password hoping you're just a clumsy typer
    passwordFailing=True
    while passwordFailing:

        entered_password=getpass.getpass('\033[32m\n>> \033[0m')

        readLines_init=encryptedData.split('\n')

        # Check length of each line to ensure proper encoding
        for checkLen in readLines_init:

            # You should never run into these errors, I only made them happen intentionally when troubleshooting how the program handles corrupt/invalid KEF wallets. Feel free to ignore these checks
            if int(len(checkLen))>=int(16 * 16384): # 128^2 possible characters each encoded into individual 16x16 grids
                failureAt=int(readLines_init.index(checkLen))
                print(' ! \033[31mOne or more lines beginning at line: \033[0m'+str(failureAt)+'\033[31m exceed the maximum theoretical length (16 * 128^2) of KEF data.\033[0m The program will exit now.')
                time.sleep(8)
                sys.exit()
            if int(len(checkLen) % 16) != 0: # If not exactly divisible by 16 then the line (file) is malformed
                failureAt=int(readLines_init.index(checkLen))
                print(' ! \033[31mOne or more lines beginning at line: \033[0m'+str(failureAt)+'\033[31m are not precisely divisible by 16.\033[0m The program will exit now.')
                time.sleep(8)
                sys.exit()

            for ind in range(len(checkLen)):
                if str(checkLen[ind]) not in [str(q) for q in range(10)]+['a','b','c','d','e','f']: # Checking if each character in there is in fact hexadecimal
                    print(' ! \033[31mThere are one or more invalid (non-hex) characters beginning on line: \033[0m'+str(readLines_init.index(checkLen))+'\033[31m, index: \033[0m'+str(ind)+'\033[0m. The program will exit now.')
                    time.sleep(8)
                    sys.exit()
        
        # Check maximum row length of 16 - another error you should never see...
        if len(readLines_init)>16:
            print(' ! \033[31mThe exact number of rows in properly encoded KEF data must be 16, no more or less.\033[0m The current amount being read is \033[34m'+str(len(readLines_init))+'\033[0m. The program will exit now.')
            time.sleep(8)
            sys.exit()


        # Uses the same functions to decrypt as the encryption function uses
        sha512_hash,sha512_hash_reverse,hash_array_128x128,hash_array_as_one_string=generate_hash_stuff(str(entered_password),str(logMod))

        try:
            # Reorder readLines_init according to the same function as when encoding the file
            # Takes the first 4 chars of hash and add to 'z', then rehash and take the sum of the first 4 chars of hash
            readLines=[]
            for jj in range(len(readLines_init)):
                resorting_hash=hashlib.sha512(str(str(jj)+str(sha512_hash)).encode()).hexdigest()
                resorting_num=sum(int(resorting_hash[i], 16) for i in range(4))

                working_line=readLines_init[jj]
                
                # Reference the encrypt function, this is just the exact opposite of their last step
                current_line=working_line[-resorting_num:] + working_line[:-resorting_num]
                readLines.append(current_line)


            # Split into unique 16x16 arrays from the splitlines of the file
            split_into_unique_16x16_arrays=[]
            for i in range(int(len(readLines[0])/16)):
                current_array=[]
                for j in range(16):
                    one_row=[readLines[j][(i*16)+k] for k in range(16)] # I totally did not ask chatgpt to do this for me. I swear

                    current_array.append(one_row)
                
                split_into_unique_16x16_arrays.append(current_array)


            # Reference notes of the encoding section, this (not so simply) undoes that whole function
            full_decrypted_string=''
            for q in range(len(split_into_unique_16x16_arrays)):
                work_on_this_array=split_into_unique_16x16_arrays[q]
                location1,location2,location3,location4=get_locations_within_an_array(sha512_hash,hash_array_as_one_string,q)

                hex1_part1=str(work_on_this_array[int(location1[1],16)][int(location1[0],16)])
                hex1_part2=str(work_on_this_array[int(location2[1],16)][int(location2[0],16)])
                hex1=str(combine_hex_values(hex1_part1, hex1_part2))

                hex2_part1=str(work_on_this_array[int(location3[1],16)][int(location3[0],16)])
                hex2_part2=str(work_on_this_array[int(location4[1],16)][int(location4[0],16)])
                hex2=str(combine_hex_values(hex2_part1, hex2_part2))

                text_as_hex=str(hex1)+str(hex2)

                # After modifying the encoding function this check should no longer be necesary, but it's here just in case someone finds a way to break it...
                try:
                    full_decrypted_string+=str(bytes.fromhex(text_as_hex).decode())
                except:
                    full_decrypted_string+='?'


            # Since '\n' has its own hex code that is kept as the line delimiter
            full_decrypted_list=full_decrypted_string.split('\n')
            # Emphasis on the ';' NEEDING to be the field delimiter of the csv file...
            full_decrypted_array=[rw.split(';') for rw in full_decrypted_list]

            # Sometimes includes a blank new line at the end of the csv file, this removes that
            if len(full_decrypted_array[-1])==1:
                full_decrypted_array=full_decrypted_array[:-1]


            print("\n + \033[34mDecryption process looks like it went through okay.\033[0m\n") # Well miracles do happen
            passwordFailing=False
            break
        
        except:
            print("\n\n ! \033[31mAn incorrect password was likely entered.\033[0m You will be prompted to try again shortly if you mistyped it.\n")
            time.sleep(5)
            #sys.exit() # No longer auto-exit, give them a chance to try again

        
    # This can be called later, so keep it in a function for now
    def show_help():
        scroll=["\nYou can use the following keys to view or modify the wallet's contents:",
                '\n   + \033[34msearch\033[0m \033[32m<term>\033[0m     |  Ex. \033[34msearch \033[32mBank\033[0m',
                '   + \033[34mmodify\033[0m \033[32m<row#>\033[0m     |  Ex. \033[34mmodify \033[32m4\033[0m',
                '   + \033[34mdelete\033[0m \033[32m<row#>\033[0m     |  Ex. \033[34mdelete \033[32m17\033[0m',
                '   + \033[34mview all\033[0m          |  View all contents of the file',
                '   + \033[34madd\033[0m               |  This will prompt you to add info for new data',
                '   + \033[34msave\033[0m              |  This will export existing changes to the same KEF wallet',
                '   + \033[34mpasswd\033[0m            |  Prompts you to enter in a new password that will re-encrypt the KEF wallet',
                '   + \033[34mexport csv\033[0m        |  Not recommended, but will export all data in cleartext to a csv file',
                '   + \033[32mhelp\033[0m              |  Shows this menu',
                '   + \033[31mexit\033[0m              |  Quits the program\n']
        for line in scroll:
            time.sleep(0.3)
            print(line)

    show_help()

    # Make output look pretty. I spent too much time trying to sort out something so simple
    def printTabledResults(results):

        col_widths = [max(len(str(item)) for item in col) for col in zip(*results)]
        header = results[0]
        print(" \033[34m|\033[0m ".join(f"\033[36m{str(item):<{col_width}}\033[0m" for item, col_width in zip(header, col_widths)))

        total_width = sum(col_widths) + (3 * (len(col_widths) - 1))  # Total table width, including separators
        print("\033[34m-\033[0m" * total_width)

        for row in results[1:]:
            print(" \033[34m|\033[0m ".join(f"{str(item):<{col_width}}" for item, col_width in zip(row, col_widths)))

    headers=['#','Description', 'Link', 'Username/email', 'Password', 'Other info']

    # I have this customized to alert me whenever a password file with a certain key phrase in one of the columns is opened
    # Once identified, it will try and pull info like the currently logged in user and their public IP, then send me an email
    # So, if want to share this with someone but you want to know when it's accessed, it's a good method. It does require
    # you to configure this encryption before sharing it (and the KEF wallet) according to your identifier and email info
    # I'll leave it comment-blocked out for now, but you can test this for yourself if you want.
    """
    for checkRow in full_decrypted_array:
        for checkCol in checkRow:
            if checkCol=='search_key_here':

                try:

                    to="receiving_email@gmail.com"
                    user="sender_email@gmail.com"

                    try:
                        userID=str(os.getlogin())
                    except:
                        userID='Unable to get username'

                    try:
                        response = requests.get("https://api64.ipify.org?format=text", timeout=5)
                        response.raise_for_status()
                        publicIP=str(response.text)
                    except:
                        publicIP='Could not pull Public IP'

                    message = MIMEMultipart()
                    message['From'] = Header(user)
                    message['To'] = Header(to)
                    message['Subject'] = Header('Password file was successfully opened - User: '+str(userID)+', Public IP: '+str(publicIP))
                    gmail_pass = "api_key"

                    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                    server.login(user, gmail_pass)

                    server.sendmail(user, to, message.as_string())
                    server.quit()
                except:
                    pass
    """


    # This is the main loop used for the searching, exporting, and manipulating of the decrypted data
    while True:

        command=input('>> ')

        # Search through EACH column now, not just the decryption one
        if str(command)[:6]=='search':
            search_term=command[7:]

            results=[headers]
            for list_row in full_decrypted_array:
                for col in list_row:
                    if str(search_term).lower() in str(col).lower():
                        if len(list_row)>1: # Blank check, just in case
                            results.append(list_row)
                            break


            print('\n + \033[34mMatching results:\033[0m\n')
            printTabledResults(results)
            print('\n\n')
        
        # Prints out all of the tabled data in one go
        elif str(command).lower() in ['view all','show all']: # My dumbass kept forgetting which of these I chose, so now we have both
            results=[headers]
            for list_row in full_decrypted_array:
                if len(list_row)>1:
                    results.append(list_row)

            print('\n + \033[34mReturning all results:\033[0m\n')
            time.sleep(1)
            
            printTabledResults(results)
            print('\n\n')

        # Exit the loop
        elif str(command).lower()=='exit':
            print(' + \033[31mExiting now.\033[0m')
            time.sleep(2)
            break
        
        # Remove a record
        elif str(command)[:6]=='delete':
            search_term=command[7:]

            try:
                delete_index=int(search_term)
                reorder=[]

                if delete_index+1>len(full_decrypted_array) and delete_index>=0:
                    print('\n ! \033[31mDelete index value outside the scope limit of the array.\033[0m Try again.\n')
                else:

                    full_decrypted_array.pop(delete_index)

                    for d in range(len(full_decrypted_array)):
                        temp_array=full_decrypted_array[d]
                        temp_array[0]=str(d)
                        reorder.append(temp_array)

                    full_decrypted_array=[ele for ele in reorder]

                print(" + \033[34mRow deleted\033[0m. If you wish to save these changes, enter in \033[34msave\033[0m before closing out the program.\n")

            except TypeError:
                print(' ! \033[31mUnable to convert value to integer.\033[0m Try again.\n')

        # Modify a record's column
        elif str(command)[:6]=='modify':
            search_term=command[7:]

            try:
                modify_index=int(search_term)

                if modify_index+1>len(full_decrypted_array) and modify_index>=0:
                    print('\n ! \033[31mModify index value outside the scope limit of the array.\033[0m Try again.\n')
                else:
                    print('\n + You have chosen to edit row \033[34m'+str(search_term)+'\033[0m. The current values of this row are:\n')
                    new_headers=[str(str(headers[r])+' ('+str(r)+')') for r in range(len(headers))]
                    printOutTable=[new_headers,full_decrypted_array[modify_index]]
                    printTabledResults(printOutTable)
                    zero=0 # Fml color formatting
                    one=1
                    print(f"\n + With the left most column starting at \033[34m{zero}\033[0m, enter in the columnn # you wish to edit. For example, entering in \033[34m{one}\033[0m would allow you to edit the \033[34mDescription\033[0m column.\n")

                    editWhatColumn=input('>> ')
                    while editWhatColumn not in [str(s) for s in range(1,6)]:
                        print('\n ! \033[31mInvalid number entered.\033[0m Only numbers \033[34m1-5\033[0m are currently accepted. Try again.\n')
                        editWhatColumn=input('>> ')
                    editWhatColumn=int(editWhatColumn)

                    print("\n + All ascii characters excluding \033[34m;\033[0m are accepted. Enter in the new data for the column you selected now:\n")
                    newColumnData=input('>> ')
                    sanitized_input="".join(char for char in newColumnData if char.isascii())
                    sanitized_input="".join(char for char in sanitized_input if str(char)!=";")

                    newDataList=full_decrypted_array[modify_index]

                    newDataList.pop(editWhatColumn)
                    newDataList.insert(editWhatColumn, str(str(sanitized_input)))

                    full_decrypted_array.pop(modify_index)
                    full_decrypted_array.insert(modify_index, newDataList)
                    
                    print("\n + \033[34mRow updated.\033[0m If you wish to save these changes, enter in \033[34msave\033[0m before closing out the program.\n")

            except TypeError:
                print('\n ! \033[31mUnable to convert value to integer.\033[0m Try again.\n')
            
        # Add a record
        elif str(command).lower()=='add':
            temp_headers=headers[1:]
            print("\n + You will now be prompted to enter in each column's info for the new row. All ascii characters excluding \033[34m;\033[0m are accepted.\n")
            new_row_data=[str(len(full_decrypted_array))]
            for item in temp_headers:
                toAdd=input(" >> Enter in '"+str(item)+"': ")
                new_row_data.append(str(toAdd))

            full_decrypted_array.append(new_row_data)
            
            print("\n + \033[34mRow added.\033[0m If you wish to save these changes, enter in \033[34msave\033[0m before closing out the program.\n")

        # Export loaded file into a cleartext csv file
        elif str(command).lower()=='export csv':

            new_filepath=file_path[:-4]+'_clear.csv' # So .kef >> _cleartext.csv in the same directory

            with open(new_filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=";")
                writer.writerows(full_decrypted_array)

            print(' + \033[34mFile saved to: \033[0m"'+str(new_filepath)+'"\n')

        # Export as a re-encrypted file, uses existing password by default
        elif str(command).lower()=='save': # Formerly 'export kef'

            print('\n + \033[34mSaving changes to the existing KEF wallet.\033[0m\n')

            # Use just file_path now
            new_filepath=str(file_path)

            text_to_encode_in_a_list=[]
            for listed in full_decrypted_array:
                for i in range(len(listed)):
                    for char in listed[i]:
                        text_to_encode_in_a_list.append(str(char))

                    if i!=len(listed)-1:
                        text_to_encode_in_a_list.append(';')
                    else:
                        text_to_encode_in_a_list.append('\n')
            
            text_to_encode_in_a_list.pop(-1) # Remove the last '\n'

            encryptFileFunction(new_filepath,text_to_encode_in_a_list,generate_hash_stuff,entered_password,logMod)

        # Change the password used to encrypt the wallet
        elif str(command).lower()=='passwd': # logMod counter will still go up during the save, that is NOT reset alongside the password
            print('\n + You have chosen to select a new password to encrpyt the wallet with. Note that the password will only be applied once \033[34msave\033[0m has been entered. Enter in your new password now:')
            entered_password,confirm_password=requestPassword()

        # Display the 'help' menu of options
        elif str(command).lower()=='help':
            show_help()

        # How'd you mess this part up?
        else:
            print('\n ! \033[31mNot a valid option.\033[0m\n')
            show_help()


# At the very least overwrite these variables to try and prevent memory-based attacks...
password=hashlib.sha512("something_to_overwrite".encode()).hexdigest()
new_password=hashlib.sha512("something_to_overwrite".encode()).hexdigest()
confirm_password=hashlib.sha512("something_to_overwrite".encode()).hexdigest()
entered_password=hashlib.sha512("something_to_overwrite".encode()).hexdigest()
sha512_hash=hashlib.sha512("something_to_overwrite".encode()).hexdigest()
sha512_hash_reverse=hashlib.sha512("something_to_overwrite".encode()).hexdigest()
results=[str(hashlib.sha512("something_to_overwrite".encode()).hexdigest()) for j in range(1000)]
full_decrypted_array=[str(hashlib.sha512("something_to_overwrite".encode()).hexdigest()) for j in range(1000)]


sys.exit()
