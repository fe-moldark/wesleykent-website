---
layout: page
title: USB Keyboard Controller with a Teensy board
subtitle: Using an original Zenith Data Systems laptop's keyboard
permalink: /electronics/usb_keyboard_controller/
description: DIY USB Keyboard Controller using a Teensy 4.0 and an original Zenith Data Systems Laptop's Keyboard.
---

<head>
  <link rel="stylesheet" type="text/css" href="/styles/embedded_videos_and_stls.css">
</head>

# Introduction
I'm modernizing a non-functioning Zenith Data Systems laptop that was made in the 90s using a Raspberry Pi 5 - well, I'm on backorder right now, so it'll take a few months. Here is the laptop / keyboard:<br>
<center>
  <img width="1050" src="/assets/Zenith/keyboard/laptop_and_keyboard.jpg">
</center><br>
Naturally I wanted to use the original keyboard from the laptop but since we are talking about a very old (and proprietary) keyboard there is no easy plug-and-play solution. Having worked on some keyboard injectors in the past I know you can emulate a keyboard over USB with a microcontroller, so somehow I need to configure the device to interpret inputs from the two FPC cables and then send that data back out as keystrokes. Thankfully, <a href="https://www.instructables.com/How-to-Make-a-USB-Laptop-Keyboard-Controller/" target="_blank" rel="noopener noreferrer">this guy</a> has already made an entire step-by-step process to decode a keyboard's matrix.
<br><br>

# Hardware
- <a href="https://www.pjrc.com/store/teensy40.html" target="_blank" rel="noopener noreferrer">1x PJRC Teensy 4.0</a>
- The keyboard itself (model: Zenith Data Systems Z-note 433Lnp+)
- Some kind of FPC breakout board connector - I cut the original connectors out of the motherboard (RIP)
- 30 gauge wire, solder, soldering iron, etc.
<br><br>

# Configuring this / the software side of things
I'm not going to break this down step by step since it would just be me copying the guy I linked above, but explained worse. Instead I'll give a broad overview of what you are doing and explain some things that had me a bit confused going into this project.
<br><br>
After wiring every pin from the FPC cables to an I/O pin on the Teensy you need to compile and upload the Matrix_Decoder script (again, reference above). Once it is running, you use a separate text file that has every single key that could exist on the keyboard, and line by line manually press every key as they appear on the list. Each key press will produce two numbers for the FPC Pin numbers (NOT the Teensy I/O pins). Using these numbers you will create a matrix (or array) of these numbers that will look something like what I generated below (csv version <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/Zenith/keyboard_matrix_as_csv.csv" target="_blank" rel="noopener noreferrer">here</a>):
<br>
<center>
  <img width="1200" src="/assets/Zenith/keyboard/matrix_v2.jpg">
</center>
<br><br>
Now, how do you determine which numbers are the rows or columns / outputs or inputs? Well, from what I read there are typically 8 input columns and looking at the ribbon cables from the keyboard I noticed one had 8 pins and the other had 11. I went with my gut and sure enough, that was the correct guess. An interesting way to look at this is to actually reference the connections inside the keyboard itself. I took the keyboard apart and snapped this photo:<br>
<center>
  <img width="950" src="/assets/Zenith/keyboard/both_overlays_to_fpc.jpg">
</center>
<br><br>
Looking at this gives you a bit of a headache because it is not set up in direct columns and rows like you saw in the matrix above. Another way to look at this is to manually trace each of these which gave me something that looks like the below picture. Each color represents keys that are linked across a single contact of the FPC cable and keep in mind this was only for one of the overlays.<br>
<center>
  <img width="1100" src="/assets/Zenith/keyboard/colored_schematic_of_wiring.jpg">
</center>
<br><br>
Visually this helps you confirm the numbers that you got from the first text file after running that script and manually pressing each key. Looking at what keys are in the same 'group' reveals the common numbers between them. This step is not necessary, but it is fun to take the keyboard apart and manually trace the wiring. It also helps you identify issues with the keyboard, for instance if 3 or 4 keys are not working that might point to a break in the wiring somewhere that would otherwise not be obvious. Once you have this matrix you move onto the next step which is translating the FPC numbers to their Teensy I/O pin numbers using a table that guy already provides. From there you will need to customize the keyboard ino script with how your own matrix looks like, and this applies to the "normal" keys array, the "media" one, and the "modifier" one. Again, I wont be explaining this in depth because it has already been done in depth on his page <a href="https://github.com/thedalles77/USB_Laptop_Keyboard_Controller/blob/master/Example_Keyboards/Instructions%20for%20modifying%20the%20Teensyduino%204.0%20and%204.1%20code.pdf" target="_blank" rel="noopener noreferrer">here</a>.
<br><br>
In the end you are able to directly plug in the keyboard to your device over USB and use it to its fullest extent. You can use regular keys like letters and numbers, modifier keys allow you to use common shortcuts like CTRL-C or SHIFT+letter for capital letters, and function keys like Fn+F1 for things like Print Screen. You can even program specific keys to perform different functions than they normally would - it's all up to you. All of that in the brief video below:<br>
<center>
  <iframe id="content" src="https://player.vimeo.com/video/892768801?h=bfe4e0d9a8" frameborder="0" allow="autoplay; fullscreen; picture-in-picture" allowfullscreen></iframe>
<p><a href="https://vimeo.com/892768801">zenith_keyboard_with_teensy</a> from <a href="https://vimeo.com/user186074646">Wesley Kent</a> on <a href="https://vimeo.com">Vimeo</a>.</p>
</center>


# Conclusion
Well, another part of this laptop modernization project is done. Next will be the audio which should be fairly straight forward - the LCD module has L +/- and R +/- output, so that will be going through a 3P3T switch. That throws your 3 channels L+, R+ and combined grounds to three options - mute (goes nowhere), a speaker, or an audio jack. If that is as simple as I expect the next step will be using a cheap microcontroller that will measure the voltage coming off the battery to estimate remaining battery capacity and use Adafruit's <a href="https://www.adafruit.com/product/3106" target="_blank" rel="noopener noreferrer">4-Digit 7-Segment FeatherWing</a> to display that as a percentage for the user. If you look at the first image on this page, it will be replacing the old LCD there on the top left next to the power button. And that's all for now. Thanks for reading this far.
<br><br>
