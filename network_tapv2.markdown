---
layout: page
title: Designing a Network Tap w/ a RPi4 (version 2)
subtitle: With ways to log traffic to an on-board USB drive or output to a USB/ethernet adapter, and access the captured pcap files remotely
description: 
permalink: /network_intrusion/network_tapv2/
---

<head>
  <link rel="stylesheet" type="text/css" href="/styles/embedded_videos_and_stls.css">
</head>


# Introduction
This is an updated version of the previous network tap, better in multiple ways and with a proper case this time around. Name basically says it all, but here is some more information on how this works. It runs in three different modes, controlled by a 'cycle mode' button on the outside of the case.
- Mode 1: Network tap that copies traffic to the connected usb drive
- Mode 2: Network tap that functions more as a port mirror by copying all traffic of the bridged interface to a second USB/ethernet adapter, which you can then capture using tcpdump, Wireshark, etc
- Mode 3: Essentially turns the device into an IP phone. The eth0 interface can receive a dhcp address (assuming a dhcp server is running on the network) and the bridged interface from eth0>eth1 stays open, allowing a second device to connect to the network with its own IP address (sorta like a mini-switch)
<br>

The device can be managed via a serial connection over a micro USB port or an adhoc network running on the built-in wlan0 interface.
<br><br>

# Video of the Network tap in action
This just showcases how it works in practice, and is arguably more enjoyable to watch than it is to read through all the technical stuff below...
<center>
  <iframe id="content" src="https://www.youtube.com/embed/anbbQ4CnhXM?si=aWbbG1CK-L0_J7OD" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe><br>
</center>
<br>

# Hardware used
- 1x <a href="https://www.adafruit.com/product/4296" target="_blank" rel="noopener noreferrer">RPi 4 Model B w/ 4GB RAM</a>
- 1x <a href="https://amazon.com/gp/product/B07XB5PR9J" target="_blank" rel="noopener noreferrer">LoveRPi PoE HAT</a>
- 2x <a href="https://amazon.com/gp/product/B09Q5XC7T9" target="_blank" rel="noopener noreferrer">USB to ethernet adapters</a>
- 1x <a href="https://www.adafruit.com/product/3527" target="_blank" rel="noopener noreferrer">128x32 Monochrome OLED</a>
- 2x <a href="https://www.adafruit.com/product/4183" target="_blank" rel="noopener noreferrer">Buttons</a>
- 1x USB to TTL adapter (e.g. the YP-01 model, but others work too)
- 1x USB drive (formatted in ext4, and the more storage the better)
- 1x SD card for the OS
- USB breakout components - 2x male and female USB Type A, 1x female Micro USB
- Wires, solder, perf boards, screws, etc.
<br><br>

# Circuit Diagram / Wiring
*GPIO pins 14/15 connect out to a USB/TTL adapter for an additional management option. Not necessary, but certainly useful.
<center>
  <img src="/assets/3d_files/ntap//ntap_circuitdiagram.png" alt="" width=950><br>
</center>
<br><br>

# 3D model / case I designed
File is also available for download in its MCX format <a href="https://github.com/fe-moldark/wesleykent-website/raw/refs/heads/gh-pages/assets/3d_files/ntap/ntap_full.mcx" target="_blank" rel="noopener noreferrer">here</a>.
<br>
<center>
  <div id="content">
    <iframe id="content" title="RPi4 Network Tap Case" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/094abbf72c08406aa5cb040c4519215e/embed"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/rpi4-network-tap-case-094abbf72c08406aa5cb040c4519215e?utm_medium=embed&utm_campaign=share-popup&utm_content=094abbf72c08406aa5cb040c4519215e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> RPi4 Network Tap Case </a> by <a href="https://sketchfab.com/femoldark?utm_medium=embed&utm_campaign=share-popup&utm_content=094abbf72c08406aa5cb040c4519215e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> femoldark </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=094abbf72c08406aa5cb040c4519215e" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p>
  </div>
</center>
<br><br>


# Configuration
## Basics
Install the headless Raspberry Pi OS and set up a user called `ntap`. Update and install some packages:<br>
```bash
sudo apt-get update &&
sudo apt-get upgrade -y &&
sudo apt install iptables -y &&
sudo apt install bridge-utils &&
sudo apt install iw dnsmasq hostapd -y &&
sudo apt install tcpdump &&

sudo apt install python3-pip -y &&
sudo pip3 install adafruit-circuitpython-ssd1306 --break-system-packages &&
sudo apt-get install python3-pip -y &&
sudo apt-get install python3-pil -y &&
sudo apt install -y i2c-tools
```
<br>
Go into `raspi-config` and enable SSH, I2C, and Serial. Create the following:<br>
`sudo mkdir /mnt/usb_dev1/ && touch /home/ntap/log.log && sudo chown ntap:ntap /home/ntap/log.log`
<br><br>

## Crontab
Edit the crontab with `crontab -e` and add the following entries:
```bash
# Script that will mount the USB device correctly, then start the python script for the oled
# which also controls the "network tap" functions
@reboot /bin/bash /home/ntap/mountUSB_and_startNTap.sh >> /home/ntap/log.log 2&>1

# Configure a consistent baud rate for the serial connection
@reboot stty -F /dev/serial0 115200
```
That baud rate setting for `/dev/serial0` is needed because it was acting really weird, practically every time it booted up it would select a random (but still valid) baud rate. Not a clue where it was pulling that from, so the cronjob sets it manually at boot.
<br><br>

## Adhoc network stuff
Edit the file at `/etc/dnsmasq.conf` to be:<br>
```bash
interface=wlan0
dhcp-range=169.254.1.2,169.254.255.254,255.255.0.0,24h
```
Then `sudo systemctl enable dnsmasq`.
<br><br>
Keeping in mind you should choose your own password and ssid, edit the file at `/etc/hostapd/hostapd.conf` to be:<br>
```bash
interface=wlan0
driver=nl80211
ssid=ntap_adhoc
hw_mode=g
channel=1
auth_algs=1
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_passphrase=somethingcomplexthatyouchoose
wpa_pairwise=CCMP
wpa_group_rekey=600
ieee80211n=1
wmm_enabled=0
country_code=US
```
And `/etc/default/hostapd` should have one line at the bottom that points to this conf file we just created:
```bash
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```
Finally, execute:<br>
```bash
sudo systemctl unmask hostapd &&
sudo systemctl enable hostapd &&
sudo systemctl start hostapd
```
<br>
<br>
## Network interfaces
Config the file at `/etc/network/interfaces.d/wlan0` to be:<br>
```bash
allow-hotplug wlan0
iface wlan0 inet manual
```
Now you will need to create two different files, one configured for dhcp and one for bridged mode. Create `/etc/network/interfaces.dhcp` to be:<br>
```bash
source /etc/network.interfaces.d/*

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp
```
And `/etc/network/interfaces.bridged` to be
```bash
source /etc/network.interfaces.d/*

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet manual

auto eth1
iface eth1 inet manual

auto br0
iface br0 inet manual
  bridge_ports eth0 eth1
```
Now, execute a one time copy of `sudo cp /etc/network/interfaces.dhcp /etc/network/interfaces`.

<br><br>

## Install the scripts I wrote
Every file listed in <a href="https://github.com/fe-moldark/wesleykent-website/tree/gh-pages/assets/ntap" target="_blank" rel="noopener noreferrer">this folder</a> should be downloaded and saved to the `/home/ntap/` directory, and made executable with `chmod +x <filename>`. These control the LCD, start the adhoc network, conduct the initial load of the USB media, and configure the mirrored bridged interface when in mode 2.
<br>

You can play around with those files as you want, they do make some assumptions about your system like where the USB media loads to by default (/dev/sda1) and the filters that are applied to the tcpdump capture, so you'll likely want to adjust them. They should be relatively straight-forward to understand. Also keep in mind that the receiving interface when in mode 2 will need to be set to promiscuous mode to work properly. Otherwise you'll just see stuff like ARP traffic.
<br><br>

# Random thoughts
- If you are planning on _keeping_ the second usb/ethernet adapter plugged in for mode 2, look into configuring a udev rule to ensure it is assigned the correct interface name (`eth2`). I didn't consider this on a reboot of the Pi and suddenly my port mirroring was all messed up, turns out the adapters had loaded in backwards that time around and `eth1` was `eth2`, and `eth2` was `eth1`. Bah.
- Unfortunately my internet speeds and the 10/100 ethernet adapter I used didn't allow me to do any real stress tests on the device, but let me know how it handles Gigabyte speeds if you ever try it out. It was handling ~70 Mbps down w/out stressing out system resources, _or_ slowing download speeds by more than 1-3% compared to a direct connection to the network.
- You can modify what information the OLED displays, I just chose what I thought would be most useful but it can really be anything you want. Same goes for the mode - if you want to boot into a different default mode for the network tap, modify the `mode` variable in the `main.py` file.
<br>

# Conclusion
Well, that's all folks. A simple enough network tap that's a lot cheaper than anything you can buy online. Great for monitoring any unencrypted traffic like telnet, http, etc. Any questions feel free to reach out and I'll get back to you when I can.
<br><br>
