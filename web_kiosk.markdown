---
layout: page
title: Raspberry Pi Web Kiosk
subtitle: Complete configuration for deployment in a production environment
description: Configuring a web kiosk for use in a production environment
permalink: /raspberrypi/web_kiosk/
---

# Introduction
Well, a work project led to needing some kind of web kiosk / "smart" monitor that would be in a production environment. Naturally I was partial to the Raspberry Pi route and they let me roll with it. I'll cover how to configure this from start to finish including some different ways for the kiosk to be managed as well as address several security concerns and their mitigations towards the end.
<br><br>

# Hardware
The simplest hardware set up for a RPi project yet - this only requires a Raspberry Pi board and a monitor. Technically the microSD card, power supply, and HDMI cable too, but whatever. I am using a Pi 3 Model B in addition to a generic Dell keyboard and monitor.
<br><br>

# Software
### Initial config
I'll be changing the usernames, IP addresses, etc for this but everything else remains the same in practice. Using the Raspberry Pi Imager flash the SD card with the most recent full desktop image. Some initial configurations with `sudo raspi-config`: enable SSH under `Interface options` and disable screen blanking under `Display Options > Screen Blanking > No`.
### Network config
Assign a hostname, yes, but more importantly assign a static IP. This more applies if you do not join your device to your domain since it won't work well with your local DNS server, that was my experience at least. A static IP outside of your dhcp scope is always a good practice. Do this by editing `/etc/network/interfaces` as follows:<br>
```bash
auto wlan0
iface wlan0 inet static
    address 192.168.1.146
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 192.168.1.2
```
_Note: I am using the wireless interface for this config, you can also use the built in `eth0`._<br><br>
Call a quick reboot and test if the IP address is being used and you are still connected to the network.
<br>
### Create user accounts
I created one with root permissions for myself, one for the kiosk service to run under, and one for other employees to manage/edit the website that the kiosk displays. And no, please do not use the default `pi` user as one of these...
<br><br>
You should already have your root account from the RPi Imager settings, so let's set up the last two accounts with `sudo adduser kiosk` ("kiosk" is the example username here). If their home directories are not made automatically, create them with `sudo mkdir /home/kiosk` and `sudo chown kiosk:kiosk /home/kiosk`. Set a password for the users with `sudo passwd kiosk`. Go through these same steps for the third user, for this example I will call them `editURL`. _Note:I also found it easier to add the "kiosk" user to the `sudo` group, and then remove them again at the end. Use `sudo usermod -aG sudo kiosk` if you want._
<br><br>
Create `url.txt` which we will use for the web kiosk under `kiosk`'s home directory with `nano /home/kiosk/url.txt`. Depending how this file will be accessed and edited, adjust ownership and permissions accordingly. For my setup this meant setting the permissions to 760 and changing the ownership to the `editURL` user.
<br>

### Updates (including long-term, consistent updates)
As you should always do, run a quick `sudo apt update && sudo apt -y upgrade && sudo apt -y autoremove`. This only happens once, however, so let's configure these updates to run every week, every month, or whatever you find best. Edit the crontab for your su with `crontab -e` and append something similar to: `0 2 * * 0 sudo apt update && sudo apt -y upgrade && sudo apt -y autoremove`. This runs at 2am every Sunday.<br>
_Note: in many cases you do NOT want to schedule automatic updates and upgrades to your devices since it may break something in production. For a simple web kiosk, however, there is little to worry about and this reduces time needed for management. Just keep a good backup image._
<br>

### Management of the Web Kiosk
In my situation the end goal is to have other users managing this kiosk themselves and that requires the ability for them to be able to edit the web page (or other media) being displayed. I configured this in three different ways, the first being more secure but not as user friendly and the latter being more user friendly but less secure.
<br><br>
##### Method 1: Configuring remote access and a custom shell
This is by far my favorite and the more secure option because of how their login shell works. For those that don't know you can customize a user's bash shell to something other than, well, a standard bash shell. What this looked like was creating the user and the following file `sudo nano /usr/local/bin/edit_only.sh` (and later making the file executable with `sudo chmod +x /usr/local/bin/edit_only.sh`). The contents of it should be the following:
```bash
#!/bin/bash
nano /home/kiosk/url.txt
```
Afterwards the user's profile still needs to be "assigned" this new shell which we can do with `sudo usermod -s /usr/local/bin/edit_only.sh editURL` (where `editURL` is the user).
<br><br>
In this example the `kiosk` user is hosting a file called `url.txt` in their home directory, and this bash script (login shell in this context) points directly to editing a single file with `nano`. If you try this out yourself you'll notice the second you login it pulls up the file to edit, and once you save and exit from there your session immediately ends and you are logged out of the system.
_Note: if the user is not already in the ssh group, add them, and ensure the right permissions are set for that bash file._
<br><br>
##### Method 2: Create a samba share that other users on the network can access
This is by far the most user friendly since it easily allows them to modify the url, upload images, point the url to them, and more. The "URL" can either be an actual web URL or be something like `file:\\\path\to\share\image.jpg` and it will open the local image, pdf, etc in the chrome browser, fullscreen. The only active management that may be needed from you is adjusting the screen's resolution/zoom as the media changes. To create the share we will need to execute the following:<br>
```bash
sudo apt install samba samba-common-bin
sudo mkdir -m 1770 /shared # (or whatever else you want to call this folder, and wherever you want it to be)
sudo nano /etc/samba/smb.conf
```
Where that last conf file contains:<br>
```
[RPiShare]
path = /shared
writeable = yes
browseable = yes
create mask = 0660
directory mask = 0660
public = no
```
I wouldn't change much about the permissions. Keep things read and writable, but w/out the executable bit. Brief note: create a file called `pointToUrl.txt` in that share! (I'll explain why later).
<br><br>
Assign a password for the smb login, which I kept the same as the `editURL` user mentioned previously. Restart the smb service with `sudo systemctl restart smbd` and try to navigate to the share from your Windows (or whatever) computer. Enter the username / password you configured and ensure you are able to edit and move files to the share.
<br><br>**Note: this took me 20 seconds to figure out, but the username you use there needs to start with "IPADDRESS\then_username". Just like logging into a local (non-domain) account on Windows and you need to use ".\username" you will need to include the IP address before the username to use that local login for authentication, else it defaults to your domain.**
<br><br>
##### Method 3: Configure the VNC server
This is a secure and very dynamic option, especially if you'll be displaying different types of content and want easy access to the desktop. This also allows you to entirely disable the USB ports since you'll be able to use a keyboard and mouse solely over VNC. There are plenty of tutorials on how to configure this that are already out there - I won't go over it here.
<br><br>
##### (Method 4: Just do it yourself)
This shouldn't really count, but you can always just not give anyone else access to the web kiosk and manage it yourself. It's more work for you and doesn't scale well, but if you're anything like me you are not very trusting anyway.
<br><br>

# Configuring the Kiosk service
### Initial config
You can use any combination of the three methods mentioned above as you want, but we still need to set up the kiosk service itself. This was entirely new to me, so I heavily referenced what is outlined <a href="https://raspberrypi-guide.github.io/filesharing/filesharing-raspberry-pi" target="_blank" rel="noopener noreferrer">here</a>. Let's start with the following commands:<br>
```bash
sudo apt purge wolfram-engine scratch nuscratch sonic-pi idle3 –y
sudo apt purge smartsim java-common libreoffice* -y
sudo apt clean
sudo apt autoremove
sudo apt install xdotool unclutter sed
```
<br>
Execute another `sudo raspi-config`, this time navigating to `System Options > Boot / Auto Login` and choose the Desktop autologin for the **KIOSK** user (reboot later). Also, if needed copy this folder to the `kiosk` user with: `sudo cp -R /home/<managementAccount>/.config/chromium/ /home/kiosk/.config/chromium/`
<br>
### Create the kiosk bash and service files
##### Bash file
While still logged in as the `kiosk` user create the following file with `nano /home/kiosk/kiosk.sh` and enter in the below info:
```bash
#!/bin/bash

xset s noblank
xset s off
xset –dpms

unclutter -idle 0.5 -root &
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/$USER/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/$USER/.config/chromium/Default/Preferences
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk $(cat /home/kiosk/url.txt)
```
You'll notice the url the kiosk is reading from the `/home/kiosk/url.txt` file we created earlier. Make it executable with `chmod +x /home/kiosk/kiosk.sh`.
<br><br>
##### Service file
_IMPORTANT: execute `echo $DISPLAY` using the device and monitor directly plugged into the device - ie, **NOT** over SSH._
<br><br>
Create the service file with `sudo nano /lib/systemd/system/kiosk.service` and copy in the below info:<br>
```
[Unit]
Description=Chromium Kiosk
Wants=graphical.target
After=graphical.target

[Service]
Environment=DISPLAY=:0.0
Environment=XAUTHORITY=/home/kiosk/.Xauthority
Type=simple
ExecStart=/bin/bash /home/kiosk/kiosk.sh
Restart=always
User=kiosk
Group=kiosk

[Install]
WantedBy=graphical.target
```
<br>
Replace `Environment=DISPLAY=:0.0` with the results of the echo command from before - my result was ":0", so I filled it in as you see above. Enable and start the service with `sudo systemctl enable kiosk.service`  then `sudo systemctl start kiosk.service`. If the bash script runs as expected, reboot the machine and ensure it starts automatically after the restart.
<br><br>

# Updating the website for the kiosk
Okay, so we have the file where the kiosk will read the url from and the kiosk itself has been set up, however, modifying that file will not actually change anything since the service was already loaded right after the initial boot process. To account for this I wrote a script that executes every minute (cronjob) as follows:<br>
```python
import os, sys, time
file='/shared/pointToUrl.txt'

if (int(time.time()) - int(os.stat(file).st_mtime) < 60): #file changed recently
    pointToUrl=open('/shared/pointToUrl.txt','r').read().split('\n')[0]
    savedUrl=open('/home/kiosk/url.txt','r').read().split('\n')[0]

    if pointToUrl!=savedUrl:
        os.system('cp /shared/pointToUrl.txt /home/kiosk/url.txt')
        time.sleep(2)
        os.system('sudo service kiosk stop')
        time.sleep(2)
        os.system('sudo service kiosk start')
```
Also, I know this looks weird with the `pointToUrl.txt` file being copied to `kiosk`'s home directory but the share takes longer to come online and there was an awkward pause between booting to the desktop and waiting for a simple text file to be registered. Hence the copy function, but it isn't needed as long as you put in a sleep function before starting the kiosk service.
<br><br>
While we are talking about cronjobs, I would also add a reboot function to your Pi for every so often, maybe once a month? Up to you.
<br><br>

# Addressing security concerns and their mitigations
I looked at this from two perspectives - physical and logical risks, which is maybe not the best way to phrase it, but you get the idea.
<br>

### Physical concerns
##### Ethernet
Disable the interface at boot using the `rc.local` file and adding the below command: `sudo ifconfig eth0 down`
<br><br>
##### Bluetooth
Not needed, so might as well reduce your attack surface with `sudo nano /boot/firmware/config.txt` (older versions have this at `/boot/config.txt`) and at the bottom add `dtoverlay=disable-bt`.
<br><br>
##### USB ports
Two scenarios:
- Disable _all_ USB ports if not needed by modifying the same `rc.local` file with `echo '1-1' | sudo tee /sys/bus/usb/drivers/usb/unbind`. This may or may not need to change, reference the `/sys/bus/usb/devices/` directory for the names of which root (idk if I'm using the right terminology here) device(s) should be disabled.
- Keep USB ports open, but white list which devices can connect. This is not a perfect solution - whitelisting never is, after all. It is more of a deterrent or hindrance similar to what MAC address filtering is. "Security through obscurity" and all that. What this does do is prevent anyone from sneakily plugging in just any malicious USB and walking away while it does its thing, but a more focused attack will be able to get around this measure. I'll discuss how this is covered in the section below.
<br>

### Logical concerns
##### Outdated software, OS, and services
Covered as best as can be expected under the weekly update and upgrade cronjob. Not much else is needed as far as I can tell.
<br><br>
##### Whitelisting USB devices
This turned more complicated since blocking devices that mount with a normal udev rule pointing towards the device's `authorized` file did not work. After many frustrated hours trying to get it to work, I wrote my own script that uses a device's `bind` and `unbin` functions. From a high level overview the script runs off a custom ruleset whenever _any_ new USB device is plugged in. The script contains a list of pre-approved (whitelisted) devices using its vendor and product IDs. I've uploaded the script <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/Zenith/USB_bind_unbind/unbindUSBs.py" target="_blank" rel="noopener noreferrer">here</a>. To implement this copy the script using `sudo curl https://raw.githubusercontent.com/fe-moldark/wesleykent-website/gh-pages/assets/Zenith/USB_bind_unbind/unbindUSBs.py > /usr/local/bin/unbindUSBs.py`, adjust permissions as needed keeping in mind that read permissions let's anyone know what to imitate to get past the whitelist. Make it executable as well. The two parts you will need to modify will be the `whiteListed` list (use `lsusb` to view the vendor and product IDs) and the list with the `['1-0:1.0','2-0:1.0','3-0:1.0','4-0:1.0','usb1','usb2','usb3','usb4']`. The latter of those are in the same directory as other devices but they are simply the "root" ports for the USBs, so they can stay open and then you'll see "sub" folders populate with every new plugged in USB device. I'm missing the right terminology here, but I'm 89% sure I'm right about this conceptually.
<br><br>
The rule itself should be saved to the `/etc/udev/rules.d/` directory as something like `00_myNewRule.rules` and contain `ACTION=="add", SUBSYSTEM=="usb", RUN+="/usr/bin/python3 /usr/local/bin/unbindUSBs.py"`. Once a new rule has been added or modified you will need to reset the rules using `sudo udevadmn control --reload-rules && sudo udevadm trigger`, then plug in a USB device and see if it gets triggered. Useful debug / troubleshooting tools will be `sudo udevadm test /path/to/rule.rules`.
<br><br>
##### Blocking certain 'escape' keys from the kiosk
Sounds simple, but it's Linux so… yeah, no. The tutorials I read through would not work even with hours of wasted time. But, I managed to find a combination of things that did what I wanted it to, which was to block the keys that can be used to escape the kiosk including the "start" key, ALT, CTRL and certain F1-F12 keys. The following packages are needed and installed with `sudo apt-get install xbindkeys && sudo apt-get install xmodmap`.
<br><br>
Now you need to identify which keycodes correspond to the keys you want to block. I won't give you my list since it'll probably change for you, but you can easily identify the keycodes using `evtest` (install if not already installed, I think with `sudo pip3 install evdev --break-system-packages` - again, I think). Once identified, execute the following (as the kiosk user): `xmodmap -pke > ~/.Xmodmap`. Now edit the file and map the keycodes you identified to `NoSymbol` instead of whatever it used to be. To keep these changes in affect after a reboot edit the `kiosk` user's `~.profile` to include:<br>
```
xbindkeys --file /home/kiosk/.xbindkeysrc

if [ -f ~/.Xmodmap ]; then
    xmodmap ~/.Xmodmap
    xmodmap -e "clear control"
    xmodmap -e "clear mod1"
    fi
```
<br>
Now, limiting the ALT and CTRL keys with just `xmodmap` was still finicky - in other words it didn't work as it should have so I needed to use the `xbindkeys` line you see there (**before** `xmodmap`). We will make that file using `xbindkeys --defaults > /home/kiosk/.xbindkeysrc` then edit the file and add in:<br>
```
"xte 'key F1'"
    F1
```
<br>
Do I know what exactly this does and how it works? Ha, no, no I don't. I do know it works, however, and the F1 key that would normally open Chrome's help page no longer works, so I'm a happy man.
<br><br>

# Clean up
As mentioned way back in the beginning, remove the `kiosk` user from the `sudo` group with `sudo deluser kiosk sudo`.
<br><br>

# Conclusion
Hopefully this worked for you without issue, but I'd be willing to bet it didn't right off the bat. It'll take some tweaking on your end before it gets up and running. Best of luck to you.
<br><br>
