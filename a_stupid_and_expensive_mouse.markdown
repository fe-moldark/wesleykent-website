---
layout: page
title: A Stupid and Expensive Mouse
subtitle: This is actually a 'proof of concept' for a larger project - but still
description: This is actually a proof of concept for a larger project - but still
permalink: /electronics/a_stupid_and_expensive_mouse/
---

<head>
  <link rel="stylesheet" type="text/css" href="/styles/embedded_videos_and_stls.css">
</head>


# Introduction
Have you ever taken a long, hard look in the mirror and wondered what is wrong with your life? Well, I found the answer: your computer mouse is too simple to use. What you need is a poorly designed, overcomplicated, inefficient, and expensive alternative. This has all the functions you would expect from a typical computer mouse to include mouse movement, left and right buttons, and a scroll wheel of sorts. I give you... whatever this thing is:<br>
<center>
  <img width="1200" src="/assets/usb_hid.jpg">
</center>
<center>
  <iframe id="content" src="https://www.youtube.com/embed/bCFhI2NDR2Q" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe><br>
</center>
<br><br>

# Hardware
- <a href="https://www.pjrc.com/store/teensy40.html" target="_blank" rel="noopener noreferrer">1x PJRC Teensy 4.0</a>
- <a href="https://www.amazon.com/dp/B08MQCK8KN" target="_blank" rel="noopener noreferrer">1x PSP 2-Axis Analog Thumb Joystick</a>
- <a href="https://www.amazon.com/dp/B07D3D64X7" target="_blank" rel="noopener noreferrer">1x EC11 Rotary Encoder</a>
- <a href="https://www.amazon.com/dp/B07F7W91LC" target="_blank" rel="noopener noreferrer">1x Logic Level Converter Bi-Directional 3.3V-5V Shifter Module</a>
- <a href="https://www.adafruit.com/product/4183" target="_blank" rel="noopener noreferrer">2x Buttons (like these)</a>
- <a href="https://www.adafruit.com/search?q=resistors" target="_blank" rel="noopener noreferrer">4x 10K resistors</a>
- 1x Perf board
- Solder, soldering iron, wire (28-30 AWG)
<br><br>

# What this will be used for
I am "restoring" an old Zenith Data Systems laptop by using the case and putting entirely new hardware inside. One thing I need to do for this project is add a mouse trackpad of some kind in there, and this was the solution I came up with. I wanted to get a working version before designing the 3d components that will house it all. I'll be putting up more stuff like this for the laptop in time and it's going to end up really cool. You will have ways to power it over a DIY battery pack or directly plugged, 2x external USB ports, an ethernet jack, audio control and switches with a potentiometer and 3.5mm jack, HDMI out, SD card adapter, malicious USB device storage, two _additional_ LCDs to monitor remaining battery and system resources, and it will be using the original keyboard (this will take a lot of work I think).
<br><br>

# Circuit diagram
I just drew this out instead of finding something more professional, sorry. Here it is:<br>
<center>
  <img width="1000" src="/assets/circuit_usb_hid.jpg">
</center>

<br><br>

# Software
Okay, this part is relatively straight forward. Assuming the hardware is connected correctly that is. Using the Arduino IDE select the Teensy 4.0 as your board and designate the USB type as "Serial, Keyboard, Mouse, Joystick". If you are missing any of the boards / libraries you can find resources online on how to install them. Link to script is <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/Zenith/usb_mouse_v10.ino" target="_blank" rel="noopener noreferrer">here</a>, otherwise just copy below directly:<br>
```cpp
/*This script uses the Teensy 4.0 to emulate a mouse
 * 
 * A rotary encoder mimics the scroll function, two buttons mimick the Left and 
 * Right button clicks, and the PSP joystick controls mouse movement.
 * 
 * From the Arduino IDE use the Teensy 4.0 as the Board and USB Type as "Serial,
 * keyboard, Mouse, Joystick"*/


#include <Bounce.h>

const int moveDistance = 5;  // how much to move the mouse on each button press

const int joyXPin = A0;  // Joystick X-axis input
const int joyYPin = A1;  // Joystick Y-axis input

int joyXValue, joyYValue;


const int encoderPinA = 1;
const int encoderPinB = 2;

volatile int encoderPosition = 0;
volatile int lastEncoded = 0;

const int grayCode[16] = {0, 1, 3, 2, 7, 6, 4, 5, 15, 14, 12, 13, 8, 9, 11, 10};


Bounce button6 = Bounce(6, 10);
Bounce button7 = Bounce(7, 10);



void setup() {
	
	Serial.begin(9600);
	
	pinMode(6, INPUT_PULLUP);
	pinMode(7, INPUT_PULLUP);
	
	Mouse.screenSize(1000, 600);
	
	pinMode(encoderPinA, INPUT);
	pinMode(encoderPinB, INPUT);
	
	attachInterrupt(digitalPinToInterrupt(encoderPinA), updateEncoder, CHANGE);
	attachInterrupt(digitalPinToInterrupt(encoderPinB), updateEncoder, CHANGE);
	
}


void loop() {
	
	button6.update();
	button7.update();
	
	joyXValue = analogRead(joyXPin);
	joyYValue = analogRead(joyYPin);
	
	//Serial.println(joyXValue);
	//Serial.println(joyYValue);
	//Serial.println("------");
	
	
	/* PSP joystick values I was getting
	 *  X - normal: 532-541
	 *  - left:   842
	 *  - right:  167
	 * 
	 * Y - normal: 457-490
	 *  - up:     157
	 *  - down:   840
	 */
	
	
	/*Well, let's build a simplish range for this stuff
	 *  
	 *  512 is (or supposed to be) center / average
	 *  375-512-649 will qualify as no movement - the 'normal' values fluctuate, so keep the range as is for now
	 *  
	 *  Anything above or below should return a value that will modify the mouse position
	 */
	
	
	int threshold = 137;
	int base = 512; // 1024/2 = 
	int mouseMoveRate = 5;
	
	
	//int mouseX = map(joyXValue, 0, 1024, 0,255);
	int mouseX;
	if (joyXValue <= base-threshold) { //left
		mouseX = -1*mouseMoveRate;
	} else if (joyXValue > base+threshold && joyXValue != 1023) { //right
		mouseX = 1*mouseMoveRate;
	} else { //pass
		mouseX = 0;
	}
	
	int mouseY;
	if (joyYValue <= base-threshold) { //up
		mouseY = -1*mouseMoveRate;
	} else if (joyYValue > base+threshold && joyYValue != 1023) { //down
		mouseY = 1*mouseMoveRate;
	} else { //pass
		mouseY = 0;
	}
	
	
	Mouse.move(mouseX, mouseY, 0);
	
	if (button6.fallingEdge()) {
		Mouse.press(MOUSE_RIGHT);
	}
	if (button6.risingEdge()) {
		Mouse.release(MOUSE_RIGHT);
	}
	
	if (button7.fallingEdge()) {
		Mouse.press(MOUSE_LEFT);
	}
	if (button7.risingEdge()) {
		Mouse.release(MOUSE_LEFT);
	}
	
	delay(10);
	
}


void updateEncoder() {
	int MSB = digitalRead(encoderPinA);
	int LSB = digitalRead(encoderPinB);
	
	int encoded = (MSB << 1) | LSB;
	int sum = (lastEncoded << 2) | encoded;
	
	int state = grayCode[sum & 0b1111];
	
	if (state == 1 || state == 7 || state == 8 || state == 14) {
		encoderPosition++;
		Mouse.scroll(+3);
	} else if (state == 2 || state == 4 || state == 11 || state == 13) {
		encoderPosition--;
		Mouse.scroll(-3);
	}
	
	lastEncoded = encoded;
	
	Serial.println(encoderPosition);
}
```
<br><br>

# Final thoughts
The code for the rotary encoder needs some adjustments as it's still acting a bit iffy. To modify the speed of the mouse you can increase or decrease the `mouseMoveRate`. Also, if you do this with another 2-axis joystick you may need to adjust some of the ranges and exceptions I am using. Otherwise everything works fine, in time I'll get the 3d model designed and printed off for the laptop.
<br><br>
