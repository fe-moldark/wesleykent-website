---
layout: post
title:  TryHackMe - Simple CTF
date:   2022-04-03 00:00:00 -0600
categories: THM
intro: As the name indicates, this is a simple CTF but it's never bad to go back to the fundamentals.
--- 

# TryHackMe - Simple CTF

As the name indicates, this is a simple CTF but it's never bad to go back to the fundamentals. Let's begin with an nmap scan:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Simple-CTF/nmap.png"></p> 
We notice several open ports that answer the first couple questions for this box. We can enumerate port 80 further by running gobuster on it:<br>
<p align="center"><img width="800" src="/assets/blog/THM-Simple-CTF/gobuster.png"></p> 
This `/simple` directory leads us to a website for "CMS Made Simple", and a quick google search for known exploits will find us a workable exploit (CVE) plus information about it for questions 3, 4 and 5.
<br><br>
We can get its script from exploit-db:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Simple-CTF/exploitdb.png"></p> 
It is a .py file, and from examining the code we know to run it will require several flags/arguments/whatever you choose to call them, including `-u`, `-w` and `-c`:<br>
<p align="center"><img width="700" src="/assets/blog/THM-Simple-CTF/py.png"></p> 
Let's run this exploit now. Quick note, you may have to adjust some of the file, I had to in order to get it working with python3 as it is written in the older v2.7. And yes, below I ran the script as `python` and not explicitly `python3` but I think that's becoming more common where the new standard has finally transitioned into using v3 by default. Maybe it's just Parrot's OS, not sure, anyway that looks like the following: <br>
<p align="center"><img width="850" src="/assets/blog/THM-Simple-CTF/exploit.png"></p> 
It reveals the following information for us:<br>
<p align="center"><img width="600" src="/assets/blog/THM-Simple-CTF/pass.png"></p> 
And the password is it at the bottom there.
<br><br>
We can try to explicitly use these login credentials on the ssh login now, or try to find a login page on the website. Let's start with ssh:
<br><br>
And another learning moment: I initially tried to ssh on the default port, forgetting that ssh was running on port 2222 here, not 22. Let's try and login, although it is possible that the hydra brute force might have worked given enough time initially.<br>
<p align="center"><img width="800" src="/assets/blog/THM-Simple-CTF/ssh in.png"></p> 
It works, and we can get the `user.txt` from the working directory. We can find the other user to answer question 8 in the `/home` directory.
<br><br>
Again, we can elevate our privileges after leveraging a quick `sudo -l` and looking to gtfobins for a corresponding exploit. I went with option B which was vim from their site and got a working shell with root privileges. That leads to this:<br>
<p align="center"><img width="525" src="/assets/blog/THM-Simple-CTF/root.png"></p> 
And that is all for this box. Cheers,<br><br>
Wes


