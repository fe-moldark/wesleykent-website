---
layout: page
title: The Kent Encryption Standard
subtitle: Yes, I am vain enough to name it after myself
description: Encrypts a six column csv file delimited by a semicolon into an encrpyted password wallet.
permalink: /scripts/kent_encryption_standard/
---


# <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/KEF/KES_v3-11.py" target="_blank" rel="noopener noreferrer">The Kent Encryption Standard</a>
This is a complete overhaul of the [original cipher](/scripts/creating_my_own_cipher/) I had written many years ago, but this one is actually secure. Which means I have been unable to break it no matter what way I look at it, but I welcome anyone to prove me wrong. The only method I can see is to brute-force the password. What this encryption does is convert a six column csv file delimited by a semicolon into an encrypted file. Within the program you can add, delete, and modify entries, save those changes, and change the password used to encrypt the data if you so choose.
<br><br>
Going over this by line or by section in the code sounds exhausting since it's just shy of 1,000 lines of code, so I will just break down the broader steps it takes so you can understand what the code is doing. Link to the script can be found <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/KEF/KES_v3-13.py" target="_blank" rel="noopener noreferrer">here</a>.
<center>
  <img src="/assets/KEF/welcome_menu.png" alt="" width=900><br>
</center>
<center>
  <img src="/assets/KEF/search_example.png" alt="" width=950><br>
</center>
<center>
  <img src="/assets/KEF/kef_example.png" alt="" width=1300><br>
</center>
<br><br>

# High level overview of how the encryption works
- **Step 1:** Using a SHA512 hash of the given password a unique 128x128 hash array will be created
- **Step 2:** Each character in the cleartext file will use a unique hash using a `hash(original hash + thatRow[0:index of that character being encoded in the array's row]`
- **Step 3:** A random 16x16 array will be created using hexadecimal values for each character to be encoded
- **Step 4:** Using four of the first unique pairs in the character-specific hash, four locations to encode the data will be selected
- **Step 5:** The hex value of the character will be assigned, for instance `?` would be equal to `3f`
- **Step 6:** A random hexadecimal value will be chosen, and the second must "add" to create the target. For example, to encode the `3` let's say the first randomly chosen hex value was a `0`, so the second would be a `2` (positions of 1 + 3 == 4, or `3`)
- **Step 7:** This will be done for the `f` value as well, and each of the four unique locations will be selected to host each of the 4 unique values that make up the single hex-encoded character
- **Step 8:** This is done for each and every character, and at the very end all of the 16x16 arrays are combined "horizontally"
- **Step 9:** The (now very long) 16 rows are then shifted x number of characters using elements of the original hash
- **Step 10:** Export the data in an xml-based format to a KEF wallet
<br><br>


# Limitations of encoding
Let's cover some brief limitations:
- The initial format must be a 6-column csv file delimited by semicolons, and the very first column in that row should be a `0` (example base file <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/KEF/example_base.csv" target="_blank" rel="noopener noreferrer">here</a>).
- Only hex-encodable ascii characters are accepted. Anything not accepted during encoding will alert the user and replace the character with a `?`.
- There is a limit of 128^2 characters, or ~16,000. THIS IS OKAY. None of this is meant to be the most efficient or scalable encryption - it accepts a very specifically formatted file and encrypts it. Choosing an alternate base hashing algorithm besides SHA512 could increase this amount, but for a password wallet this is not necessary.
- Error handling may not be perfect. I went through my own fuzzing process trying to generate weird scenarios and errors, and I believe most situations are now properly handled. I'm far from perfect however (shocking, I know), so I'm bound to have missed some things.
- The security of the wallet is only as good as its password. If you want to choose "1234" as your password then I don't even know what you're doing reading this webpage
- As already mentioned, this is not meant to be an efficient algorithm since it increases the file size by ~170x. Is this a problem? No, because even now with every password and account info I have saved in my KEF wallet it only increased the file size from <10 KB to <1.5 MB.

<br>

# Version 3.12
<a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/KEF/KES_v3-12.py" target="_blank" rel="noopener noreferrer">This version</a> is designed to work directly in a bash shell with no prompts and you can add an alias for it like `alias wallet='clear && python /home/<user>/System/Scripts/KES_v3-12.py --file /home/<user>/System/Files/wallet.kef && clear'`. Some notable improvements include time-based lockouts for security and a bug fix to the matrix generation that will never, ever happen in a million years (but theoretically could).
<br><br>

# Version 3.13
<a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/KEF/KES_v3-13.py" target="_blank" rel="noopener noreferrer">This version</a> fixes a bug that allows you to overwrite your KEF wallet with bad data after the decryption process appears to go through fine, but actually returns gibberish. I do not want to discuss how it was I discovered this bug...
<br><br>

# Conclusion
This was a very fun project once I got it working, everything up until that point was just soul-crushing hours trying to figure out where the problems were. Built-in to the encryption program is the decryption side of it as well, which offers a very nice UI for you to interact with and manipulate the data once decoded. I also added a function to check if a particular string is found in the decrypted file, which once found after decryption can send an email to a target address pulling the username and public IP of whoever ran the program.
<br><br>
Since this is a broad overview of how it all works I would encourage you to actually look through the script and try it out for yourself. The UI is fun to interact with, I even spent an hour color coding things so it isn't just white on black in the terminal, which by my standards is fancy. Enjoy.
<br><br>
