import pygame
from pygame.locals import *
import time, sys
import spidev



mod=10
adj=260

width, height = (720,480)

#third value is the associated joybutton
joyButtons=[
    ["A",(300+adj,150-mod),0,False,30],
    ["B",(240-mod+adj,210),3,False,30],
    ["X",(360+mod+adj,210),1,False,30],
    ["Y",(300+adj,270+mod),2,False,30],
    ["START",(int(width/2)-70,410),8,False,30],
    ["SELECT",(int(width/2)+70,410),9,False,30],
    ["L SHOULDER",(80,50),4,False,30],
    ["R SHOULDER",(640,50),6,False,30]
    ]
    

#no longer using, but keep just in case
gpioButtons=[
    ["Panel 1",(30,120),24,False,30],
    ["Panel 2",(30,180),5,False,30],
    ["Panel 3",(30,240),6,False,30],
    ["Panel 4",(30,300),3,False,30],
    
    ["Lower Button",(30,410),21,False,30]
    ]

#JoyAxisMotion
twoAxisMotion=[
    ["UP",(160,150-mod),0,False,30],
    ["DOWN",(160,270+mod),0,False,30],
    ["LEFT",(100-mod,210),0,False,30],
    ["RIGHT",(220+mod,210),0,False,30]
    ]

#defineLEDs, third element is the counter
defineLEDs=[
    (25,False,15),
    (27,False,15),
    (29,False,15),
    (26,False,15)
    ]
    
    
    

pygame.mixer.pre_init(frequency=44100,size=-16,channels=2,buffer=4096)
pygame.init()
pygame.mixer.init()


def callOrder66():
    pygame.mixer.music.load('/home/pi/Downloads/order66.mp3')
    pygame.mixer.music.play(0)



def setup_joysticks():
    joystick_list = []
    for i in range(0, pygame.joystick.get_count()):
        joystick_list.append(pygame.joystick.Joystick(i))
        pygame.joystick.Joystick(i).init()
    return joystick_list

joystick_count=pygame.joystick.get_count()

if joystick_count == 0:
    print("Error, no Joysticks found. Exiting program now.")
    time.sleep(1.5)
    pygame.quit()
    sys.exit()
else:
    #Only ever gonna be one joystick
    joystick = pygame.joystick.Joystick(0)
    joystick_list = setup_joysticks()
    count_buttons=joystick.get_numbuttons()
    




bg=(83,92,166)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
FontMain = pygame.font.SysFont(None, 28)
pygame.mouse.set_visible(True)



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
    



while True:


    screen.fill(bg)
    
    vrx_pos = readChannel(vrx_channel)
    vry_pos = readChannel(vry_channel)
    swt_val = readChannel(swt_channel)
 
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()                


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
        if str(button_name) in [str(getThis[0]) for getThis in gpioButtons]: 
            quickModSize=15
            
        pygame.draw.circle(screen, (37,53,114), (button_location[0],button_location[1]), 31-quickModSize)
        
        if drawYesNo is True:
            #print(button_name," is true")
            pygame.draw.circle(screen, (11,207,255), (button_location[0],button_location[1]),expand-quickModSize,4)
            
            
        if (vrx,vry)!=(False,False):
            
            if vrx < 212 and button_name=="LEFT": #left
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
            elif vrx > 812 and button_name=="RIGHT": #right
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
                
            
            if vry < 212 and button_name=="UP": #up
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
            elif vry > 812 and button_name=="DOWN": #down
                pygame.draw.circle(screen, (58,113,222), (button_location[0],button_location[1]), 31)
                   
        if quickModSize==0:
            Text=FontMain.render(button_name, 1, (250,250,250))
            screen.blit(Text, (button_location[0]-(FontMain.size(button_name)[0]/2),button_location[1]-(FontMain.size(button_name)[1]/2)))
        else:
            Text=FontMain.render(gpioButton[0], 1, (250,250,250))
            screen.blit(Text, (60,gpioButton[1][1]-9))
            


    reduceAxis=[]
    for axisMotion in twoAxisMotion:
        draw_main(axisMotion[0],axisMotion[1],axisMotion[3],axisMotion[4],vrx_pos,vry_pos)

    reduceButton=[]
    for joyButton in joyButtons:
        #print('joyButton: ',joyButton)
        draw_main(joyButton[0],joyButton[1],joyButton[3],joyButton[4],False,False)
        reduceButton.append(joyButtons.index(joyButton))
    for item in reduceButton:
        temp=joyButtons[int(item)]
        if int(temp[4])<=int(55):
            temp[4]+=3
        else:
            temp[3]=False
            temp[4]=30

        reduceButton[item]=temp[:]
        
    if swt_val==0:
        xx=twoAxisMotion[0][1][0] #finding center between the up/down/left/right circles on display
        yy=twoAxisMotion[2][1][1]
        pygame.draw.circle(screen, (37,53,114), (xx,yy), 12)
        callOrder66() #someone get eyes on Tup...



    pygame.display.update()
    clock.tick(30)

