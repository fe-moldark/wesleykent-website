---
layout: page
title: Configuring a DIY Network Tap w/ a RPi
subtitle: With ways to log traffic to an on-board USB drive or output to an USB-ethernet adapter, and access captured packets remotely
description: 
permalink: /network_intrusion/network_tap/
---

# Introduction
I was working on a personal project that required a network tap of sorts. Now, proper ones cost too much for my pride to let me purchase outright, so I designed my own active, PoE powered Network Tap using a Raspberry Pi 4, a PoE+ hat, one or two USB ethernet adapters, and a USB stick. Total cost for me comes out to under $100, and given the hardware I already had it was much less than that. It's about a half or third the price of ones you can buy online, which is not to say mine is as good, but certainly cheaper.
<br><br>


# Hardware used
- 1x RPi 4 Model B w/ 4/8G RAM
- 1x PoE hat (e.g. the LoveRPi model)
- 1x or 2x USB to ethernet adapter (depending on your configuration)
- 1x USB storage at least 128GB in size (or not at all if using 2x USB to ethernet adapters)
- 1x SD card for the OS


# Configuration
## Basics
Update and install some packages:<br>
```
sudo apt-get update &&
sudo apt-get upgrade -y &&
sudo apt install iptables -y &&
sudo apt install bridge-utils &&
sudo apt install tcpdump
```

## Network interfaces
Config the `/etc/network/interfaces` file as follows:<br>
```bash
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet manual

auto eth1
iface eth1 inet manual

auto br0
iface br0 inet manual
    bridge_ports eth0 eth1


auto wlan0
iface wlan0 inet static
    wpa-ssid "NetworkSSID"
    wpa-psk "stillNotGivingYouMyPassword"
    address 192.168.11.33
    netmask 255.255.255.0
    gateway 192.168.11.1
    dns-nameservers 8.8.8.8 8.8.4.4
```
<br>
Another configuration I also played around with was using the `wlan0` interface as an ad hoc network that you could remotely connect to and download the pcap files from. I cover how to do that on [this page](/network_intrusion/rpi_packetsniffer/') somewhere if you're interested in that alternative. The only downside is that you need to be close enough to the device to be able to connect, and the scenario I was working in I already knew the network's password which made accessing the files a lot quicker over ssh / scp.
<br>

## Storing the captured network data
The two logging scenarios for the pcap files are to save to a USB drive or mirror the traffic to a second USB to ethernet adapter which would then plug in to a secondary device. The former scenario is better for a quick install and walk away, while the second is better if you want to be actively monitoring the traffic in e.g. Wireshark. The latter also provides much more storage capacity, which might be an important factor depending on how long you want the network tap to be active and the volume of traffic.
<br>

### Scenario 1: A USB device
Identify the device with `sudo fdisk -l`, which for me was at `/dev/sda1`. From there, create a mount point for it using `sudo mkdir /mnt/usb_dev1` and because I didn't care much for security here adjust the permissions with `sudo chmod -R pi:pi /mnt/usb_dev1/`.
<br><br>
Next, we need a startup script to mount the usb device and begin the file capture. I wrote the following to `/home/pi/startup.sh`:<br>
```bash
#!/bin/bash

echo "Script started at $(date)" >> /home/pi/youHadBetterHaveAGoodReasonForAnError.log

sudo mount -t exfat -o uid=1000,gid=1000,dmask=0000,fmask=0000 /dev/sda1 /mnt/usb_dev1
sleep 2
sudo chown -R pi:pi /mnt/usb_dev1/


# Set the base directory for the USB stick and the base filename
MOUNT_DIR="/mnt/usb_dev1"
BASE_FILENAME="capture"
EXTENSION=".pcap"

# Find the next available filename
FILENAME="${MOUNT_DIR}/${BASE_FILENAME}"
COUNTER=1
while [ -e "${FILENAME}_${COUNTER}${EXTENSION}" ]; do
    ((COUNTER++))
done

FINAL_FILENAME="${FILENAME}_${COUNTER}${EXTENSION}"

echo "Filename: ${FINAL_FILENAME}" >> /home/pi/youHadBetterHaveAGoodReasonForAnError.log

# Run tcpdump with the filter
sudo tcpdump -i br0 'not icmp and not arp and not ether broadcast and not ether multicast' -C 500 -w "${FINAL_FILENAME}"

echo "Script ended at $(date)" >> /home/pi/youHadBetterHaveAGoodReasonForAnError.log
```
<br>
A couple of notes from this script are the flags used in the `sudo mount [...]` and the `sudo tcpdump [...]` commands. The former may need to change for you based on your default user's UID and GID if not using `pi`, and the file system format on your device might not be exfat, so make those changes as needed. The actual capture of the bridged interface `br0` is omitting some protocols I did not care for and that will just eat up storage space, but you can mess around with that as well as adjust the file size of the pcap limits (using `-C`). Finally, in order to load this at the Pi's startup we will add the following entry to the crontab with `crontab -e`:
<br>
```bash
@reboot sleep 60 && sudo /home/pi/startup.sh >> /home/pi/youHadBetterHaveAGoodReasonForAnError.log 2>&1
```
<br>
The sleep function is needed for all of the interfaces to be brought online, the USB device to load in, etc. Also, a quick note on the USB device itself - the file system needs to work with linux, so I'd recommend something like ext4, especially for a larger storage capacity. If you're on Windows I'll typically do this via `cmd > diskpart > list disk > select disk x > clean > create partition primary > format fs=exfat quick`.
<br>

### Scenario 2: Output to a second USB to ethernet adapter
In this scenario you don't want to bridge the `br0` interface with `eth2`, instead you simply want a one way copy from `br0` > `eth2`. To do this I used `tc`:<br>
```bash
sudo tc qdisc add dev br0 ingress
sudo tc filter add dev br0 parent ffff: \
    protocol all \
    u32 match u8 0 0 \
    action mirred egress mirror dev eth2
```
<br>
I also needed to set the `eth2` interface to promiscuous mode using `sudo ip link set dev eth2 promisc on`. A final note on using this method is that the receiving interface (i.e. the one getting data from `eth2`) needs to be able to be set to promiscuous mode on its end as well. This is simple enough with another Linux-based device and using Wireshark/tcpdump, but if you're running Windows it'll likely not let you manipulate that interface without jumping through a few more hurdles.
<br>

# Conclusion
Well, that's all folks. A simple enough network tap that's a lot cheaper than anything you can buy online. Great for monitoring any unencrypted traffic like telnet, http, etc. Any questions feel free to reach out and I'll get back to you when I can.
<br><br>
