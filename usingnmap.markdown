---
layout: page
title: Using Nmap
subtitle: Brief overview of Nmap, flags to be aware of, and running specific scripts
image: /home/wesleyvm1/WesleyKentBlog/assets/fe.ico
description: Brief overview of Nmap, flags to be aware of, and running specific scripts
permalink: /tipsandtricks/usingnmap/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

## Introduction and flags
If you are not already aware, nmap is an open-source port scanning tool used for security testing and "network exploration" as they call it.<br>
This will be a brief overview of my basic go-to scan, and after that is done I will explain how I often modify it based on the results:<br>
*Running as sudo<br>
`nmap -sC -sV -O <Target IP>`<br>
Depending on the results from this scan, you might need to disable host discovery with `-Pn`, you should run a longer follow up scan with `-p-`, you might want to target certain scripts at specific ports / services, or you might want to include more flags for a wider range of results.
<br><br>
Using the `-sU` or `-sS` you can specifiy a UDP or SYN scan.<br>
The `-O` tries to detect the Operating System type and version.<br>
Nmap defaults to scanning the top 1000 / 1024 ports, so it's best practice to run the longer scan with `-p-` as a flag to run through all 65,535 of them. Alternatively, you can target a single (or multiple) port(s) with `-p <#>,<#>` and so on. <br>
The `-sC` will run the default scripts (always a good option).<br>
The `-sV` will examine the open ports it finds for services / versions running on them.<br>
<br><br>
## Running specific scripts on ports
Say you want to run specific scripts against a single port:<br>
- First locate where your scripts are installed with nmap. If it is somewhere other than `/usr/share/nmap/scripts`, search for it with:<br>
`find / -name scripts -type d 2>/dev/null | grep nmap`<br>
From there, you can manually look thorugh or use grep to find scripts that you would like to run - for instance it looks like nmap includes at least 6 different scripts you can try running against ports running ssh.<br><br>
- From there, let's say you chose a specific script, e.g. the `ssh-brute.nse` script, against an open ssh service over port 22:<br>
`nmap --script=ssh-brute.nse -p 22 10.10.40.182`<br>
<br><br>

## Other
Again, much more that can be said here. You can increase the verbosity, use tools to evade firewalls / IDS with spoofing, ways to save the results of the scan, etc. That's probably going further than is warranted for now, just know the options are out there. If you want to read more on nmap go [here](https://nmap.org/), or at the terminal just enter in `man nmap` for a detailed look into all the different flags, their meaning and how to use them.<br>
