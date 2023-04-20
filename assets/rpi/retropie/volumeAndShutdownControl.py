#Credit to this guy for the rotary encoder / volume control
#https://gist.github.com/shivasiddharth/6aba5fa187c8ce463259f18eb7171a1f




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
import alsaaudio
import time

# Change the following pins based on your application or HAT in use
encoder_clk = 4
encoder_data = 17
encoder_button = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(encoder_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_data, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(encoder_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)



#shutdown stuff by me
shutdownButton=NUMBER
GPIO.setup(shutdownButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)



m = alsaaudio.Mixer()

# Set desired minimum and maximum values
min = 0
max = 100

# Set the volume change step size
volume_step_size=5

is_Muted = m.getmute()[0]
volume = m.getvolume()[0]

if is_Muted == 0:
    is_Muted=False
else:
    is_Muted=True
print("Mute State: " + str(is_Muted))
print("Volume: " + str(volume))
print("")
clkLastState = GPIO.input(encoder_clk)
btnLastState = GPIO.input(encoder_button)


count_for_shutdown=0


try:
    while True:
        btnPushed = GPIO.input(encoder_button)
        if ((not btnLastState) and btnPushed):
            if is_Muted:
                is_Muted = False
                m.setmute(0)
                print("Mute State: " + str(is_Muted))
                print("Volume: " + str(int(volume)))
                print("")
            else:
                is_Muted = True
                m.setmute(1)
                print("Mute State: " + str(is_Muted))
                print("Volume: " + str(int(volume)))
                print("")
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
                if clkState == 1:
                    print("Mute State: " + str(is_Muted))
                    print("Volume: " + str(int(volume)))
                    print("")
                    m.setvolume(int(volume))
            clkLastState = clkState
        btnLastState = btnPushed
        
        
        
        start = time.time()
        input_state=GPIO.input(18)
        if input_state==False: #Button Pressed
            if start==0:
                start = time.time()
        elif input_state==True:
            start=0
            
        if start!=0:
            if time.time()-start>=4: #if has been pressed for more than 10 seconds
                os.system("sudo shutdown -h now")
            
            

finally:
    GPIO.cleanup()
 
