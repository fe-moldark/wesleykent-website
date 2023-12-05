import board
import audiomp3
import audiopwmio
from time import sleep
import pwmio
import digitalio

#Front lasers
laserLED1 = digitalio.DigitalInOut(board.GP18)
laserLED1.direction = digitalio.Direction.OUTPUT
laserLED2 = digitalio.DigitalInOut(board.GP19)
laserLED2.direction = digitalio.Direction.OUTPUT
laserLED1.value = False
laserLED2.value = False

#Pulsing white/red LEDs in the interior
led = pwmio.PWMOut(board.GP11, frequency=1000)
led2 = pwmio.PWMOut(board.GP12, frequency=1000)
step = 250


#Just one button needed
button_pin = digitalio.DigitalInOut(board.GP10)
button_pin.switch_to_input(pull=digitalio.Pull.DOWN) #Pull DOWN - no resistors used


allAudio=["gunshipv2.mp3","ambientGunship.mp3","lasers.mp3","buryingTheDeadv2.mp3"]
num=3
filename=allAudio[num] #this is how we're gonna loop through them on button press



def resetLEDs(led,led2,laserLED1,laserLED2):
    #Without this Leds can get stuck on when switching up audio files
    laserLED1.value = False
    laserLED2.value = False

    led.duty_cycle=0
    led2.duty_cycle=0


#damn this gets annoying on a loop, below will help with that
lasersNeedABreak=0


while True:

    audio = audiopwmio.PWMAudioOut(board.GP0)

    try:
        with open(filename, "rb") as audioFile:
            print("Loading audio: ",filename)
            decoder = audiomp3.MP3Decoder(audioFile)

            audio.play(decoder)

            while audio.playing:

                if button_pin.value:
                    sleep(2)

                    num+=1
                    if num>=len(allAudio):
                        num=0
                    filename=allAudio[num]

                    resetLEDs(led,led2,laserLED1,laserLED2)

                    lasersNeedABreak=0

                    break

                if filename == "lasers.mp3": #Green LEDs only in this instance

                    laserLED1.value = True
                    sleep(0.2)
                    laserLED1.value = False
                    laserLED2.value = True
                    sleep(0.2)
                    laserLED2.value = False

                else: #elif filename=="gunship2.mp3":
                    for cycle in range(0, 65536-step, step):
                        led.duty_cycle = cycle
                        led2.duty_cycle = cycle
                        sleep(0.005)
                    for cycle in range(65535, 1+step, -step):
                        led.duty_cycle = cycle
                        led2.duty_cycle = cycle
                        sleep(0.005)

    except OSError as e:
        print(f"Error: {e}")

    finally:
        audio.stop()
        audio.deinit()

        laserLED1.value = False
        laserLED2.value = False

        if filename=="lasers.mp3":
            lasersNeedABreak+=1

            if lasersNeedABreak>=2: #two loops sounded most natural
                lasersNeedABreak=0
                sleep(4)
