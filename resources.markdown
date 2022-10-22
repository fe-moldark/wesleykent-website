---
layout: page
title: Resources
subtitle: Useful stuff for CTFs with TryHackMe and my recommended Linux Distribution
image: /assets/fe.ico
description: Useful Links for CTFs with TryHackMe, HackTheBox and my favorite Linux Distribution
permalink: /tipsandtricks/resources/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

# Introduction
To start off, the CTFs I enjoy working through can be found at [TryHackMe](https://www.tryhackme.com) and [HackTheBox](https://www.hackthebox.com/).
<br>
For a massive of list of tried and true methods of bypassing misconfigured system, I give you: [gtfobins](https://gtfobins.github.io/)
<br>
For everything to do with exploiting command execution vulnerabilities: [pentestmonkey](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
<br><br>
# My Recommended Linux Distro and Installs
My choice for virtualization: [VMware](https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html)
<br>
My favorite linux distribution: [ParrotOS](https://www.parrotsec.org/download/)
<br><br>
In addition to the above links, below is an ongoing text file I keep in the event my Virtual Machine decides it no longer has the will to live and I have to rebuild from stratch. Also, if I decide I want to use another distribution but want to keep the same tools. All that being said, I would recommend the following commands / installs to get your machine ready to go. These include a number of tools for steganography, default password lists from SecLists, John for password cracking, basically just a good buff to ParrotOS if you are starting fresh.
<br>
<br>

```
sudo parrot-upgrade

sudo apt update -y && sudo apt upgrade -y
sudo apt full-upgrade
sudo apt install openvpn
sudo apt install stegosuite
sudo apt install steghide

sudo apt install build-essential libssl-dev yasm libgmp-dev libpcap-dev libnss3-dev libkrb5-dev pkg-config
wget https://github.com/openwall/john/archive/bleeding-jumbo.zip
unzip bleeding-jumbo.zip
rm bleeding-jumbo.zip
cd john-bleeding-jumbo/src/
./configure && make

sudo apt install john
sudo apt install yara

sudo apt-get install ftp
sudo apt-get install exploitdb

sudo apt-get install cifs-utils
sudo apt-get install nfs-common

sudo apt install default-mysql-client
sudo apt install enum4linux
pip install 2to3

wget -c https://github.com/danielmiessler/SecLists/archive/master.zip -O SecList.zip \
&& unzip SecList.zip \
&& rm -f SecList.zip

```
<br>
<br>
If you want to go the Kali Linux route or with another virtualization software, go for it. All I can say is that I've had good experiences with this combination thus far, so-
<br>
<br>
<img src="/assets/palps.png" alt="">
<!-- img src: https://imgflip.com/memetemplate/304517785/Star-Wars-Palpatine-Use-my-knowledge-I-beg-you--->
