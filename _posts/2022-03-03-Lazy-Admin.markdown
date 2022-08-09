---
layout: post
title:  TryHackMe - Lazy Admin
date:   2022-03-03 00:00:00 -0600
categories: THM
intro: This is an interesting CTF that involves some hash-cracking, web portals and creating some useful reverse shells running as ads on their website.
--- 

# TryHackMe - Lazy Admin

This CTF has two flags to find, let's get into it with the most basic nmap scan available (honestly no idea why I didn't include the `-sC -sV` flags here, I must've been tired):<br>
<p align="center"><img width="600" src="/assets/blog/THM-Lazy-Admin/nmap.png"></p> 
Since this is running an open port 80 and we can open it in a browser, let's try to enumerate some more directories and pages:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Lazy-Admin/gobuster.png"></p> 
There we discover the `/content` folder, which we can also run against our wordlist as well:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Lazy-Admin/gobusterII.png"></p> 
This gives us a number of paths that we can investigate, and after a lot of searching I discovered a couple of interesting things, the most obvious being a login forum at `/as`:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Lazy-Admin/slash as.png"></p> 
Now, knowing this CTF is titled "Lazy Admin", I am going to assume that this admin is using poor usernames/passwords, or default ones. As such, I looked at the get request through burpsuite for the username/password input names and attempted to brute force a password for an 'admin' and other similar usernames with hydra. Unfortunately, since I was just guessing the username nothing came of it, but it was worth a try since I just let it run in the background.
<br><br>
Moving on, in the `/inc` subfolder we do find an old mysql backup file, which are always good to find. Inside that we find some useful text, including the username and what appears to be a hashed password.<br>
<p align="center"><img width="700" src="/assets/blog/THM-Lazy-Admin/passwd.png"></p> 
Now that we have found some kind of hashed password (in the above screenshot), we can try to crack it with John after identifying the hash type:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Lazy-Admin/hashidentifier.png"></p> 
Now that we have the hash type, let's run John against it:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Lazy-Admin/gottenpw.png"></p> 
And we supposedly have a working user/pass, and trying to login on the `/as` site works. Also, from the backup sql file I now know that the username is actually 'manager', not the 'admin' I had previously guessed. Still a Lazy Admin choice, however, but moving on here is what we are greeted with after logging in:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Lazy-Admin/access.png"></p> 
Now, after navigating around a bit there is a place where we can add an "ad", which for me really meant I can just upload some custom code which may or may not accidentally start some kind of reverse shell.
<br><br>
Again, a site that will prove very useful in these kinds of situations is pentestmonkey. After a quick ad upload test, we see the add runs as a php file, so let's search pentestmonkey for an exploit that will work as that. The first option on there seems good enough, so let's modify the script to our machine and set up a netcat listener.<br>
<p align="center"><img width="700" src="/assets/blog/THM-Lazy-Admin/ad shell.png"></p> 
From there, navigate to the site or curl the URL, whatever you want and our netcat listener should start a shell:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Lazy-Admin/got shell.png"></p> 
It is simple enough to find the user flag, no different than any other box on THM. Now we do not have root access, but there is a way to get it with a quick `sudo -l` search:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Lazy-Admin/sudo l.png"></p> 
We cannot edit this perl script directly, but we see that it runs a bash script, which we can check out. The "copy" script starts its own shell, all we have to do is edit in our own address and again another port with another listener to start a root shell for ourselves this time:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Lazy-Admin/get root.png"></p> 
Once that happens, we'll get a root shell in our other window and can easily get the root flag from there:<br>
<p align="center"><img width="550" src="/assets/blog/THM-Lazy-Admin/root.png"></p> 
And that is all for this box. Cheers,<br><br>
Wes<br>



