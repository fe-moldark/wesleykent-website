---
layout: post
title:  TryHackMe - Pickle Rick
date:   2022-03-13 00:00:00 -0600
categories: THM
intro: This was a genuinely enjoyable CTF to work through, there are a number of different skills that you will need to call on to exploit this. The theme is also amusing for those Rick & Morty fans out there, but let's go ahead and dive into it.
--- 

# TryHackMe - Pickle Rick

This was a genuinely enjoyable CTF to work through, there are a number of different skills that you will need to call on to exploit this. The theme is also amusing for those Rick & Morty fans out there, but let's go ahead and dive into it.<br><br>
Let's run our initial nmap scan against our target:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Pickle-Rick/nmap.png"></p> 
Checking out the webpage, I saw from the source code that they did not clean up their code very well:<br>
<p align="center"><img width="650" src="/assets/blog/THM-Pickle-Rick/username.png"></p> 
We'll use this later. Now, since this is running a web server after all let's run gobuster / dirb on it in the background as we keep enumerating the different ports:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Pickle-Rick/gobuster.png"></p> 
This `/assets` page won't reveal anything useful unfortunately.
<br><br>
We do, however, have a username and an open ssh port. Trying to run hydra against it does not work as it is blocked from remote login, so we know we will have to use that username elsewhere.
<br><br>
Now from the nmap / gobuster scans we know that there is a `login.php` portal on the website:<br>
<p align="center"><img width="550" src="/assets/blog/THM-Pickle-Rick/loginphp.png"></p> 
Now we can try and use hydra to brute force this page, however we will need certain information about the login forum which we can get from burpsuite:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Pickle-Rick/burp.png"></p> 
Now that we have the request, let's run hydra using the information from line 22:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Pickle-Rick/hydra.png"></p> 
While this runs in the background, let's see what more we can discover about the web server using gobuster:<br>
<p align="center"><img width="750" src="/assets/blog/THM-Pickle-Rick/flag1.png"></p> 
From the rest of these results we can navigate to view these pages and we get a password on the right side of the above image. Let's try to login into the .php portal now. This user/pass combination works, meaning we can stop our hydra attack, and we are forwarded to the below page:<br>
<p align="center"><img width="650" src="/assets/blog/THM-Pickle-Rick/command panel.png"></p> 
We can run a variety of commands, for example `whoami` and `ls`, but we are restricted from certain functions such as `cat somefile.ext`. Below we can see the results of the `ls` command:<br>
<p align="center"><img width="500" src="/assets/blog/THM-Pickle-Rick/ls.png"></p> 
Although we can't `cat` the "super secret" file, we can view it in the web browser (as a page), and there we will get our first flag.
<br><br>
We can also see which (if any) python is installed via the command panel, which it is:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Pickle-Rick/which python.png"></p> 
Pentestmonkey is another great source of information alongside gtfobins, and we can use it to research how to try and start a reverse shell. We can get this shell up and running by establishing a netcat listener on our local machine and using the exploit from pentestmonkey (after modifying it of course):<br>
<p align="center"><img width="850" src="/assets/blog/THM-Pickle-Rick/netcat.png"></p> 
*It's worth noting that if you have an a distribution like Parrot OS (which I am running) they might come installed with several default payloads and other common pentesting tools. 
<br><br>
Regardless, once this netcat listener gets activated we can find a user "rick" in the `/home` directory, and within that the second flag:<br>
<p align="center"><img width="600" src="/assets/blog/THM-Pickle-Rick/second flag.png"></p> 
It is a safe bet to assume the last flag will be found in the root folder, which we currently don't have access to. We can see what we do have access to with root permissions with `sudo -l`:<br>
<p align="center"><img width="750" src="/assets/blog/THM-Pickle-Rick/sudo l.png"></p> 
We can navigate to this directory and start a shell with root permissions:<br>
<p align="center"><img width="600" src="/assets/blog/THM-Pickle-Rick/final.png"></p> 
From there we can navigate to the `/root` folder. Inside we will find the last flag / "ingredient" for this box:<br>
<p align="center"><img width="650" src="/assets/blog/THM-Pickle-Rick/root txt.png"></p> 
And that is all for this box. Cheers,<br><br>
Wes<br>

