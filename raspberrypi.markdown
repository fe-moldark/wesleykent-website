---
layout: page
title: Raspberry Pi Projects
subtitle: 
image: /assets/fe.ico
description: 
permalink: /raspberrypi/
---

# Home NAS and VPN Server
I finally got my NAS up and running, it uses a simple file sharing service I can use in conjunction with the VPN for remote access, and conveniently works with both my phone and laptop. The NAS is now running off a RPi 4 for better performance than the Pi Zero could ever offer, and I'm using a 256Gb SSD instead of the 16Gb USB stick. I might also hook up my printer to the network, although that seems like unnecessary work right now and I would need to purchase another Raspberry Pi to do so. The VPN server is running PiVPN with WireGuard (via freedns).<br>
<center>
  <img width="850" src="/assets/rpi/nasvpn.jpg">
</center>
<br><br><br>


# Home Security
You might be wondering where the security system is - and yes, that is kinda the point. The hardware (a RPi Zero W and the Pi NoIR Camera) is hidden inside of an old broken speaker. The camera faces towards my door and is barely noticeable even when you know where to look as it is viewing through a drilled hole in line with the grains in the wood (opposite side of the speaker / desk leg). The Pi is running "MotionEye", a handy OS for Pis that begins recording on motion detection and both saves recordings locally and uploads them to one of my google drive accounts. All that's left is to cover up the green LED from the Pi and no one's the wiser.<br><br>
One other note is I have a screen for my VPN (see above) that I wanted to be able to view my security logs with, however the MotionEye OS is, intentionally, very limited even running as root. After being unable to access the saved files on the drive via google credentials I resorted to running `tcdump` on the VPN server's startup (using either `.bashrc` or `rc.local`, I forget which), and then filtering for the specific IP address and for incoming ICMP packets. From there I configured a script that simply pings the VPN whenever a new log is created, and the security logs counter on the VPN screen reflects those counts. Far from a simple solution for such a simple want, but it works.<br>
<center>
  <img width="750" src="/assets/rpi/security.jpg">
</center>
<br><br><br>


# Other projects
The other projects warrant a page of their own, and you can read more about them by browsing the drop down menu under the `RPi Projects` heading. I've also got some ideas for an audio system and a malicious USB device using a Pi Pico, but those ideas won't be happening for a while.
<br><br><br>
