---
layout: page
title: Attacking my Home Network
subtitle: Because I had a weekend off
description: Attacking my home network and searchign for vulnerabilities
permalink: /homenetwork/
---

## Introduction
As the title implies, I was looking for some practical application of vulnerability testing besides just CTFs with intentional vulnerabilities left there. That brought me to attacking my home network, which this page is about, as well as testing my company's network. The latter was only just recently approved and I'm also not even sure what I would be allowed to post about it, but I'm excited to give it a go regardless. Definitely falls outside of the realm of "IT Support", but how much damage could I really do? Maybe I'll take that as a challenge actually...<br><br>
Anyway, for my home network I took a look at four seperate network devices - my security system, NAS, VPN and of course my home router.
<br><br>
## Security System
Let's start off with my Security Camera since that is the one that gave the most surprise. The results of an nmap scan came back as follows:<br>
<p align="center"><img width="850" src="/assets/homenetwork/nmap_eyemotion1.png"></p>
<p align="center"><img width="600" src="/assets/homenetwork/nmap_eyemotion2.png"></p>
Now, this is a part of the security system I have set up back home, and it runs some software called MotionEye, which I've covered on another page previously. At first glance there are way more open ports than I expected - I've only ever interacted with it over ssh and the web interface, so everything else came as a surprise. And yes, that means I probably should have taken a look at this when I first installed it. One other thing worth noting is I hadn't yet implemented the automatic updates that I mentioned on a previous page, so there was some inital concern over running an old version but I've taken care of that since.
<br><br>
SSH I do keep open for management / access purposes. There seemed to be a few vulnerabilities associated with the OpenSSH version I was running and using scp, but from everything I read about them none should affect my particular setup. The best I can do to guard that port right now is keep a strong password.
<br><br>
The web interface over port 80 does prompt a login, and the password for that is more than enough to stand against any kind of brute force attack. Despite running on a raspberry pi the OS is not running any typical setup with an either Debian or Ubuntu-based system, so interacting with it is more of a challenge than usual. Thankfully their web-interface does host a simple "Check" for updates button and while I haven't seen a way to automaitcally check I can periodically login and manually check.
<br><br>
The most concerning open port here was 8081, and from the scan there is note of "JFIF", so some kind of image something is happening. What was concerning was when I navigated to it there was no login page or authentication of any kind. Although it did not offer any management control of the RPi like port 80 has, it did allow a current view of the camera when it is turnedon:
<p align="center"><img width="600" src="/assets/homenetwork/port8081.png"></p>
(Camera fell a bit lopsided, it should be pointed more left towards the door).<br><br>
This was actually not something I initially saw as an option on the management console, but eventually I did find it a bit hidden:<br>
<p align="center"><img width="450" src="/assets/homenetwork/8081_disabled.png"></p>
This must have come with the authentication mode set to disabled by default since I have no memory of changing that, nor do I see any reason for me to have done so. This seems like an oversight if that is in fact the default. Also worth noting that if this were to ever be implemented in anything besides a home network, it should defintely be put on its own subnet. Otherwise anyone apart of the same network could navigate to the page, and even with the authentication mode enabled could try and login to the web portal.
<br><br>
The other ports were hosting access to the smb and ftp servers. Since I was not using either of those particular services I disabled them entirely. Why try and safeguard something I am not using and only poses more risk?
<br><br>

## Networked Attached Storage
This is an important part of my network since it hosts a lot of the reoccuring scripts I am running. As such, I would prefer to keep it secure and luckily there is already a relatively small attack surface:
<p align="center"><img width="700" src="/assets/homenetwork/nmap_nas.png"></p>
This doesn't host a web server to interact with as it does not need one, all it has is ssh and smb over its default ports enabled. The ssh service seems secure enough and has a strong password with a limited login attempt policy implemented. As for the security of the SMB service... I'm not entirely sure. There's nothing I've found that poses a direct threat to it, however the entire SMB share is actually a single external SSD (connected via USB) that I purchased, so someone could just as easily gain physical access and walk away with it in hand. For that reason I don't keep any sensitive files on there - it's basically just a file server I use between devices on my home network to avoid plugging and unplugging USB sticks or hard drives. The particular SMB version also showed no documented vulnerabilities on CVE.
<br><br>

## VPN
The VPN scan was very uneventful:
<p align="center"><img width="550" src="/assets/homenetwork/nmap_vpn.png"></p>
There is quite literally only that one ssh port open. Since this does have to function as a VPN I'm maybe it works in the same way SFTP does over SSH? At the same time it is directly connected over ethernet so the ssh could probably be disabled in its entirety since it just needs to communicate with the router. The only downside is then I would need to bring a screen over to the RPi whenever I needed to manage it.
<br><br>

## My Home Router
Well, despite being the network address the home router has come in last on this list. Nmap scan came back as below:<br>
<p align="center"><img width="600" src="/assets/homenetwork/nmap_router.png"></p>
First off, yes I'm ashamed to admit that is telnet you're seeing. That was initially disabled actually and I then enabled it for a short while to test something out. Since that was stupidly left on, I turned it back off.<br><br>
Next comes a DNS service running over port 53, and frankly this holds little concern for me. I think I've manually set my DNS servers to be Google's or something similar, but at the same time I don't want to disable that service and end up breaking something on accident.<br><br>
Port 80 is of course the the web interface, and I'm not too concerned there. The only real issue I see would be brute forcing this login which will supposedly take billions of years to accomplish.<br><br>
Now for port 1723 - this one surprised me simply because I didn't know what it did. Looking at the service it was running "pptp" made me think Point-to-Point Tunneling Protocol, which actually makes sense since my router offers some in-built VPN features. I did some research into this and it turns out that the service is essentially obsolete - 3rd party VPN providers no longer use it, nor do Google or Apple due to security flaws. This was also as easy as finding the right setting, turning off that feature, and running another targeted nmap scan to ensure the service is disabled. So after disabling half the ports and services on my router, it would seem at least more secure than before all this.
<br><br>

## Conclusion
Well, is my network secure? There'a always more I could I suppose. If you wanted to get super involved I'm sure I could buy a subscription to some kind of IPS and firewall, but this is a home network. All of my end devices and network devices have some kind of AV installed that periodically runs, I use a VPN when browsing the web, firewall and internet options are stricter than the default, so I don't think there is much I can or should do at this point.
<br><br>
