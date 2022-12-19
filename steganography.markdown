---
layout: page
title: Steganography
subtitle: What is steganography, how is it used and how to counter it
image: /assets/fe.ico
description: What is steganography, how is it used and how to counter it
permalink: /tipsandtricks/steganography/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
---

# What is Steganography
Steganography - concealing information within something else so that it is not visible to anyone except those that have the key and know where to look. Often this will be seen as embedding data into images, and to uncover that information there are a number of tools we can use.
<br><br>

# Tools to uncover information
To install `stegosuite` and `steghide` reference my [resources](/tipsandtricks/resources/) page.
<br><br>
To start the GUI for stegosuite, simply enter `stegosuite` in the terminal. From there you can select a file and enter a key to try and identify embedded files.<br><br>
Another tool you can use is called `binwalk`, for more details on how it works enter `binwalk -h` or reference <a href="https://www.kali.org/tools/binwalk/" target="_blank" rel="noopener noreferrer">this site</a> from Kali Linux.<br>
Example usage of this would be `binwalk -e file.bin`, where the `-e` flag indicates to extract known file types.<br>
<br>
A companion tool to `stegosuite` is `steghide` can be used to both embed and extract data, for the various flags / uses on that reference `man steghide`.
<br><br>

# A Challenge
If you want a challenge with decryption reference <a href="https://raw.githubusercontent.com/fe-moldark/wesleykent-website/gh-pages/assets/cipher/encrypted_image.jpg" target="_blank" rel="noopener noreferrer">here</a> for a go at a cipher I wrote a while back. This was well before I had done any reading at all about cryptography, steganography, ciphers, etc. but I had fun making it. I have a full break down on how this works [here](https://wesleykent.com/creating_my_own_cipher/).
<br><br>
