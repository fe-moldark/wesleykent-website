---
layout: page
title: Adding LEDs and Audio to the Lego Gunship
subtitle: Definitely one of my more unique Christmas gifts
permalink: /raspberrypi/gunship_display/
description: Adding LEDs and Audio to the Lego Gunship
---

<head>
  <link rel="stylesheet" type="text/css" href="/styles/embedded_videos_and_stls.css">
</head>

# Introduction
Well, my younger brother bought the new Lego Gunship and I had a spare microcontroller. Was it a financially irresponsible decision of him? Not for me to say. Is it a cool purchase? Yes, yes it is. We had the original version back in the day which makes it even better. Regardless of the backstory no one cares about, I had the idea to upgrade his gunship display with some lights and audio. I wish I had a few better pictures, but here is the final product:
<center>
  <img width="1150" src="/assets/gunship/gunship4.jpg">
  <img width="1050" src="/assets/gunship/gunship3.jpg">
</center>
<center>
  <iframe id="content" src="https://player.vimeo.com/video/903906991?h=ea4db1a0e6" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
  <p><a href="https://vimeo.com/903906991">Gunship Display Electronics</a> from <a href="https://vimeo.com/user186074646">Wesley Kent</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
</center>
<br><br>

# Hardware
- <a href="https://www.adafruit.com/product/4864" target="_blank" rel="noopener noreferrer">1x Pi Pico</a>
- <a href="https://www.adafruit.com/product/4183" target="_blank" rel="noopener noreferrer">1x Button</a>
- <a href="https://www.adafruit.com/product/805" target="_blank" rel="noopener noreferrer">1x SPDT Switch</a>
- <a href="https://www.adafruit.com/product/2130" target="_blank" rel="noopener noreferrer">1x PAM8302A Amplifier</a>
- <a href="https://www.adafruit.com/product/1890" target="_blank" rel="noopener noreferrer">1x 8 Ohm 0.5W speaker</a>
- <a href="https://www.adafruit.com/product/3391" target="_blank" rel="noopener noreferrer">1x 10K Log. Potentiometer</a>
- <a href="https://www.adafruit.com/search?q=resistors" target="_blank" rel="noopener noreferrer">6x 220 Ohm resistors</a>
- <a href="https://www.amazon.com/gp/product/B01AUI4W5U" target="_blank" rel="noopener noreferrer">Some 3.5mm green, red and white LEDs</a>
- 1x 3-Pos DPDT Switch
- Perfboard, 5cm x 7cm
- Micro USB Breakout (male and female ends)
- Wires, solder, soldering iron, etc.
<br><br>

# Circuit Diagram
For the record, I _think_ this is right. I sort of shipped this off before I made the final circuit diagram, but using the script I was able to connect the dots well enough. Here it is:<br>
<center>
  <img width="1150" src="/assets/gunship/gunship circuit diagram.jpg">
</center>
<br><br>

# 3d files
I designed this using Matter Control and the three different sections fit where you would expect - if not, reference the above images. File below, and backup MXC can be found <a href="https://github.com/fe-moldark/wesleykent-website/raw/gh-pages/assets/gunship/lego_gunship_backup.mcx" target="_blank" rel="noopener noreferrer">here</a>:<br>
<center>
  <div id="content">
  <iframe id="content" title="Lego Gunship Display Model" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/7d636b6bc64c4232b02b1238a50173d4/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/lego-gunship-display-model-7d636b6bc64c4232b02b1238a50173d4?utm_medium=embed&utm_campaign=share-popup&utm_content=7d636b6bc64c4232b02b1238a50173d4" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> Lego Gunship Display Model </a> by <a href="https://sketchfab.com/femoldark?utm_medium=embed&utm_campaign=share-popup&utm_content=7d636b6bc64c4232b02b1238a50173d4" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> femoldark </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=7d636b6bc64c4232b02b1238a50173d4" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
  </div>
</center>
<br><br>
_*Disclaimer here: my brother said I actually messed up a bit and the studs need to all be shifted 4mm (or half a block over). If you have some spare lego pieces you can easily get around this, otherwise feel free to modify the file yourself. Not sure when this mistake happened..._
<br><br>


# Software

### Configuring and interfacing with the microcontroller
Here is where I sort of dropped the ball. I'm writing this page a couple months after I first set this up and I did not document my steps. I do know the Pico board is using CircuitPython, and there are more than enough tutorials out there to get that installed. I had to go through four micro usb cables until I found one that had the data pins wired, so don't be worried the Pico board is broken until you are using the right cable.
<br><br>
I do remember when you get that installed you can interface with it by going to your device manager, find which COM port it is loaded under, then use some software like PuTTY to open a serial connection with it.
<br><br>

### The script itself
You can find the link to the entire script here <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/gunship/UploadToNano/code.py" target="_blank" rel="noopener noreferrer">here</a>. It's fairly short and self-explanatory, so I'll just let you read through it on your own:<br>
```python
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
num=3 #start with the lasers
filename=allAudio[num] #this is how we're gonna loop through them on button press


#Without this Leds can get stuck on when switching up audio files
def resetLEDs(led,led2,laserLED1,laserLED2):
    laserLED1.value = False
    laserLED2.value = False
    led.duty_cycle=0
    led2.duty_cycle=0


#damn this gets annoying on a constant loop, below will help with that
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

                else:

                    for cycle in range(0, 65536-step, step):
                        led.duty_cycle = cycle
                        led2.duty_cycle = cycle
                        sleep(0.005)
                    for cycle in range(65535, 1+step, -step):
                        led.duty_cycle = cycle
                        led2.duty_cycle = cycle
                        sleep(0.005)

    except:
        pass

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
```
<br><br>

# Conclusion
Overall a fun project, easy to build, and fairly cheap - except for the gunship itself, that is. If you have any questions about this feel free to [reach out](/about/) and I'll do my best to get back to you.
<br><br>
