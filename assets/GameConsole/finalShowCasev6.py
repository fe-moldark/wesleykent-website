# This creates a simple pygame window to ensure all of the buttons are mapped out correctly and the analog joystick is reading as expected, and has an audio test built-in as well
# Hardware pertinent to this script includes a RPi Model 4 board, an Analog joystick with the MCP3008 analog to digital converter, and a USB gamepad
#
# Author: Wesley Kent
# Created: 06/17/2023
#
# https://github.com/fe-moldark/wesleykent-website/tree/gh-pages/assets/GameConsole
#
# Instructions: Just press the buttons and troubleshoot from there. To test the audio press down on the analog joystick's button for some insight from Maul


import time, sys, os
import pygame
from pygame.locals import *
import spidev



#troubleshooting
#print(os.path.abspath(pygame.__file__))
#print(os.path.realpath(sys.executable)
#sys.exit()


mod=55
adj=135
width, height = (540,360)


joyButtons=[
    ["UP",(int(width/2)-adj,int(height/2)-mod),7,False,30],
    ["LEFT",(int(width/2)-mod-adj,int(height/2)),7,False,30],
    ["RIGHT",(int(width/2)+mod-adj,int(height/2)),7,False,30],
    ["DOWN",(int(width/2)-adj,int(height/2)+mod),7,False,30],
    
    ["A",(int(width/2)+adj,int(height/2)-mod),0,False,30],
    ["B",(int(width/2)-mod+adj,int(height/2)),3,False,30],
    ["X",(int(width/2)+mod+adj,int(height/2)),1,False,30],
    ["Y",(int(width/2)+adj,int(height/2)+mod),2,False,30],
    ["START",(int(width/2)-55,315),8,False,30],
    ["SELECT",(int(width/2)+55,315),9,False,30],
    ["L SHOULDER",(65,40),4,False,30],
    ["R SHOULDER",(width-65,40),6,False,30]
    ]



pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=4096)
pygame.init()
pygame.mixer.init()


baseForPic='/home/pi/pics/extras/'

MOV01 = pygame.image.load(baseForPic+"finalSelect01.png")
MOV02= pygame.image.load(baseForPic+"finalSelect02.png")
MOV03 = pygame.image.load(baseForPic+"finalSelect03.png")
MOV04 = pygame.image.load(baseForPic+"finalSelect04.png")

MOVING_TRANSPARENCY=MOV01


tilesize = 30
mapwidth = 18
mapheight = 12

movx=mapwidth/2
movy=mapheight/2

count_mov=0



def audioTest():
    pygame.mixer.music.load('/home/pi/Downloads/MAUL.mp3')
    pygame.mixer.music.play(0)



def setup_joysticks():
    joystick_list = []
    for i in range(0, pygame.joystick.get_count()):
        joystick_list.append(pygame.joystick.Joystick(i))
        pygame.joystick.Joystick(i).init()
    return joystick_list

print('Joystick count: ',pygame.joystick.get_count())
joystick_count=pygame.joystick.get_count()

if joystick_count==0:
    print("Error, no Joysticks found. Exiting program now.")
    time.sleep(1.5)
    pygame.quit()
    sys.exit()

else:
    #Only ever gonna be the one joystick
    joystick = pygame.joystick.Joystick(0)
    joystick_list = setup_joysticks()
    count_buttons=joystick.get_numbuttons()
    




bg=(83,92,166)

print(pygame.display.Info())
print(pygame.display.list_modes())

clock = pygame.time.Clock()
#BAHHHHH - pygame.scaled causes HUGE lag issue, will need to reduce 
screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)#,32)#pygame.NOFRAME
FontMain = pygame.font.SysFont(None, 28)
pygame.mouse.set_visible(False)


#analog joystick stuff here
swt_channel=0
vrx_channel=1
vry_channel=2
delay = 0.5

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data



start_check=time.time()
justcheckingbro=[]
while time.time()-start_check<2: #two seconds to check data coming from 2-axis analog joystick
    if readChannel(vrx_channel) > 400 and readChannel(vrx_channel) < 624:
        justcheckingbro.append(1)

if len(justcheckingbro)>40: #getting consistent values within expected range of the 2-axis joystick range (512)
    ANALOG=True
    
    #add custom events
    UP_EVENT=pygame.USEREVENT+1
    DOWN_EVENT=pygame.USEREVENT+2
    LEFT_EVENT=pygame.USEREVENT+3
    RIGHT_EVENT=pygame.USEREVENT+4
    
    UP_EVENTev=pygame.event.Event(UP_EVENT)
    DOWN_EVENTev=pygame.event.Event(DOWN_EVENT)
    LEFT_EVENTev=pygame.event.Event(LEFT_EVENT)
    RIGHT_EVENTev=pygame.event.Event(RIGHT_EVENT)
    
else: #this means was only getting '0' from the readings indiciating the 2-axis joystick was not hooked up
    ANALOG=False
    vrx_pos=0
    vry_pos=0

#Note: this can be broken if you hold the joystick in the up/left position causing that 0,0 reading at start
#Solution: just don't be an ass and do that. Isn't life simpler that way?


heldLeft=0
totalLeft=0

heldRight=0
totalRight=0

heldUp=0
totalUp=0

heldDown=0
totalDown=0


Intro=True
getMessage=open('/home/pi/message.txt','r').read().split('\n')

Font4Intro=pygame.font.SysFont(None, 25)


#just intro to what scripts are being used and whether the analog or digital inputs for movements are being used
def showInfo(Intro,vrx_pos,vry_pos):
    if time.time()-start_time<=4: #script version detect
        showMessage=getMessage[:]
    elif time.time()-start_time>4 and time.time()-start_time<=8:# joystick type detect
        if (vrx_pos,vry_pos)==(0,0):
            bottomString='-Analog joystick not detected-'
        else:
            bottomString='-Analog joystick detected-'

        showMessage=['Joystick readings: '+str(vrx_pos)+', '+str(vry_pos),bottomString]
    else:
        showMessage=['','']
        Intro=False


    s_transparent = pygame.Surface((width,height),pygame.SRCALPHA, 32)
    s_transparent = s_transparent.convert_alpha()
    pygame.draw.rect(s_transparent,(35,35,35,190),[0,0,width,height])         
    screen.blit(s_transparent,(0,0))


    pygame.draw.rect(screen,(0,51,102),[0,int(height/4),width,int(height/4)+10])
    

    textWidth,textHeight=Font4Intro.size(showMessage[0])
    Text=Font4Intro.render(showMessage[0], 1, (250,250,250))
    screen.blit(Text,(int(width/2)-int(textWidth/2),int(height*(3/8)-(textHeight))))

    textWidth,textHeight=Font4Intro.size(showMessage[1])
    Text=Font4Intro.render(showMessage[1], 1, (250,250,250))
    screen.blit(Text,(int(width/2)-int(textWidth/2),int(height*(3/8)+(textHeight))))

    return Intro


start_time=time.time()


def check_min(held,total,vrz_pos,postThis):
    if vrz_pos<=300: #adjusting ratio
        """
        if total>=float(framerate)*1.6:
            useRatio=5
        elif total>=float(framerate)*1.2:
            useRatio=4
        elif total>=float(framerate)*.8:
            useRatio=3
        elif total>=float(framerate)*.4:
            useRatio=2
        else:
            useRatio=1
        """
        if total>=float(framerate)*1.2:
            useRatio=13
        elif total>=float(framerate)*1:
            useRatio=11
        elif total>=float(framerate)*.8:
            useRatio=9
        elif total>=float(framerate)*.6:
            useRatio=7
        elif total>=float(framerate)*.4:
            useRatio=5
        elif total>=float(framerate)*.2:
            useRatio=3
        else:
            useRatio=1

        total+=1
        held+=1

        if held==1 and vrz_pos<=300: #instant add new event and start timer
            pygame.event.post(postThis)
        elif held>=framerate/useRatio and vrz_pos<=300:
            pygame.event.post(postThis)
            held=1
    else:
        held=0
        total=0

    return held,total



def check_max(held,total,vrz_pos,postThis):

    if vrz_pos>=1024-300: #1024 is the other side of the potentiometer
        if total>=float(framerate)*1.2:
            useRatio=13
        elif total>=float(framerate)*1:
            useRatio=11
        elif total>=float(framerate)*.8:
            useRatio=9
        elif total>=float(framerate)*.6:
            useRatio=7
        elif total>=float(framerate)*.4:
            useRatio=5
        elif total>=float(framerate)*.2:
            useRatio=3
        else:
            useRatio=1

        total+=1
        held+=1

        if held==1 and vrz_pos>=1024-300: #instant add new event and start timer
            pygame.event.post(postThis)
        elif held>=framerate/useRatio and vrz_pos>=1024-300:
            pygame.event.post(postThis)
            held=1
    else:
        held=0
        total=0

    return held,total

framerate=30

showCursor=True


while True:


    screen.fill(bg)

    #CHECK UP/DOWN/LEFT/RIGHT changes
    if ANALOG is True:

        vrx_pos = readChannel(vrx_channel)
        vry_pos = readChannel(vry_channel)
        swt_val = readChannel(swt_channel)

        heldLeft,totalLeft=check_min(heldLeft,totalLeft,vrx_pos,LEFT_EVENTev) #left
        heldUp,totalUp=check_min(heldUp,totalUp,vry_pos,UP_EVENTev) #up
        
        heldRight,totalRight=check_max(heldRight,totalRight,vrx_pos,RIGHT_EVENTev)
        heldDown,totalDown=check_max(heldDown,totalDown,vry_pos,DOWN_EVENTev)
            
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()    


        if event.type==LEFT_EVENT:
            adjustMe=joyButtons[1][:]
            adjustMe[3]=True
            adjustMe[4]=30
            joyButtons[1]=adjustMe[:]

            if movx>=1:
                movx-=1

        if event.type==UP_EVENT:
            adjustMe=joyButtons[0][:]
            adjustMe[3]=True
            adjustMe[4]=30
            joyButtons[0]=adjustMe[:]
            
            if movy>=1:
                movy-=1

        if event.type==RIGHT_EVENT:
            adjustMe=joyButtons[2][:]
            adjustMe[3]=True
            adjustMe[4]=30
            joyButtons[2]=adjustMe[:]  

            if movx<=mapwidth-2:
                movx+=1

        if event.type==DOWN_EVENT:
            adjustMe=joyButtons[3][:]
            adjustMe[3]=True
            adjustMe[4]=30
            joyButtons[3]=adjustMe[:]

            if movy<=mapheight-2:
                movy+=1


        #Check JoyPad Buttons
        if event.type==pygame.JOYBUTTONDOWN:
            adjustMe=False
            for i in range(0,count_buttons):
                if joystick.get_button(i)==1:

                    for j in range(len(joyButtons)):
                        item=joyButtons[j]
                        if int(item[2])==int(i):
                            gotEm=int(j)
                            break
                        
                    adjustMe=joyButtons[gotEm][:]#=True
                    adjustMe[3]=True
                    adjustMe[4]=30

            if adjustMe is not False:
                joyButtons[gotEm]=adjustMe[:]


    #draw circle
    def draw_main(button_name,button_location,drawYesNo,expand,vrx,vry):
        
        quickModSize=0
            
        pygame.draw.circle(screen, (37,53,114), (button_location[0],button_location[1]), 31-quickModSize)
        
        if drawYesNo is True:
            pygame.draw.circle(screen, (11,207,255), (button_location[0],button_location[1]),expand-quickModSize,4)
            

        if (vrx,vry)!=(False,False): #I think I can remove some of these checks now, no? double check
            
            sensitivity=300
            
            if vrx < sensitivity and button_name=="LEFT": #left
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
            elif vrx > 1024-sensitivity and button_name=="RIGHT": #right
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
                
            
            if vry < sensitivity and button_name=="UP": #up
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
            elif vry > 1024-sensitivity and button_name=="DOWN": #down
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
                   
        if quickModSize==0: #always true, keep for now due to gpio options
            Text=FontMain.render(button_name, 1, (250,250,250))
            screen.blit(Text, (button_location[0]-(FontMain.size(button_name)[0]/2),button_location[1]-(FontMain.size(button_name)[1]/2)))


    reduceAxis=[]
    reduceButton=[]


    for joyButton in joyButtons:
        draw_main(joyButton[0],joyButton[1],joyButton[3],joyButton[4],False,False)
        reduceButton.append(joyButtons.index(joyButton))

    for item in reduceButton:
        temp=joyButtons[int(item)]
        if int(temp[4])<=int(47):
            temp[4]+=3
        else:
            temp[3]=False
            temp[4]=30

        reduceButton[item]=temp[:]
        
    if swt_val==0:        
        xx=joyButtons[0][1][0] #finding center between the up/down/left/right circles on display
        yy=joyButtons[1][1][1]
        pygame.draw.circle(screen, (37,53,114), (xx,yy), 10)
        audioTest()
    

    if showCursor is True:
        count_mov+=1
        RATE=3
        if count_mov == int(RATE*1.5):
            MOVING_TRANSPARENCY=MOV02
        elif count_mov==int(RATE*2):
            MOVING_TRANSPARENCY=MOV03
        elif count_mov==int(RATE*2.5):
            MOVING_TRANSPARENCY=MOV04
        elif count_mov==int(RATE*8):
            MOVING_TRANSPARENCY=MOV03
        elif count_mov==int(RATE*8.5):
            MOVING_TRANSPARENCY=MOV02
        elif count_mov==int(RATE*9):
            MOVING_TRANSPARENCY=MOV01
        elif count_mov==int(RATE*15.5):
            count_mov=int(RATE*1.5)-1


        """
        tilesize = 30
        mapwidth = 18
        mapheight = 12

        movx=mapwidth/2
        movy=mapheight/2
        """

        screen.blit(MOVING_TRANSPARENCY, (movx*tilesize-3,movy*tilesize-3))



    if Intro is True:
        Intro=showInfo(Intro,vrx_pos,vry_pos)


    pygame.display.update()
    clock.tick(framerate)