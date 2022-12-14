from mpmath import mp
from PIL import Image
import numpy
import math, os
import string
import random
from random import randint
import sys, time
from numpy import asarray

#reference encrypt file for notes on these variables
test1,alphaDict=str(string.printable),[]

mp.dps = 150
pi = str(mp.pi)
pi=str(pi.replace(".",""))

for ss in test1[:-5]:
    if ss!="%":
        alphaDict.append(ss)
alphaDict.append("%") #this was causing strange problems, but this works

text1=alphaDict


text=""
for element in alphaDict:
    text+=str(element)

list1=[char for char in text] 
numpy.random.shuffle(list1)
text=""
text="".join(list1)


#short key is the actual key
def giveMeShortKey(randomKey,text):
    myAnswerKey=""

    keepCount=-1
    for numberI in range(len(pi)): #wont ever get past the 150 digit limit put in place
        number=pi[numberI]
        if numberI<=len(text)-1:
            keepCount+=int(number)+1

            try:
                myAnswerKey+=str(randomKey[keepCount])
            except IndexError:
                myAnswerKey+=random.choice(list1)
                
    return myAnswerKey


#just keep this at 16 and dont ask questions
ratio=16


#begin
while True:
    false=True#hate on this all you want, I still think it's funny
    choices=""

    while false is True:
        print "> Enter path to image for decryption.\n    > Image must be in JPEG format.\n    > Enter 'exit' to quit program."
        choices=raw_input("\n> Input : ")
        

        if os.path.exists(str(choices)) and choices[-4:]=='.jpg':
            false=False
            fileAt=str(choices)
        elif choices in ["exit",'Exit']:
            sys.exit()
        else:
            false=True

    print "\n> Enter the randomized key to the image."
    answerKey=raw_input("> Input : ")
    print "> Using the above key, text translates as follows: \n"


    #breaks down the long key to short one we can use later
    #I also don;t think this has proper error handling, so just get it right the first time
    answerKey2=giveMeShortKey(answerKey,text)

    newImage=Image.open(str(choices))
    newData = asarray(newImage) #open as array

    checkArray=[]

    #IMPORTANT - for some reason list will sometimes return ONE value that is ONE rgb value higher in the list of 16 pixels
    #e.g. a list of 15 "42"s and one "43" at the end - no clue why
    #below function will select the most common number from the list (i.e. the one that appears ~15 / 16 times)
    def give_most_common_num(list_numbers):
        dict1={}
        max_freq_so_far=0
        most_common_number=None 
        for number in list_numbers:
            dict1[number] = dict1.get(number,0)+1
            if dict1[number] >= max_freq_so_far:
                max_freq_so_far = dict1[number]
                most_common_number=number
        
        return most_common_number
            
        
            
    all_rows1=[]
    for y in range((len(newData)/(ratio))-1):#the -1 is now for the red line at the bottom, no need to to look at it
        checkLine=[]
        temp_row1=[]
        
        for x in range(len(newData[0])/(ratio)):

            
            averageFifteen,averageSixteen=(0,0)
            for i in range(4):
                for j in range(4):
                    averageFifteen+=int(newData[y*ratio+i+12][x*ratio+j+8][0])
            averageFifteen=int(math.ceil(float(averageFifteen)/float(16)))
                    
            for i in range(4):
                for j in range(4):
                    averageSixteen+=int(newData[y*ratio+i+12][x*ratio+j+12][0])
            averageSixteen=int(math.ceil(float(averageSixteen)/float(16)))


            use1=(averageFifteen-50)/40 #so stupid, but the values switch x,y positions when being saved and everything is already built around that
            use2=(averageSixteen-50)/40 #this caused around 45min of headaches, so I'm keeping this note here



            #addF1/2/3 is new method for calculation - avoids false RGB readings or from writing - unclear which but this method solved it
            #use of 'average' is old method, but keep around just in case
            #average=0
            addF1=[]
            for i in range(4):
                for j in range(4):
                    #average+=int(newData[y*ratio+i+(use2*4)][x*ratio+j+(use1*4)][0])
                    addF1.append(int(newData[y*ratio+i+(use2*4)][x*ratio+j+(use1*4)][0]))
            #averageF=int(math.ceil(float(average)/float(16)))
            averageF=give_most_common_num(addF1)

            #this function returns the next row available (if not, back to 0), and the remaining slots columns-wise (which, again, is actually rows because fml)
            def get_spots(use1,use2):#use1=x,use2=y
                #so we know these two are actually switched
                #use1 is for the x, and use2 for y
                if use2+1>2:
                    new_row=0
                else:
                    new_row=use2+1

                given=[0,1,2]
                given.pop(use1)#can pop by index ONLY once
                new_columns=given[:]

                return new_row,new_columns
            
            new_row,new_columns=get_spots(use1,use2)

            addF2=[]
            #averagePart1=0
            for i in range(4):
                for j in range(4):
                    #averagePart1+=int(newData[y*ratio+i+(new_row*4)][x*ratio+j+(new_columns[0]*4)][0])
                    addF2.append(int(newData[y*ratio+i+(new_row*4)][x*ratio+j+(new_columns[0]*4)][0]))
            #averageF_Part1=int(math.ceil(float(averagePart1)/float(16)))
            averagePart1=give_most_common_num(addF2)

            addF3=[]
            #averagePart2=0
            for i in range(4):
                for j in range(4):
                    #averagePart2+=int(newData[y*ratio+i+(new_row*4)][x*ratio+j+(new_columns[1]*4)][0])
                    addF3.append(int(newData[y*ratio+i+(new_row*4)][x*ratio+j+(new_columns[1]*4)][0]))
            #averageF_Part2=int(math.ceil(float(averagePart2)/float(16)))
            averagePart2=give_most_common_num(addF3)


            #reduce the main spot holding the RGB value by the combined other two values that house information
            averageF2=averageF+(averagePart1-averagePart2)

            checkLine.append(averageF2)

        checkArray.append(checkLine)
        all_rows1.append(temp_row1)




    FINAL=[] #will house decoded message by line
    savekey=[]
    for line in checkArray:
        FINAL_line=""
        savekeyline=[]

        for char in line:

            key=((int(char)-44)/2)#was 10, now 44 - can ignore


            #adjust
            if key<0:
                break
            else:
                try:
                    savekeyline.append(int(key))
                
                    finalDecrypted=str(answerKey2[key])

                    FINAL_line+=str(finalDecrypted)
                except IndexError:
                    pass

        FINAL.append(FINAL_line)
        savekey.append(savekeyline)

    
    print "\n+BEGIN++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    time.sleep(1)
    for line in FINAL:
        print line
        time.sleep(0.1)
    print "\n+END++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"

    askThem="" #offering to save results - generally not recommended since this will store the now unencrypted data in clear text
    print '\n\n> Do you wish to save the decryption to a new text file (y / n) ?'

    
    while askThem not in ['(y)','y','Y','(Y)','(n)','n','N','(N)']:    
        askThem=raw_input('> Input : ')

    if askThem in ['(n)','n','N','(N)']:
        pass#so useless
    elif askThem in ['(y)','y','Y','(Y)']:

        desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
        print "\n=================================================\n> Text file will save to the Desktop for this user\n> Enter the name you wish to save the file as below.\n    > Do not include punctuation or file formats.\n    > Will automatically save as a .txt, or as a basic text file format.\n    > Do not include spaces in name."

        choosePath=""
        testThis=False
        while testThis is False: #ie waiting on valid path name for saving
            
            choosePath=raw_input("\n> Enter desired file name : ")
            this="".join(x for x in choosePath if x.isalnum())

            if os.path.exists(desktopPath+"\\"+this+'.txt') is True:
                testThis=False
                print ">>> File name already taken. <<<\n\n"
            else:
                
                print ">>> Valid name for desktop. Saving now. <<<\n\n"

                NewFile=open(desktopPath+"\\"+this+'.txt','w')
                for ii in range(len(FINAL)):
                    _line_adj=str(FINAL[ii])
                    
                    if ii+1==len(FINAL):
                        pass
                    else:
                        _line_adj+='\n'
                    
                    NewFile.write(_line_adj)
                testThis=True #break loop and exit
                    
                NewFile.close()
        

sys.exit()







