---
layout: post
title:  TryHackMe - Break Out The Cage
date:   2022-06-11 00:00:00 -0600
categories: THM
intro: Wherever you fall on the "Nick Cage being a great actor" scale, this is an amusing CTF to work through. Besides, Community has already tried to answer that question I think.
--- 

# TryHackMe - Break Out The Cage

Wherever you fall on the "Nick Cage being a great actor" scale, this is an amusing CTF to work through. Besides, "Community" has already tried to answer that question I think.
<br><br>
For this challenge we are looking for an initial login for a user "Weston", and ultimately looking for the user and root flags. Beginning with an initial nmap scan:<br>
<p align="center"><img width="800" src="/assets/blog/THM-BreakOutTheCage/initial nmap.png"></p> 
3 ports are open to us - ftp (with anonymous logon), ssh on port 22, and a web page on port 80. To begin I started an initial gobuster scan in the background:<br>
<p align="center"><img width="800" src="/assets/blog/THM-BreakOutTheCage/useless dirb.png"></p> 
Now this didn't end up providing anything in the end since I found another way to access the machine but it's still good practice. Moving on to what we know we have access to via ftp:<br>
<p align="center"><img width="800" src="/assets/blog/THM-BreakOutTheCage/ftp anonymous.png"></p> 
This `dad_tasks` file we can access is encrypted in a way that didn't immediately jump out at me, thankfully we have the internet. Using an online tool it determined it was likely encoded using Base64:<br>
<p align="center"><img width="750" src="/assets/blog/THM-BreakOutTheCage/find out base64.png"></p> 
Decoding with Base64 however doesn't giving us the true form of the note since it is encrypted with yet another cipher. We can again identify the type, Vigenere, and use an online tool to break the cipher for us:<br>
<p align="center"><img width="700" src="/assets/blog/THM-BreakOutTheCage/solved vigenere cipher.png"></p> 
This will give us Weston's password to gain our initial foothold on the machine. It's worth noting I was running a hydra brute force attack against Weston on port 22, but safe to say it would never have cracked it. We can now log in:<br>
<p align="center"><img width="800" src="/assets/blog/THM-BreakOutTheCage/use cipher pw to login on ssh.png"></p> 
Since we can't access anything from Cage's home folder, I ran a quick `sudo -l` command as Weston:<br>
<p align="center"><img width="800" src="/assets/blog/THM-BreakOutTheCage/sudo dash l can edit.png"></p> 
This didn't end up helping too much as I recall. However, after being on the machine for a couple of minutes we get a broadcast message:<br>
<p align="center"><img width="700" src="/assets/blog/THM-BreakOutTheCage/broadcast message.png"></p> 
This indicates that likely a cronjob or something similar is running on the machine and spitting out these random lines. After identifying the file that is being run, we find out very quickly that it cannot be edited or modified with our current privileges:<br>
<p align="center"><img width="600" src="/assets/blog/THM-BreakOutTheCage/cant edit file with vim.png"></p> 
Also, annoyingly only vim is available on the device and not nano. Even though we cannot edit the file directly, we can affect the source of the quotes that the broadcast program draws from. Ultimately, we will probably want to start a reverse shell at some point, so let's reference pentestmonkey for an example:<br>
<p align="center"><img width="800" src="/assets/blog/THM-BreakOutTheCage/pentest monkey bash how to reverse shell.png"></p> 
After editing the IP / port to our liking, we can create a simple bash script to run the above command in the `/tmp` folder since we know we have write permissions there. Then, we can overwrite the quotes file while keeping an initial line for the broadcast message to print, and the second being the location of our custom reverse shell script. On our local machine we start the netcat listener and when the broadcast message next executes (should be within a couple of minutes) you should receive that shell.<br>
<p align="center"><img width="700" src="/assets/blog/THM-BreakOutTheCage/secondflag from lsitnener.png"></p> 
As seen above, the user flag is found in Cage's home directory. In that same directory we find a folder with email backups that contains what can only be assumed to be a password that we can again identify as also being encrypted with the vigenere cipher. Unfortunately, we can't crack it at face value but upon reading through the emails you can very easily find a keyword that is explicitly brought up numerous times, sometimes even in capital letters. They really toss you a bone on this part.<br>
<p align="center"><img width="600" src="/assets/blog/THM-BreakOutTheCage/get root pw.png"></p> 
This will give us the root password, and we can switch users over to them. <br>
<p align="center"><img width="700" src="/assets/blog/THM-BreakOutTheCage/find a way to switch to root user.png"></p> 
As you can see I had to call a better shell real quick before being able to switch to the root user.
<br><br>
From there we can access the root directory and find the final flag.<br>
<p align="center"><img width="800" src="/assets/blog/THM-BreakOutTheCage/and final root flag.png"></p> 
And the box has been pwned. Cheers,<br><br>
Wes<br>




