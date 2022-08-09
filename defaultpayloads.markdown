---
layout: page
title: Default Payloads and Metasploit
subtitle: 
image: /home/wesleyvm1/WesleyKentBlog/assets/fe.ico
description: Brief overview of some default payloads and how they're used in Metasploit
permalink: /tipsandtricks/defaultpayloads/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

## Introduction
So what is Metasploit - it is a framework used to find and exploit vulnerabilities on a network, which makes it a great tool for pen testing.<br>
How it is accesed - enter `msfconsole` at the terminal.<br>
<br>
This is often used in conjuction with searching exploit-db or more easily using the tool `searchsploit`. `searchsploit` will return a list of any known vulnerabilities associated with a service  or OS and its version. For instance, an old CTF I did called something like "tom ghost" I think had the Apache Tomcat v9.0.30 running over port 8080. From there, searchsploit as well using `search apache tomcat` on msfconsole pointed towards a known exploit called `auxiliary/admin/http/tomcat_ghostcat`.<br><br>
From there, you can `use x`, with "x" being the number next to the matching module you want to use. `options` will tell you what settings you can be, and which settings have to be, changed. This is done be designating `set OPTION NEW_SETTING`.<br>
Example: To change the target host this would appear as: `set RHOSTS 10.10.40.182`<br>
And then when ready to execute - enter `exploit`.
<br><br>
The two general types you will use from msfconsole are going to be labeled either an "exploit" or an "auxiliary" scan.<br>
I believe I created a report on that exploit, if I remember to link it will be [here]().
<br><br>

## Default Payloads List
Full disclosure on the following list of default payloads for metasploit - I did not put this together, I got it from another site proably a year back and I can't remember which one it was, but I _think_ it was [this one](https://docs.rapid7.com/metasploit/working-with-payloads/). Anyway, metasploit will auto choose from the following list or you can manually designate which one you want to use:<br><br>
windows/meterpreter/reverse_tcp<br>
java/meterpreter/reverse_tcp<br>
php/meterpreter/reverse_tcp<br>
php/meterpreter_reverse_tcp<br>
ruby/shell_reverse_tcp<br>
cmd/unix/interact<br>
cmd/unix/reverse<br>
cmd/unix/reverse_perl<br>
cmd/unix/reverse_netcat_gaping<br>
windows/meterpreter/reverse_nonx_tcp<br>
windows/meterpreter/reverse_ord_tcp<br>
windows/shell/reverse_tcp<br>
generic/shell_reverse_tcp<br>
<br>
