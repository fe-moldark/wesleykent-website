---
layout: page
title: Fresh Linux Install
subtitle: If you're brand new to this or just looking for a blank slate to start with, I offer you this
image: /home/wesleyvm1/WesleyKentBlog/assets/fe.ico
description: Useful notes for commands and common exploit tools, methods that have proven useful
permalink: /resources/freshinstall/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

# My Recommended Fresh Linux Install
<br>
<br>
**My choice for virtualization:** [VMware](https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html)
<br>
<br>
**My favorite linux distribution:** [ParrotOS](https://www.parrotsec.org/download/)
<br>
<br>
Below is an ongoing text file I keep in the event my Virtual Machine decides it no longer has the will to live and I have to rebuild from stratch. Also, if I decide I want to use another distribution but want to keep the same tools. All that being said, I would recommend the following commands / installs to get your machine ready to go. There are a number of tools for steganography, default password lists from SecLists, John for password cracking, etc. Enjoy.
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
install enum4linux
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
