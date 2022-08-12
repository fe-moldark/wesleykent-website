---
layout: page
title: Raspberry Pi Projects
subtitle: 
image: /assets/fe.ico
description: 
permalink: /raspberrypi/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

# Custom RetroPie
This project took a good chunk of time, but now runs RetroPie perfectly, sound included, with a larger case than normal for comfort reasons. I know parts of this design will get some hate for using a) wood for the case, and b) for using a Pi3 instead of a pi zero. At the time using a Pi3 made more sense due to the specific lcd screen I already had and since the case was designed to be larger anyway, a Pi 3 fit easily. As far as using wood, it was a fun way to avoid having to 3d print a small case and allowed me more freedom when designing it. Haven't had any issues with it overheating yet (going on two years) as the backing provides more than enough ventilation. Currently has over 3 dozen games installed and alleviates boredom when needed - definitely a success.<br>
<p align="center"><img width="950" src="/assets/rpi/retropie1.jpg"></p>

<img src="/assets/rpi/retropie2.jpg" alt=""> | <img src="/assets/rpi/retropie4.jpg" alt="">

<br><br>

# Home NAS and VPN Server
I finally got my NAS up and running, it uses a simple file sharing service I can use in conjunction with the VPN for remote access, and conveniently works with both my phone and laptop. I might also hook up my home printer to the samba service, although that seems like unnecessary work right now and I would need another raspberry pi to act as a print server. VPN is running PiVPN with wire guard (via freedns).<br>
<p align="center"><img width="850" src="/assets/rpi/nasvpn.jpg"></p>
<br><br><br>

# Dashcam
This project took just a bit of research and writing the software for the project even as I was assembling the hardware. The first image below, or "Version 1.0" as I call it, with the LCD screen proved too heavy to stay stuck to the windshield when driving over bumpy roads. "Version 2.0" (3rd image) was more lightweight and has only slightly less functionality but still includes the switches and LEDs needed for control and monitoring. Records with a push of a button and a flip of a switch, and provides plenty of room for heat to escape.<br>
<p align="center"><img width="850" src="/assets/rpi/dash1.jpg"></p>

<img src="/assets/rpi/dash2test.jpg" alt=""> | <img src="/assets/rpi/dash3test.jpg" alt="">


<br><br>

# Home Security
You might be wondering where the security system is - and yes, that is kinda the point. The hardware (a basic pi zero and the Pi NoIR Camera) is hidden inside of an old broken speaker. The camera faces towards my door and is barely noticeable even when you know where to look as it is viewing through a drilled hole in line with the grains in the wood (opposite side of the speaker / desk leg). The Pi is running "MotionEye", a handy OS for Pis that begins recording on motion detection and both saves recordings locally on the pi and remotely uploads them to one of my google drive accounts. All that's left is to cover up the green LED from the pi and no one's the wiser.<br><br>
One other note is I have a screen for my VPN (see above) that I wanted to be able to view my security logs with, however the MotionEye OS is, intentionally, very limited even running as root. After being unable to access the saved files on the drive via google credentials, I resorted to running tcdump on the VPN server's startup (using either .bashrc or rc.local, I forget which), filtering for the specific IP address and for incoming ICMP packets. From there I configured a script that simply pings the VPN whenever a new log is created, and the security logs counter on the VPN screen reflects those counts. Far from a simple solution for such a simple want, but it works.<br>
<br>![](/assets/rpi/security.jpg)<br>
<br><br>

# ISS Livestream at Startup
Simply put, it's a Pi3 B+ hooked up to a 7" display. Script can auto-run from startup after configuring the .bashrc file. It opens a live stream from the International Space Station as seen below, which I think is kinda neat. The screen is also large enough to work for regular desktop scenarios if needed, just a bit small.<br>
<br>
<center>
	<img src="/assets/rpi/isslivestream.jpg" alt=""><br>
</center>
<br><br>

# Ongoing Projects
### Audio System and USB Injectors
Having completed the VPN and NAS projects I will likely be taking a break as I study for certifications. The mess pictured below is an old, slightly disassembled audio system that has buttons to play/pause, skip, mute, shuffle and utilizes a rotary encoder for volume control. Fun stuff. My projects for the USB Injector are currently on the far back burner as they will take a good amount of research and learning to get started. As I mentioned I've also got my Pi3 hooked up to my wall for an easier desktop environment, but I often plug that into my extra monitor to avoid dealing with the smaller 7" screen.<br>
<center>
<img src="/assets/rpi/ongoing.jpg" alt=""><br>
</center>
<br>
