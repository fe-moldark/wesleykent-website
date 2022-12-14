---
layout: page
title: Web Stuff
subtitle: Web enumeration, starting a web server, and uses of curl
image: /assets/fe.ico
description: Web enumeration, starting a web server, and uses of curl
permalink: /tipsandtricks/webstuff/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

# Introduction
Title more or less says it all. If you are looking for help on how to setup hydra attacks against http / https login portals reference the [bruteforcing](/tipsandtricks/bruteforcing/) page. On to the rest.
<br><br><br>
## Web Enumeration
I will be focusing solely on `gobuster` since that is what I have consistently used without issue, but you can look into `dirb` if that is your preference.
<br><br>
Below is my default web enumeration / gobuster scan that I always start with: `gobuster dir -u IP_ADDRESS -w /home/wesleyvm1/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt ` - that should give you enough to work on in the beginning.<br><br>
As you can see my initial scan comes from SecLists, and you should use more expansive lists and more focused lists at specific of web services after that initial scan. Other good ones I use are the `common.txt` and `big.txt` in that same directory from SecLists. If you need to designate a non-default port just add that as you normally would to the IP address with `IP_ADDRESS:Port#`. Lastly, in some instances I've run into issues with certificates being invalid, you can disable certificate checks with a `-k` flag. Anything else you'll need for it can be found within the help menu.
<br><br>
Another tool you can use for this is your standard search engine. Let's take a look at my own website - if I were trying to find the page for my Raspberry Pi Projects I could use duckduckgo's search engine with the following query: `site:wesleykent.com Raspberry Pi`. Now, annoyingly this doesn't work on Google yet because their search engine refuses to crawl my website, but you get the idea of what this kind of search does. Say you are looking for an employee's login portal for a company's website - you might try that same search but modified for a different website name and maybe looking for the string "login". This certainly shouldn't be your only source of enumerating a web server, but it's another tool in your toolbelt to be aware of.
<br><br><br>
## Starting a Web Server
Since most modern web servers come with some version of Python installed and you can very often get access to it because of how much it is used, it comes in handy when trying to start a web server. This might be to get a more visual representation of a directory within a web server, maybe you want an easy point-and-click method for downloading files, etc. Of course, this scenario implies you do already have access to the server, thought I should mention that.<br><br>
To do this with the more modern version of Python, version 3, execute the following _within_ the directory you will need access to (you won't be able to go "up"):<br>
`python3 -m http.server` and then navigate to that IP address and port. You can also use a web server as a host on your local machine and then `wget` a script from your server to the target machine. I've used this method several times.
<br><br>
Alternatively, you can use an older version of Python if present:
`python -m SimpleHTTPServer 8000` where the 8000 is just any port you choose.
<br><br><br>
## Curl and wget
Just a quick note that curl can be used to trigger a reverse tcp shell you uploaded as an e.g. php file, I discuss that on the [privilege escalation](/tipsandtricks/privilegeescalation/) page.
There are also ways to curl a file TO a web server, but you won't likely need to use that. I've only had to do that once, [here](/thm/2022/05/26/Dav.html).
<br>
