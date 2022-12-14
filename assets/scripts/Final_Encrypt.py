from mpmath import mp
from PIL import Image
import numpy
import math, os
import string
import random
from random import randint
import sys

#contains all characters that will be use for 
test1,alphaDict=str(string.printable),[]


#limiting the calculation of pi to only 150 digits
mp.dps = 150
pi = str(mp.pi)
pi=str(pi.replace(".",""))#only need the numbers


#check function to convert long key back to short key
def giveMeShortKey(randomKey,text):
    myAnswerKey=""

    keepCount=-1
    for numberI in range(len(pi)):
        number=pi[numberI]
        if numberI<=len(text)-1:
            keepCount+=int(number)+1

            myAnswerKey+=str(randomKey[keepCount])

    #print len(myAnswerKey),myAnswerKey
    #print len(randomKey),randomKey
    return myAnswerKey


#ie the long key to be stored
def giveMeNewKey():

    #this is all kind of a mess where I redefine variables from before but it works so just leave it
    test1,alphaDict=str(string.printable),[]

    for char in test1[:-5]:
        if char!="%":#for some stupid reason this gave me issues, don't ask why
            alphaDict.append(char)
    alphaDict.append("%")

    text1=alphaDict
    text=""

    for element in text1:
        text+=str(element)

    list1=[char for char in text] 
    numpy.random.shuffle(list1)
    text="".join(list1)
        
    mp.dps = 150
    pi = str(mp.pi)
    pi=str(pi.replace(".",""))#only after the numbers

    randomKey=''

    #reference the webpage for an depth explanation of what is happening here
    for i in range(0,len(text)):
            
        piNumber=int(pi[i])
        firstPart=""
        for j in range(piNumber):
            firstPart+=text[randint(1,len(text)-1)]

        adding=firstPart+text[i]
        randomKey+=adding

    print "New Key: ",randomKey,"\n"
        
    return randomKey,text



def encryptFile(enterDirectory,listToEncrypt):
    desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    print "\n=================================================\n> Encrypted image will save to the Desktop for current user\n> Enter the name you wish to save the file as below.\n    > Do not include punctuation or file formats.\n    > Will automatically save as a .jpg, or in JPEG format.\n    > Do not include spaces in name."

    choosePath=""
    testThis=False
    while testThis is False:
        
        choosePath=raw_input("\n> Enter desired file name : ")
        this="".join(x for x in choosePath if x.isalnum())
        #print "check::",str(desktopPath+"/"+this)
        if os.path.exists(desktopPath+"\\"+this+'.jpg') is True:
            testThis=False
            print ">>> File name already taken. <<<"
        else:
            testThis=True
            print ">>> Valid name for the Desktop. Encrypting now. <<<"
            

    #GENERATE NEW RANDOMKEY
    randomKey,text=giveMeNewKey()#long
    myAnswerKey=giveMeShortKey(randomKey,text)#short - used for a check

    #convert to numbered (indexed)
    numberedText=[]
    for line in listToEncrypt:
        adjustLine=[]
        for char in line:
            try:
                #print myAnswerKey.index(char)
                adjustLine.append(myAnswerKey.index(char))
            except ValueError:
                pass

        numberedText.append(adjustLine)

    
    #get max width and height
    maxWidth=0
    maxHeight=len(numberedText)+1#adding the plus one for the red row

    #get us the longest width
    for Line in numberedText:
        if len(Line)>maxWidth:
            maxWidth=len(Line)

    #just because, don't question me
    maxWidth+=8

    #generate data
    ratio=16
    data = numpy.zeros((maxHeight*ratio, maxWidth*ratio, 3), dtype=numpy.uint8)

    all_rows1=[]

    for y in range(maxHeight):

        temp_row1=[]
        for x in range(maxWidth):

            try:
                test=numberedText[y][x]
                num=(numberedText[y][x]*2)+44 #was 10 formerly (not 44), keep for now
            except IndexError:
                num=0

            #There is a better way to do this, but I broke it down so it makes more sense visually
            #From the 16 blocks, they are broken down by "numx" for 1-4, 5-8, 9-12, 13-16

            #line1
            num1=randint(15,230)   
            num2=randint(15,230)
            num3=randint(15,230)
            num4=50+(randint(0,2)*40) #values can be 50, 90, 130

            #line2
            num5=randint(15,230)
            num6=randint(15,230)
            num7=randint(15,230)
            num8=50+(randint(0,2)*40)

            #line3
            num9=randint(15,230)
            num10=randint(15,230)
            num11=randint(15,230)
            num12_adj=50+(randint(0,2)*40)

            #line4
            num13=50+(randint(0,2)*40)
            num14=50+(randint(0,2)*40)
            
            use1=randint(0,2)
            use2=randint(0,2)
            ONE=(use1*40)
            TWO=(use2*40)

            num15_adj=50+ONE
            num16_adj=50+TWO
            

            #save as above, there is a much cleaner way to do this but for visual's sake it easier to track this way
            #don't forget the ratio is 16, although it was different a while back
            #this will break the each block in the 4x4 grid into it's own 4x4 pixel block (same RGB across the 4x4 pixel block, however)

            #line1
            data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio):(x*ratio)+(ratio/4)]=[num1,num1,num1]#topleft
            data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[num2,num2,num2]
            data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[num3,num3,num3]
            data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[num4,num4,num4]
            #line2
            data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio):(x*ratio)+(ratio/4)]=[num5,num5,num5]#left
            data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[num6,num6,num6]
            data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[num7,num7,num7]
            data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[num8,num8,num8]

            #line3
            data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio):(x*ratio)+(ratio/4)]=[num9,num9,num9]#left
            data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[num10,num10,num10]
            data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[num11,num11,num11]
            data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[num12_adj,num12_adj,num12_adj]

            #line4
            data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio):(x*ratio)+(ratio/4)]=[num13,num13,num13]#bottomleft
            data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[num14,num14,num14]
            data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[num15_adj,num15_adj,num15_adj]
            data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[num16_adj,num16_adj,num16_adj]

            
            #now to adjust to other spots to avoid frequency analysis
            def get_spots(use1,use2):#use1=x,use2=y --> this whole thing is backwards, but it works so just leave it
                if use1+1>2:
                    new_row=0
                else:
                    new_row=use1+1

                given=[0,1,2]
                given.pop(use2) #only works once this way
                new_columns=given[:]

                return new_row,new_columns
            
            new_row,new_columns=get_spots(use2,use1)
            
            #choose difference that will exist between these new two squares
            choose_apart=random.choice([i for i in range(9,40) if i%2==0])#gives even #s, 10-40
            choose_difference=random.choice([i for i in range(4,choose_apart-3)])#choose the difference that will split the above number
            
            doesntmatterthenumber=randint(55,190)#number to manipulate

            for i in range(len(new_columns)):
                new_col=new_columns[i]
                if i==0:#first item
                    new_col_one_rgb=doesntmatterthenumber+choose_difference
                else:#second item, nothing else
                    new_col_two_rgb=doesntmatterthenumber-(choose_apart-choose_difference)
                    
            #print 'rgb values at two spots: ',new_col_one_rgb,new_col_two_rgb

            #reformat those two points now on the same data block we were just working on
            data[(y*(ratio))+(4*(new_row)):(y*(ratio))+(4*(new_row+1)), (x*ratio)+(4*(new_columns[0])):(x*ratio)+(4*(new_columns[0]+1))]=[new_col_one_rgb,new_col_one_rgb,new_col_one_rgb]
            data[(y*(ratio))+(4*(new_row)):(y*(ratio))+(4*(new_row+1)), (x*ratio)+(4*(new_columns[1])):(x*ratio)+(4*(new_columns[1]+1))]=[new_col_two_rgb,new_col_two_rgb,new_col_two_rgb]

            #print '##',new_col_one_rgb,new_col_two_rgb,new_num
            #the main grid square here

            #confusing, but this has to do with how the end is identified when being decrypted and how I later changed things needing this add-on check
            #if you have a soul, just let it be
            if num==0:
                new_num=0
            else:
                new_num=num-choose_apart

            #the 'main' block that has been manipulated now, and is ready to be encoded
            data[(y*(ratio))+(4*(use2)):(y*(ratio))+(4*(use2+1)), (x*ratio)+(4*(use1)):(x*ratio)+(4*(use1+1))]=[new_num,new_num,new_num]


            #distraction red squares, random
            def decieve(use2,new_row):#dont forget use1 and the rows are actually the x, not y
                given=[0,1,2]
                
                given.pop(given.index(use2))
                given.pop(given.index(new_row))

                decieve1=given[0]#should only be one remaining value

                decieve2=randint(0,2)

                return decieve1,decieve2
                
            decieve1,decieve2=decieve(use2,new_row)
            #print 'by some miracle we've made it this far'

            #decieve with single red square, divisible by 9 to create a false pattern
            data[(y*(ratio))+(4*(decieve1)):(y*(ratio))+(4*(decieve1+1)), (x*ratio)+(4*(decieve2)):(x*ratio)+(4*(decieve2+1))]=[(randint(0,8)*24)+20,0,0]
            temp_row1.append((new_num,new_col_one_rgb,new_col_two_rgb))


        all_rows1.append(temp_row1)


    #add a single red bar at the bottom to confuse people trying to identify markers, patterns, etc.
    def random_red_odd_rgb():
        rando_red=[]
        for i in range(8):
            rando_red.append(random.choice([i for i in range(55,255) if i%2!=0]))#only odd numbers between 55-255
        return rando_red
    def random_red_even_rgb():
        rando_red=[]
        for i in range(8):
            rando_red.append(random.choice([i for i in range(55,255) if i%2==0]))#only even numbers between 55-255
        return rando_red
    
    for x in range(maxWidth):
        y=maxHeight-1 #single line to write to on the array

        #again, adding in some kind of pattern for people to try and find
        _1,_3,_5,_7,_9,_11,_13,_15=random_red_odd_rgb()
        _2,_4,_6,_8,_10,_12,_14,_16=random_red_even_rgb()
        
    
        #same as above, only difference is these are all some variation of red on the RGB scale
        data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio):(x*ratio)+(ratio/4)]=[_1,0,0]
        data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[_2,0,0]
        data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[_3,0,0]
        data[(y*(ratio)):(y*(ratio))+(ratio/4), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[_4,0,0]

        data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio):(x*ratio)+(ratio/4)]=[_5,0,0]
        data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[_6,0,0]
        data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[_7,0,0]
        data[(y*(ratio))+(ratio/4):(y*(ratio))+(ratio/2), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[_8,0,0]

        data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio):(x*ratio)+(ratio/4)]=[_9,0,0]
        data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[_10,0,0]
        data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[_11,0,0]
        data[(y*ratio)+(ratio/2):(y*ratio)+int(float(ratio)/float((float(4)/3))), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[_12,0,0]

        data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio):(x*ratio)+(ratio/4)]=[_13,0,0]
        data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio)+(ratio/4):(x*ratio)+(ratio/2)]=[_14,0,0]
        data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio)+(ratio/2):(x*ratio)+int(float(ratio)/float((float(4)/3)))]=[_15,0,0]
        data[(y*ratio)+int(float(ratio)/float((float(4)/3))):(y*ratio)+(ratio), (x*ratio)+int(float(ratio)/float((float(4)/3))):(x*ratio)+(ratio)]=[_16,0,0]



            
    img = Image.fromarray(data, 'RGB')
    adj_img=img #below will save the rgb array into a jpeg file, important is no compression (ironic for jpeg, I know)
    adj_img.save(desktopPath+"\\"+this+'.jpg', format='JPEG', subsampling=0, quality=100)

    #this is where we open the file to 'append' and tack on the long key to the bottom of it
    please=open(desktopPath+"\\"+this+'.jpg','a')
    please.writelines(['\n'+str(randomKey)])
    please.close()


def readFile(enterDirectory):
    testTxt=open(enterDirectory,"r").readlines()
    testTxt2=[]
    for line in testTxt:
        #print line[-1:]
        if line[-1:]=="\n":#I hate you
            testTxt2.append(line[:-1])
        else:
            testTxt2.append(line)

    return testTxt2
                                          

while True:
    options1=["1","2","(1)","(2)","exit","Exit","one","two","One","Two"]
    choices=""
    while choices not in options1:
        choices=raw_input("=================================================\n> (1) Encrypt text file\n> (2) Manually enter text\n> Or enter 'exit' to exit program\n=================================================\nInput: ")
        if choices not in options1:
            print "\n--> Invalid input, reference above and try again.\n"

    if choices in ["exit","Exit"]:
        sys.exit()
    
    elif choices in ["1","(1)","one","One"]:
        enterDirectory="random"
        while (os.path.exists(enterDirectory),enterDirectory[-4:])!=(True,".txt"): #waiting on valid path and txt format
            enterDirectory=raw_input("=================================================\n> Enter full path to file to be encrypted below <\n=================================================\nInput: ")

            if os.path.exists(enterDirectory)==False and enterDirectory[-4:]!=".txt":
                print "Named file does not exist and entered name is not a compatible text file. Try again."
            elif os.path.exists(enterDirectory)!=True:
                print "Named file does not exist at that location. Try again."
            elif enterDirectory[-4:]!=".txt": #obsolete now? I think
                print "Entered name is not a compatible text file. Try again."

        confirm=""
        while confirm not in ["Y","y","(y)","N","n","(n)"]:
            confirm=raw_input("> Are sure you wish to encrypt >>>"+enterDirectory+"<<< (y / n) ?\nInput: ")

            if confirm in ["N","n","(n)"]:
                break
            elif confirm in ["Y","y","(y)"]:

                #open file and read into list
                theList=readFile(enterDirectory)

                
                encryptFile(enterDirectory,theList)
            else:
                print "\n--> Invalid input, reference above and try again.\n"


    elif choices in ["2","(2)","two","Two"]:
        print "\n> Enter text line by line, press enter to start new line.\n    > Enter 'done' when ready to save.\n    > Cannot edit already entered lines."

        saveLines=[]

        
        entering=""
        while entering not in ["done","Done","(done)","(Done)"]:
            entering=raw_input("\n> Input: ")


            if entering not in ["done","Done","(done)","(Done)"]:
                saveLines.append(str(entering))

        encryptFile("",saveLines)






                
