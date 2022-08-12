---
layout: page
title: The Basics
subtitle: A collection of random thoughts that aren't individually long enough to warrant their own page
image: /assets/fe.ico
description: If you need any help with the basics, such as indexing, locating stuff, anything not directly related to pen testing, but essential to know
permalink: /tipsandtricks/thebasics/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
--- 

# Some random thoughts to begin

To viewing tasks running on a machine:<br>
- I trust you know how this works on Windows, go to task manager
- With Linux you can use `ps aux` and then `grep` for specific processes. To kill by process ID, just `kill PID`


For current location in the system, use `pwd`.

When doing searches and other commands using the `2>/dev/null` throws out the stderr to the void, or the `null`.

Useful logs can always be found in `/var/log`, Windows has Event Viewer, etc.
<br><br><br>

## Finding Information

To find out who you currently are on the system use `whoami`.
<br><br>
Listing what is in the current directory with `ls`, there are more flags you can through on there to expand or limit the search (e.g. including hidden files). Also look into using `| grep SOMETHING` to only return results containg specific strings.

To pull words from gibberish use: `strings filename.ext`<br>
This might thwart a poor attempt on someone's part to hide real information in plain text behind a bunch of randomly combined letters in a large text file.

To recursively grep, ignoring case sensitivity: `grep -iRl "search for this string"`<br>
The `i` is ignoring the case, the `R` for the recursive search.<br><br>
A `grep -x` search would search for an exact string.<br>
Adding a `-C3` would highlight the line where the text was found as well as three lines above and below it. You can substitute `A` or `B` as well for returning lines just above or below the search as well.<br><br>
<br>

## Getting files over ftp, sftp, ssh, and smb

#### ftp / sftp
Let's start with ftp, from your nmap scan you should know whether or not you have anonymous login capabiltities, but even without that there are scripts you can run to enumerate usernames or try and brute force a login with hydra.<br>
Once on the server, you can `get filename` back to your local machine, use the `put` command for uploading files, and navigate / list directories with `dir`, `ls`, and `cd` like normal.<br>
Note: To actually initiate an ftp session, simply use: `ftp IPADDRESS`, at which point you will prompted with a login request.
<br><br>
I've had limited interactions with sftp, but I do know it is a secure version of ftp running over ssh (port 22), and should use almost identical or identical commands to ftp.
<br><br>
#### ssh
For ssh, you will need to connect in various ways - here's a few situations you might see:<br>
- The "normal" way - `ssh username@IPADDRESS` and once prompted enter the password
- Logging into a domain - `ssh -l username@something.local IPADDRESS`
- When using a key - `ssh -i path_to_key username@IPADDRESS`
<br>

Note: Reference the [brute forcing](/tipsandtricks/bruteforcing/) page for how to brute force a login over ssh.
<br><br>
#### smb
For smb, there are some tools that are useful to enumerate the shares and users from the port, and for this I mainly use `enum4linux`.<br>
Whenever you see smb running over a port (commonly seen over 139 and 445), the following command will help with enumeration:<br>
`enum4linux -a IPADDRESS`<br><br>
This will perform all simple enumerations and from there hopefully you will uncover some shares you can get anonymous access to, maybe the usernames there are the same for other services running (like ssh for a possible brute force), etc.<br><br>
To actually login afterwards once you have more info:<br>
`smbclient //IPADDRESS/SHARE -U username -p port`<br>
Again, if you can login anonymously you shouldn't need the `-U` flag, and if smb is running over a standard port the same goes for the `-p`.<br><br>
Smb follows similar commands like with an ftp server, to get files off the server you can use the `get filename` command.
<br><br><br>

# More on file permissions
Interestingly enough you can actually see if files have SUID permissions based on their permissions as the rwx permissions denote it with an "s", but that's beside the point.
<br><br>
Linux file permissions are described with three numbers, each of which can be between 0-7. Assuming you already know binary, let's take a look at just one of those three numbers. Now, each bit when combined (ex. binary bit for 4 and 1 = 5 total) would describe the read, write, execute permissions (aka 4,2,1 - with 0 meaning NO permissions) for that number.<br><br>
But, there are three numbers, right? _Each_   of those three numbers - be it, 777, 754, 600, etc etc _individually_ describe the permissions (read write execute, don't forget) for the user, the group, and lastly anyone else.<br><br>
Let's take an example of a permission set of "650":
- The first 6 in binary would be 110(0) = (4+2+0+0) and we care about the left most three
- The second number, 5, would be 101(0) = (4+0+1+0) and again, only the left three matter
- The last number is 0, which 000(0) = (0+0+0+0), denoting no permissions for anyone else
<br><br>

So, we said we care only about the left three digits - starting with the "6" in binary that was 110.<br>
In terms of our read write execute permissions, then, the USER has read, write, but NOT execute permissions for that file.
<br><br>
The next digit, "5", is the permissions for the GROUP - which in binary is 101 (again, we only care about the left three).<br>
So, the GROUP's permissions include YES to read, NO to write, and YES to execute.<br><br>
Lastly, the 0 indicates NO permissions at all for anyone else outside the user and group.<br><br><br>
And one thing I almost forgot to add - `chmod` and `chown`.<br>
- To "own" a file, thus giving yourself permissions to use it, you can use the `chown USERNAME filename` command.<br>
- The `chmod` command can be used to add or otherwise alter permissions for a file.<br>
For example: `chmod +x filename` will give you executable permissions, or something like `chmod 777 filename`, where the number is whatever permissions you want to designate.<br><br><br>

This breakdown makes sense to me, but might be horribly explained to you. There are number of ways to explain this, and I'm sure you can find a video or another explanation if this didn't quite hit the mark. Cheers.
<br>
