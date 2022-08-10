---
layout: page
title: Web Stuff
subtitle: Web enumeration, starting a web server, and uses of curl
image: /home/wesleyvm1/WesleyKentBlog/assets/fe.ico
description: Web enumeration, starting a web server, and uses of curl
permalink: /tipsandtricks/webstuff/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

# Introduction
Note: reference the [bruteforcing](/tipsandtricks/bruteforcing/) page for using hydra against http / https login pages. On to the rest.
<br><br><br>
## Web Enumeration
I will be focusing solely on `gobuster` since that is what I have consistently used without issue, but you can look into `dirb` if that is your preference.
<br><br>
Below is my default web enumration / gobuster scan that I always start with:
`gobuster dir -u 10.10.242.242 -w /home/wesleyvm1/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt `<br>
As you can see I'm using one of the lists from SecLists, and you can use more expansive lists (takes more time though) or use more focused lists at specific types of web servers. Other good ones I use are the `common.txt` and `big.txt` in that same directory from SecLists.
<br><br><br>
## Starting a Web Server
Since most modern web servers come with some version of Python installed and you very often can get access to it because of how much it is used, it comes handy when trying to start a web server. This might be to get a more visual representation of a directory within a web server, maybe you want an easy point-and-click method for downloading files, etc. Of course, this scenario implies you do already have access to the server, thought I should mention that.<br><br>
To do this with the more modern version of Python, version 3, execute the following _within_ the directory you will need access to (you won't be able to go "up"):<br>
`python3 -m http.server` and then navigate to that IP address and port
<br><br>
Alternatively, you can use an older version of Python if present:
`python -m SimpleHTTPServer 8000` where the 8000 is just any port you choose
<br><br><br>
## Curl and wget
Just a quick note that curl can be used to trigger a reverse tcp shell you uploaded as an e.g. php file, I discuss that on the [privilege escalation](/tipsandtricks/privilegeescalation/) page.
There are also ways to curl a file TO a web server, but you won't likely need to use that.
<br>
