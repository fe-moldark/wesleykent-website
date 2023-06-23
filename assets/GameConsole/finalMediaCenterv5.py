# This creates a simple pygame window to display the contents of a USB drive and select video files to play with the python-vlc module
# Hardware pertinent to this script includes a RPi Model 4 board, an Analog joystick with the MCP3008 analog to digital converter, and a USB gamepad
#
# Author: Wesley Kent
# Created: 06/17/2023
#
# https://github.com/fe-moldark/wesleykent-website/tree/gh-pages/assets/GameConsole
#
# Instructions: Navigate with the analog joystick, 'a' for select, and 'b' for deselect. Use 'select' to toggle fullscreen, 'start' to play/pause, and 'x' to exit the player
# Note: there are some issues after returning to the pygame windows after exiting the vlc player, you may need to restart the program afterwards. In my setup this is not an issue so I have not gone to the trouble of identifying the exact issue yet


import sys,os
import vlc
import pygame
from pygame.locals import *
from time import time
import spidev
import subprocess


#vlc will take the focus off the pygame window, so below is needed
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"


joyButtons=[
    ["A",0,False,30],
    ["B",3,False,30],
    ["X",1,False,30],
    ["Y",2,False,30],
    ["START",8,False,30],
    ["SELECT",9,False,30],
    ["L SHOULDER",4,False,30],
    ["R SHOULDER",6,False,30]
    ]


width, height = (230,380)
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (40,15)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height),pygame.NOFRAME)


pygame.mouse.set_visible(True)
pygame.init()


FontMain    = pygame.font.SysFont('agencyfb', 21) #'agencyfb'
FontSmaller = pygame.font.SysFont('agencyfb', 24) #'agencyfb'
FontSelect = pygame.font.SysFont('agencyfb', 27) #'agencyfb'


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
    joystick = pygame.joystick.Joystick(0)
    joystick_list = setup_joysticks()
    count_buttons=joystick.get_numbuttons()


swt_channel=0
vrx_channel=1
vry_channel=2

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000


def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data



#this assumes ONLY one USB device, which is my case
#otherwise it'll just grab the first one, so best of luck to you

#now adopted to select non-empty directory --> it spawns two empty ones for some reason? idk, this fixed the issue
getConnectedMedia=os.listdir('/media/pi/')

#some are empty
useThisDir=''
for possibleDir in getConnectedMedia:
    if len(os.listdir('/media/pi/'+str(possibleDir)))!=0:
        useThisDir=str(possibleDir)

main='/media/pi/'+useThisDir
tracking=''

listDir=os.listdir(main+tracking)
listDir.remove('System Volume Information')


startTimeList=['>> Start at beginning','>> Start at saved time: ']
cursor=0


lastUP=time()
lastDOWN=time()
lastLEFT=time()
lastRIGHT=time()


bg=(99,126,166)
alt_bg=(60,200,200)


ANALOG=True
VLC_PLAYING=False
QueryWhenStart=False


#clock update_rate
update_rate=30



while True:


    if QueryWhenStart is True:
        screen.fill(alt_bg)
    elif QueryWhenStart is False:
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

        elif event.type==pygame.JOYBUTTONDOWN:

            if QueryWhenStart is False:
            
                if joystick.get_button(3)==1: #(B) 'deselect'
                    
                    if main+tracking!=main:

                        while tracking[-1]!='/':
                            tracking=tracking[:-1]
                        tracking=tracking[:-1]
                        listDir=os.listdir(main+tracking)
                        if 'System Volume Information' in listDir:
                            listDir.remove('System Volume Information')
                    
                elif joystick.get_button(0)==1: #(A) 'select'
                    
                    getName=main+'/'+tracking+'/'+listDir[cursor]                    
                    
                    if os.path.isdir(str(getName)):
                        tracking+='/'
                        tracking+=listDir[cursor]
                        listDir=os.listdir(main+'/'+tracking)
                                                    
                        print('new tracking: ',tracking)

                    else:

                        if VLC_PLAYING is False:
                            VLC_PLAYING=True                            
                            
                            player=vlc.MediaPlayer(getName)
                            player.audio_set_volume(100)
                            player.play()
                    
                    cursor=0
                    
                    
            if VLC_PLAYING is True:
                if joystick.get_button(1)==1: #'X' button
                    player.stop()
                elif joystick.get_button(9)==1: #'Select' button
                    player.toggle_fullscreen()
                elif joystick.get_button(8)==1: #'Start' button
                    if player.is_playing():
                        player.pause()
                    else:
                        player.play()


    #changes in 2-axis joystick
    threshold=25
    btn_break=float(.35)


    if ANALOG is True:

        if VLC_PLAYING is False:
            
            if vry_pos < threshold and float(time()-lastUP) > float(btn_break):
                if VLC_PLAYING is False:
                    if cursor!=0:
                        cursor-=1
                    else:
                        cursor=len(listDir)-1
                lastUP=time()

            elif vry_pos > 1024-threshold and  float(time()-lastDOWN) > float(btn_break):
                if VLC_PLAYING is False:
                    if cursor<len(listDir)-1:
                        cursor+=1
                    else:
                        cursor=0
                lastDOWN=time()

    trackY=40
    startX=25
    spacing=20


    Text=FontMain.render(str(main), 1, (102,0,0)) #main is pwd for current media device
    
    screen.blit(Text, (20,trackY))

    trackY+=30


    for option in listDir:

        if os.path.isdir(str(main+tracking+'/'+option)):
            Color=(202,213,127)
        else:
            Color=(240,240,240)
            
        Text=FontMain.render(option, 1, Color)
        modWidth,modHeight=FontMain.size(option)
        
        if listDir.index(option)==cursor:
            borderAdd=6
            Text=FontSelect.render(option, 1, (10,10,10))
            
            #add '>' indicator separately?
            TextCursor=FontSelect.render('>', 1, (10,10,10))
            screen.blit(TextCursor, (10,trackY-1))
            
        screen.blit(Text, (startX,trackY))
            
        trackY+=spacing


    pygame.display.update()
    clock.tick(update_rate)
