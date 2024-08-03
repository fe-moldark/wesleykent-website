---
layout: page
title: Fix for FortiClient Vuln 5303 // CVE-2023-29328 Remote Code Execution Vulnerability
subtitle: 
description: Fix for FortiClient Vuln 5303 // CVE-2023-29328 Remote Code Execution Vulnerability
permalink: /FortiClient_CVEs/CVE_2023_29328
---


# Fix for FortiClient Vuln 5303 // CVE-2023-29328 Remote Code Execution Vulnerability
This vulnerability appeared for nearly a hundred devices on our FortiClient EMS - 93 to be exact. Looking into some of these computers showed it was an old Teams directory in the user's `AppData` folder, and nearly all of these accounts had only been logged into once to set up the computer and join it to the domain. Now, getting rid of this is fairly simple and takes three steps:
1. Run the python script or package it into an executable like I did and deploy via PDQ
2. Reboot the computer (can be done via GPO, PDQ, manually, etc)
3. Wait for the daily scan or force a rescan over the FortiClient EMS and you'll see it go away
<br><br>

If you want to avoid downloading a sketchy executable from some guy on the internet (I get it) you can convert the <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/FortiClient_CVEs/CVE-2023-29328.py" target="_blank" rel="noopener noreferrer">python file</a> yourself, otherwise here is the <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/FortiClient_CVEs/CVE-2023-29328.exe" target="_blank" rel="noopener noreferrer">executable</a>. Here's what it looks like from both the EMS server and directly on the device:
<center>
  <img src="/assets/FortiClient_CVEs/forticlientems.png" alt="" width=1100><br>
</center>
<br><br>
<center>
  <img src="/assets/FortiClient_CVEs/forticlient error.png" alt="" width=950><br>
</center>
<br><br>

The program accepts one optional flag (-l or --log-file) to write some basic logs to. No log file or an invalid location will just print it out normally to the terminal. What this looks like as a PDQ package is:<br>
<center>
  <img src="/assets/FortiClient_CVEs/pdq_package.png" alt="" width=1000><br>
</center>
<br><br>

# A few more notes:
The vulnerability appears in FortiClient EMS but does not show the exact folder location unless you are on the computer itself looking at the FortiClient application. But, that application is pulling the info from a log file, which by default is at `C:/Program Files/Fortinet/FortiClient/logs/netDB.dat`, and looks like this:<br>
<center>
  <img src="/assets/FortiClient_CVEs/log_file_opened.png" alt="" width=1000><br>
</center>
<br><br>


Now, this script assumes only one user account needs this removed, which was the case for our 93 devices. If you have this on a couple of accounts you may just need to run through that script/executable a few times until every account's `Teams` directory has been removed, or manipulate the script a bit.
<br><br>

If converting the python script yourself look to `auto-py-to-exe` or something similar. Any questions, feel free to reach out via contact info on the [about](/about) page.
<br><br>
