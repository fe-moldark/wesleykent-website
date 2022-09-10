---
layout: page
title: FE Moldark
subtitle: Building a game from the ground up...
image: /assets/fe.ico
description: The pages meta description
permalink: /femoldark/
#hero_image: /assets/fe.ico
#hero_height: is-fullheight
--- 

I won't go into detail here since I have already created an entirely seperate website for this topic at [fe-moldark.dev](https://www.fe-moldark.dev).
<br><br>
Summarized, this is a game I have been recreating with Python / Pygame from the ground up, literally started at nothing and the project now stands at around 16,000 lines of code. The game I am recreating is Fire Emblem, more specifically the older versions as seen on the GBA and DS since that is what I grew up with. This is a project that has been ongoing for many years now with just as many breaks in between. Life happens and you get busy I guess.
<br><br>
One thing I will note is that the end goal is to play this game on a case that I will make using a 3D printer I recently purchased. I've already got the design down (on paper that is) and what parts I will need, however some initial tests on my Pi 3B+ showed the processor was too slow. Thankfully, I don't think the issue is in my code, rather times when the screen has to blit numerous surfaces with some transparent parts that need the `convert_alpha()` - that's not really something I can get around. That being said, I am looking into getting a Banana Pi M5 as that _should_ provide more than enough additional computing power. Given the chip / pi shortage however, that may take some time to get, and with other projects and school right now I am okay with keeping this part on the back burner.
<br><br>
Again, a lot to say about this but there is a website that does so better and in more detail, so click the link above if you are interested. To maybe pique your interest I'll include some screenshots of the gameplay / graphics I've created for this project. Enjoy.
<br><br>
<center>
	<img src="/assets/femoldark/chapter config.png" alt=""><br>
	<img src="/assets/femoldark/armory.png" alt=""><br>
	<img src="/assets/femoldark/fog of war2.png" alt=""><br>
	<img src="/assets/femoldark/full enemy map.png" alt=""><br>
	<img src="/assets/femoldark/move map.png" alt=""><br>
	<img src="/assets/femoldark/player info.png" alt=""><br>
	<img src="/assets/femoldark/player phase.png" alt=""><br>
	<img src="/assets/femoldark/supply.png" alt=""><br>
	<img src="/assets/femoldark/trade chapter config.png" alt=""><br>
	<img src="/assets/femoldark/trade.png" alt=""><br>
</center>

