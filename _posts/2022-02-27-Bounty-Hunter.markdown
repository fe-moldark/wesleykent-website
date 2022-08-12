---
layout: post
title:  TryHackMe - Bounty Hunter
date:   2022-02-27 00:00:00 -0600
categories: THM
intro: This CTF begins getting more interesting than previous ones, as it involves ftp, hydra, and gtfobins for the first time.
--- 

# TryHackMe - Bounty Hunter

This CTF begins getting more interesting than previous ones, as it involves ftp, hydra, and gtfobins for the first time. It is a relatively short CTF, so let's go ahead and jump into it with an nmap scan:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Bounty-Hunter/initial nmap.png"></p> 
After seeing the webpage, we can try to enumerate the webserver with gobuster:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Bounty-Hunter/failed gobuster.png"></p> 
However, this gives us nothing else, and visiting the actual webpage also does not provide anything useful.
<br><br>
There is still the anonymous ftp login, however. From the ftp login we can get several files that provide a potential password list to brute force as well as a potential username for ssh:<br>
<p align="center"><img width="550" src="/assets/blog/THM-Bounty-Hunter/ftp anonymous.png"></p> 
The possible username, `lin`, along with the password list completes a nice hydra brute force that looks as follows:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Bounty-Hunter/hydraandSSH.png"></p>
Once those credentials are found, we have our foothold and can locate the first flag:<br>
<p align="center"><img width="450" src="/assets/blog/THM-Bounty-Hunter/usertxt.png"></p> 
Now, we are not root, and do not have permissions to access the root folder on this machine. However, the useful `sudo -l` command does provide a path we might be able to use to escalate our privileges:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Bounty-Hunter/sudo-l.png"></p> 
Here we see that `/bin/tar` can run root commands for us as the `lin` user. To exploit this we can search on gtfobins for a tar exploit and I quickly found the following:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Bounty-Hunter/gtfobins.png"></p> 
Initially, I thought this exploit did not work because outright running this did not give a root shell. However all you have to do is add the `sudo` to the beginning since you are after all trying to run this as root. User error on my part...
<br><br>
After adding the `sudo` in front, we are able to get our root shell and cat the file at its location in the `/root` directory:<br>
<p align="center"><img width="850" src="/assets/blog/THM-Bounty-Hunter/running gtfo.png"></p>
Easy day. Cheers,<br><br>
Wes<br>
