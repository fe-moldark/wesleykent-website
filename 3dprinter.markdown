---
layout: page
title: 3d Printer Additions
subtitle: An enclosure, OctoPrint, fan filtering system, and temperature monitoring
image: /assets/fe.ico
description: RetroPie Project
permalink: /raspberrypi/3dprinter/
---


<head>
  <link rel="stylesheet" type="text/css" href="/styles/embedded_videos_and_stls.css">
</head>


## Intro
I've ended up adding on several components to my 3d printer setup. This includes running OctoPrint on a Pi3 B+, an Arduino for temperature monitoring, a fan and filter for the enclosure when printing with ABS filament, and the enclosure itself with an added LED strip on the inside. I have already designed some of the cases for all of these projects while others remain unfinished, so some sections might remain incomplete until updated.
<br><br><br>

## The enclosure
To start off, here is what my enclosure looks like:<br>
<center>
  <img src="/assets/3d_printer_stuff/enclosure2_new.jpg" alt="" width=950><br>
  <img src="/assets/3d_printer_stuff/enclosure1_new.jpg" alt="" width=950><br>
</center>
<br>
As you can tell, this is far from any kind of "official" enclosure, rather it is just some pieces of wood that keeps the temperature high enough inside for those annoying filaments like ABS. With the fan / filter running the enclosure reaches a maximum temperature of around 108°F/42°C from what I've observed. I've also brought out some power and ground wires from the printer's PSU that is running the LED strip you can see in the image. The power wire is first routed through a toggle switch on the side for easy on / off control.
<br><br>
Something I am looking to eventually change about this enclosure is buying some plexiglass for the front piece instead of the wood that is currently there. That will just make it easier to check if a print is warped or not sticking to the bed. OctoPrint does allow for some monitoring this way with the camera I have set up, but at the same time I would like to be able to look at it directly.
<br><br>
<center>
  <iframe id="content" src="https://player.vimeo.com/video/820163332?h=c4199368c1&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>
<br><br><br>
## Arduino for monitoring temperature
I didn't really have a need for this initially, but adding the fan filter I'll mention down below pushed me to make this. You may or may not know this, but ABS filament requires a much higher ambient temperature (hence the enclosure) than the other kinds of filaments I normally use like PLA. After adding the fan I was worried I would be pulling too much heat out of the enclosure, and since I had a spare Arduino, temperature sensor and LCD, I decided to write a <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_printer_stuff/temp_monitor.ino" target="_blank" rel="noopener noreferrer">quick script</a> that would let me monitor the temperature inside the enclosure:
<br>
<center>
  <img src="/assets/3d_printer_stuff/temp monitor.jpg" alt="" width=950><br>
</center>
<br>

##### Hardware used:
- <a href="https://www.adafruit.com/product/2488" target="_blank" rel="noopener noreferrer">Adafruit Metro 328</a>
- <a href="https://www.adafruit.com/product/181" target="_blank" rel="noopener noreferrer">Standard 16x2 LCD</a>
- <a href="https://www.amazon.com/gp/product/B009OVGKTQ" target="_blank" rel="noopener noreferrer">DS18B20 Digital Temperature Sensor Module</a>
<br>

_*Note: If you don't want to shell out money for the LCD an alternative I thought of was to use a series of 3-5 LEDs instead. From there you can define parameters of what is too cold or too hot, and then reflect that through which LEDs light up. You can also go with a less powerful microcontroller as well, this sensor isn't doing too much work after all._
<br><br>
I'm considering adding more sensors in time, but for now the Arduino is only acting as a temperature monitor. To set this up yourself you'll need the same hardware as I just described or at least similar enough. The `.ino` script I wrote that interacts with the sensor and LCD can be found <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_printer_stuff/temp_monitor.ino" target="_blank" rel="noopener noreferrer">here</a>.
<br><br>

##### 3D Model
<center>
  <div id="content">
    <iframe id="content" title="Temperature Monitor Case" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/899e236515304c5583b6eaf6474ab7ad/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/temperature-monitor-case-899e236515304c5583b6eaf6474ab7ad?utm_medium=embed&utm_campaign=share-popup&utm_content=899e236515304c5583b6eaf6474ab7ad" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> Temperature Monitor Case </a> by <a href="https://sketchfab.com/femoldark?utm_medium=embed&utm_campaign=share-popup&utm_content=899e236515304c5583b6eaf6474ab7ad" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> femoldark </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=899e236515304c5583b6eaf6474ab7ad" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
  </div>
</center>
<br><br>

##### Circuit diagram:
<center>
  <img src="/assets/3d_printer_stuff/arduino circuit.png" alt="" width=750><br>
</center>
<br><br><br>

## Fan for filtering ABS fumes
When I first started printing with ABS I learned that a) you need a higher ambient temperature (hence the enclosure), and b) it gives off a lot more fumes than PLA and so requires some kind of ventilation or filtering. I realized all I really needed was a fan and some filters after all, and since we were throwing out an old server at work I was able to grab several of its fans before it was scrapped.
<br><br>
<center>
  <img src="/assets/3d_printer_stuff/fan filters.jpg" alt="" width=950><br>
</center>
<br>
##### Hardware used:
- 1x Dell Server Fan Model PFC0612DE (I got mine from an old server, but they can be purchased individually as well)
- <a href="https://www.aliexpress.us/item/3256804358897430.html" target="_blank" rel="noopener noreferrer">1x DC12V Manual Four-Wire PWM Fan Speed Motor Controller Board</a>
- <a href="https://www.adafruit.com/product/3221" target="_blank" rel="noopener noreferrer">1x SPST Toggle Switch</a>
- 1x DC Power Jack Socket
- 1x 12V 2A DC Power Supply
- <a href="https://www.amazon.com/gp/product/B07RNGMXYG" target="_blank" rel="noopener noreferrer">Carbon filters (~3/8” thick)</a>
- Wire, solder, soldering iron, some screws, etc.
<br><br>

The case I designed to house all of that can be seen here:<br>
<center>
  <div id="content">
    <iframe id="content" title="Fan Filter Case for 3D Printer Enclosure" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/3079421cb01249a38283ea86fecf6124/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/fan-filter-case-for-3d-printer-enclosure-3079421cb01249a38283ea86fecf6124?utm_medium=embed&utm_campaign=share-popup&utm_content=3079421cb01249a38283ea86fecf6124" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> Fan Filter Case for 3D Printer Enclosure </a> by <a href="https://sketchfab.com/femoldark?utm_medium=embed&utm_campaign=share-popup&utm_content=3079421cb01249a38283ea86fecf6124" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> femoldark </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=3079421cb01249a38283ea86fecf6124" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
  </div>
</center>
<br><br><br>

MCX backup file for this can be downloaded <a href="https://github.com/fe-moldark/wesleykent-website/raw/gh-pages/assets/3d_files/fan_case/fan_design_final_v3.mcx" target="_blank" rel="noopener noreferrer">here</a>. I've also made an easy to follow assembly guide / what wires connect where in the video below. This should simplify things if you want to replicate this on your own:<br>
<center>
  <iframe id="content" src="https://player.vimeo.com/video/811832169?h=dff157a591&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>
<br><br>

I adopted this same design to work as a solder fume extractor as well. It uses the exact same hardware except for an altered case to shift where the filters are in relation to the fan. Hardware requirements are the same, and links to that model can be found <a href="https://sketchfab.com/3d-models/fan-filter-case-for-3d-printer-enclosure-3079421cb01249a38283ea86fecf6124" target="_blank" rel="noopener noreferrer">here</a>.

<center>
  <div id="content">
    <iframe id="content" title="Solder Fume Extractor" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/d82742ce55c6415dae60637595cb9a2d/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/solder-fume-extractor-d82742ce55c6415dae60637595cb9a2d?utm_medium=embed&utm_campaign=share-popup&utm_content=d82742ce55c6415dae60637595cb9a2d" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> Solder Fume Extractor </a> by <a href="https://sketchfab.com/femoldark?utm_medium=embed&utm_campaign=share-popup&utm_content=d82742ce55c6415dae60637595cb9a2d" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> femoldark </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=d82742ce55c6415dae60637595cb9a2d" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
  </div>
</center>
<br>
MCX backup file for this can be downloaded <a href="https://github.com/fe-moldark/wesleykent-website/raw/gh-pages/assets/3d_files/fan_case/solder_fume_extractor.mcx" target="_blank" rel="noopener noreferrer">here</a>.
<br><br><br>

## OctoPrint
I've gotten OctoPrint more or less set up and configured, all I need to do now is print off a case for the RPi and to hold the camera for time lapse captures. It also looks like I will need to flash the Ender's firmware with a few slight changes to allow OctoPrint to fully work as intended. I'm also setting up OctoDash with a 3.5" touch screen for more control.
<br><br>
I will update this in time, provided I don't forget...
<br><br>

## Print settings
Since this page is all about my printer, here are the settings I've been using with success so far. These are for the Ender 3 Pro when slicing with Cura:
<br>
##### PLA filament:<br>
- Initial layer:
  - Print speed: 10 mm/s
  - Extruder temp: 200.0 °C
  - Build plate temp: 70 °C
- Following layers:
  - Print speed: 50 mm/s
  - Extruder temp:  210 °C
  - Build plate temp: 70 °C
<br><br>

##### ABS filament:<br>
- Initial layer:
  - Print speed: 40 mm/s
  - Extruder temp: 235 °C
  - Build plate temp: 70 °C
- Following layers:
  - Print speed: 55 mm/s
  - Extruder temp: 235 °C
  - Build plate temp: 60 °C
- Retraction distance: 5 mm // Retraction speed: 45mm/s
- Enable print cooling: `False`
<br><br>

_Anything else not mentioned is using the default settings for the Ender 3 Pro printer._
<br><br><br>

