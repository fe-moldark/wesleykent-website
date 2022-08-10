---
layout: page
title: Brute Forcing Logins and Passwords
subtitle: Using tools like Hydra, John, and Burpsuite
image: /home/wesleyvm1/WesleyKentBlog/assets/fe.ico
description: Using tools like Hydra, John, and Burpsuite
permalink: /tipsandtricks/bruteforcing/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

## Hydra for cracking online web portals, ssh and ftp ports
<br>
For this section I'll cover two examples using hydra - both will be instances I've used in exploits from various CTFs<br><br>
First, some of the basic flags used with hydra:<br>
- You need a username: `-l admin` for a single username OR `-L usernamelist.txt` for a list of possible usernames
- You need a password to run against the username(s): `-p aSinglePassword` OR `-P /usr/share/wordlists/rockyou.txt`  the latter being more likely
- You need the IP address you are targeting, for example: `10.10.188.175`
- If you need to designate a non-default port: `-s [port#]`
- The _type_ of attack, examples include: `http-post-form`, `ssh`, or `ftp`, to name but a few
- If it is an `http-post-form` you will need to designate either a (for example) `:S=302` indicating a redirect which might be a good sign, or a `:F=failed` which would designate a failed login attempt (i.e. ignore).
- Another part you will need for the web logins specifically is the actual request, which is obtained with burpsuite and get into that down below
- There are many more flags you can include, but these should be enougshould get you started.
<br><br><br>

#### Example: Using hydra against a web portal
This was a Mr. Robot themed CTF if I recall correctly, anyway hopefully seeing all this put together makes more sense:<br>
After running gobuster to enumerate their web server I found their login portal at "/wp-login". From there I used burpsuite to capture the request:<br>
<br>![](/assets/burp1.jpg)<br><br>
I replaced my test inputs of "testuser" and "testpw" with the appropriate `^USER^` and `^PASS^` notation, and at the end of that added that a success means a 302 redirect, since that means I am being logged in and forwarded elsewhere: `:S=302`.<br>
Before I show the command I will also note that I knew the username was `fsociety` and had obtained a password list hidden on their site called `fsociety.dic`.<br><br>
SO - putting all this together and knowing the syntax from above we get the following (semi-coherent) command:<br>
`hydra -l fsociety -P /home/wesleyvm1/Downloads/fsociety.dic 10.10.188.175 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&redirect_to=http%3A%2F%2F10.10.188.175%2Fwp-admin%2F&testcookie=1:S=302`<br>
<br>
It's as simple as that. Even more simple is an ssh brute force, which I will cover below.<br><br>
Quick note: To clarify the `:F=failed` scenario, basically if after attempting a login if that word (in this scenario "failed") appears on the screen that indicates an `F`, or failure, so it will try again until it does not get the word "failed" on the page - i.e. a successful login.
<br><br><br>
#### Example: Using hydra against a ssh port
I forget the name of this CTF, but you'll see how much more straightforward of an exploit this was.<br><br>
What I knew going into this: the username was `lin` and I had obtained a possible password file named `locks.txt` anonymously from their ftp server.
<br><br>
The final command ended up being as simple as:<br>
`hydra -t 4 -l lin -P /home/wesleyvm1/Downloads/locks.txt 10.10.180.91 ssh -v`<br><br>
And to see what a successful login looks like, this is what I (eventually) got:<br>
![](/assets/hydra1.jpg)<br>
You can see for this instance I chose to incldue the `-t 4` flag to lower the default number of tasks and used the `-v` for verbose.<br><br><br>

## Hash-identifier, hashid, and John
<br>
Okay, let's say you get your hands on the `/etc/shadow` file or some other form of a hashed password, how do you go about identifying the hash before you can try and break it?<br>
For this, many distributions of linux should have a tool called "hash-identifier". How it works is you simply type in `hash-identifier` in your terminal and that'll start the program where you'll be prompted to enter in the hash. Alternatively, you can use a tool called "hashid" which works very similar to the former, if you need help with this one just enter in `man hashid` or `hashid --help` for help figuring it out.
<br><br>
Now using John to crack the hash. The first step is which _type_ of hash are you cracking, for instance John lists at least 5 different forms of MD5 hashes. So to identify which one is the one to use with John, type in something along the lines of `john --list=formats | grep MD5`. This will give the different MD5 hash forms you can try. Once the format is chosen, you will need a password list to use, the default should almost always be the `rockyou.txt` file (reference [here](/resources/freshinstall/) to get it), and if that doesn't work you'll likely have to branch out to other lists from SecLists.
<br><br>
Now to setup an example brute force against a MD5 hash stored in the hash.txt file:<br>
`john --form=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt`<br>
<br>
Note: If you have already cracked a specific hash and deleted it, John will say it is already cracked if you try it again and then annoyingly not show you what it is. That cracked hash can be found in the john.pot file on your system. Since I don't know where you'll install John, you can find it with the following command:<br>
`find / -type f -name john.pot 2>/dev/null`<br>
<br>
Another note: Sometimes before attempting to crack a file you will need to convert it to a format that John can use. These tools are named things like "ssh2john" or "zip2john" (reference [here](/thm/2022/04/18/TomGhost.html) for a time when I had to use "gpg2john"), and since there are so many different kinds of formats out there, I'll leave you to do your own research on each one specifically. Just know that before John can take a crack at certain file types there has to be some conversion made beforehand. There are a million forums online that will cover the how-to for ssh keys, zip password protected files, etc - what's important is that you know these tools exist.<br>
<br><br>

## Other means of breaking hashes / encoded files
Even if you don't know much about encoding / decoding you probably have heard the term "base64" at some point. To decode a file as simple as this just use:<br>
`cat filename.ext | base64 -d` and you can of course output the result to a file by adding `> output.txt`
<br><br>

## One note on everyone's favorite resource... online tools
To be fair, I do try and use John whenever possible to keep sharp on that skill, but I can be lazy and there are powerful online cracking tools out there. Sometimes it is tedious to go through the whole process of identifying the hash with a hash-identifer, it eventually tells you it is a raw MD5 hash, then you have to find the exact format for it in John with `john --list=formats | grep MD5` - where you eventually see `Raw-MD5` as an output, and then you finally run the command `john --format=Raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt`. What I'm saying is that sometimes it can be a tedious process, and plenty of online resources can save you that time and energy. Sites like [crackstation](https://crackstation.net/) are one of many out there that can meet these needs, just make sure to stay proficient with John.
<br>
