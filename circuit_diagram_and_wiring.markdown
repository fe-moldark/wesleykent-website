---
layout: page
title: Circuit Diagram and Wiring
subtitle: How to put this all together
image: /assets/fe.ico
description: Circuit Diagram and Wiring
permalink: /femoldark/circuit_diagram/
---

# Circuit Diagram
Okay, this should all be setup correctly. If anything does not make sense about it, reference actual images / videos of how it looks on other pages - it is possible this setup will change after all. The parts not included below are the devices that attach via USB, although some do use a couple switches here and there.<br>
<center>
<img src="/assets/circuit_diagram/gameconsole_circuit.png" alt="" width=1050><br>
</center>
<br><br>
The only part from the above diagram that might need explaining is the audio portion. Basically, I am taking audio out from the jack by soldering onto contacts for the left and right channels there, sending that through the potentiometer for volume control and then pushing that to the audio amplifier. From there, the board gets its ground and power from some of the GPIO pins and outputs the left and right channels through a DPDT switch - this will either route the signal to the left and right speakers, or to a 3.5mm headphone jack. I know there are ways to automatically route the audio by completing some circuit or something when you plug in an audio jack, but a manual switch seems easiest for now. The [January Update (Part 2) on this page](/femoldark/gameconsole/) shows how this works.
<br><br><br>

# The rest of the wiring
### USB Extenders
For the USB extenders, there is nothing here that will surprise you - get some <a href="https://www.adafruit.com/product/2225" target="_blank" rel="noopener noreferrer">male and female USB connectors</a>, 4 wires, some solder, and wire it up. I would also recommend some heat shrink tubing to prevent any shorts where applicable. That should end up looking something like this:<br>
<center>
<img src="/assets/circuit_diagram/usb_extenders.png" alt="" width=700><br>
</center>
<br><br>
You can check out some videos on how I assembled them, what length to cut the wires, etc on [this page](/femoldark/gameconsole/). The only thing out of the ordinary with these is that I added a simple SPDT / SPST slide switch on the power pin for both USBs meant for the WiFi and the mass storage device I am using. _*Don't forget: Pin1=Power, Pin2=Data-, Pin3=Data+, Pin4=GND_. To do this simply cut the power wire in two, and hook up the SPDT switch in between. (Note: you can use SPST, all I have right now are a couple SPDT switches, however). That ends up looking like:<br>
<center>
<img src="/assets/circuit_diagram/usb_extender_power_switch.png" alt="" width=500><br>
</center>
<br><br>
I added those switches because the game console is designed to be able to run off its battery after all, so the more I can do to consume less power, the better. Some of the USB slots will always need power, for example the USB joystick and the power to the LCD, but others like the Wi-Fi I am bringing in over USB won't always be needed.
<br><br>

### The Gamepads
What I am using for the gamepads are two of <a href="https://www.adafruit.com/product/2934" target="_blank" rel="noopener noreferrer">these</a> from Adafruit and a USB joystick. You can pass off the inputs from Adafruit's gamepad by directly soldering onto the metal contacts on the USB joystick's board. That USB joystick's board looks like this:<br>
<center>
<img src="/assets/circuit_diagram/usb_gamepad.png" alt="" width=800><br>
</center>
<br><br>
Sadly, I don't recall where I got the USB joystick from - all I remember is that it was fashioned after an old NES controller from eBay (I think). Any one you can find online should work so long as you have those metal points of contact by each of the buttons on the board itself. You can also go the route of directly plugging in the buttons to the GPIO pins on the Pi board, but my way saves ~12 GPIO slots and only uses a single USB port. Handling those inputs over GPIO is also more of a pain within Pygame, but also offers no problems when configuring it for use with the RetroPie software.
<br><br><br>

# Parts / Boards needed
_*Goes without saying but none of this is sponsored, this is just where I happened to source the parts from for this project. If you can find these pieces cheaper elsewhere, go for it._
<br><br>
This isn't a complete list yet, but some of those parts mentioned above can be found here:<br>
- <a href="https://www.adafruit.com/product/987" target="_blank" rel="noopener noreferrer">Stereo 3.7W Class D Audio Amplifier - MAX98306</a>
- <a href="https://www.adafruit.com/product/5270" target="_blank" rel="noopener noreferrer">Alpha Dual-Gang 16mm Right-angle PC Mount - 50K Audio - RV16A01F-41-15R1-A25K-30H4</a>
- <a href="https://www.adafruit.com/?q=resistors&p=5&sort=BestMatch" target="_blank" rel="noopener noreferrer">Some resistors (the ones I used for the LED were 220-330 Ohms, I believe)</a>
- <a href="https://www.adafruit.com/product/2934" target="_blank" rel="noopener noreferrer">2x PiGrrl Zero Custom Gamepad PCB</a>
- For the buttons I used a mix of <a href="https://www.adafruit.com/product/367" target="_blank" rel="noopener noreferrer">these</a>  and <a href="https://www.adafruit.com/product/3101" target="_blank" rel="noopener noreferrer">these</a> depending on purpose and preference
- <a href="https://www.adafruit.com/product/4202" target="_blank" rel="noopener noreferrer">Diffused 3mm LEDs</a>
- <a href="https://www.adafruit.com/product/1890" target="_blank" rel="noopener noreferrer">2x speakers </a>
- <a href="https://www.adafruit.com/product/1699" target="_blank" rel="noopener noreferrer">3.5mm audio jack</a>
- A 2-position DPDT switch <a href="https://raw.githubusercontent.com/fe-moldark/wesleykent-website/gh-pages/assets/circuit_diagram/DPDT_switch.png" target="_blank" rel="noopener noreferrer">that looks something like this</a>
- <a href="https://www.adafruit.com/product/805" target="_blank" rel="noopener noreferrer">2x SPST / SPDT switches</a>
- A RPi 4 or BPi M5 should both work
- Wires, solder, soldering iron, heat shrink tubing, perfboards / breadboards, wire cutters, etc.
<br><br>

All of the above are very specific parts, however you should still be able to find other brands or types depending on your situation. For example, <a href="https://www.digikey.com" target="_blank" rel="noopener noreferrer">DigiKey</a> or <a href="https://www.microcenter.com/" target="_blank" rel="noopener noreferrer">Micro Center</a> should have a lot of these same parts.
<br><br>





