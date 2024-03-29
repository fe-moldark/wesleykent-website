# Credit to this guy for the rotary encoder part: https://gist.github.com/shivasiddharth/6aba5fa187c8ce463259f18eb7171a1f
# 
# I've had to adopt this to work directly with the HDMI audio using amixer and not alsaaudio
# Might be a difference in using a Pi Zero board or it could be the OS, not sure, but this way works



#***************************************************************************************
#               Code for Controlling Pi Volume Using Rotary Encoder
#                     Original Code: https://bit.ly/2OcaQGq
#                    Re-Written by Sid for Sid's E Classroom
#                    https://www.youtube.com/c/SidsEClassroom
#             All text above must be included in any redistribution.
#  If you find this useful and want to make a donation -> https://paypal.me/sidsclass
# ***************************************************************************************
 
from RPi import GPIO
from time import sleep
#import alsaaudio
import time

encoder_clk = 4
encoder_data = 17
encoder_button = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(encoder_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_data, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)



import subprocess
#subprocess.call(["amixer", "sset", "HDMI", str(new_percent)+"%"]) 


# Set desired minimum and maximum values
min = 60 #high, I know, but is what it is - basically muted below this point
max = 100
volume=80 #let's start things below the max...
subprocess.call(["amixer", "sset", "HDMI", "80%"]) 
volume_step_size=4

clkLastState = GPIO.input(encoder_clk)
btnLastState = GPIO.input(encoder_button)


try:
    while True:
        btnPushed = GPIO.input(encoder_button)
        if ((not btnLastState) and btnPushed):
            sleep(0.05)
        else:
            clkState = GPIO.input(encoder_clk)
            dtState = GPIO.input(encoder_data)
            if clkState != clkLastState:
                if dtState != clkState:
                    volume += volume_step_size/2
                    if volume > max:
                        volume = max
                else:
                    volume -= volume_step_size/2
                    if volume < min:
                        volume = min
                if clkState == 1: #encoder moved, update with new volume
                    subprocess.call(["amixer", "sset", "HDMI", str(volume)+"%"]) 
            clkLastState = clkState
        btnLastState = btnPushed

finally:
    GPIO.cleanup()