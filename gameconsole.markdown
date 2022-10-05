---
layout: page
title: Designing the Game Console
subtitle: (A work in progress...)
permalink: /femoldark/gameconsole/
---
<br>
Update as of October '22:
<center>
<iframe width="840" height="445" src="https://player.vimeo.com/video/756628586?h=9c7c184f0b&amp;badge=0&amp;autopause=0&amp;autoplay=1;player_id=0&amp;app_id=58479" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>
<br><br><br>
I was initially going to push this onto the main [femoldark](/femoldark/) page but I figured this will be a consistently updated topic, so I might as well create a seperate space for it. I settled on designing this case using [MatterControl](https://www.matterhackers.com/store/l/mattercontrol/sk/MKZGTDW6) for the following reasons:
- It's free
- It's a relatively straight-forward 3d design software, nothing complex like you would see with Blender, etc
- It also acts as a slicer, so I can directly export the stl files into gcode for my Ender 3 Pro
<br><br>

All in all, it provides exactly what I'm looking for without a steep learning curve. If you did go ahead and watch the video above then you know the main issue right now is me redesigning how the battery is going to work. This actually has more layers to it than you might think. What I've currently settled on should work, however based on some measurements it likely means I will have to heavily redesign the backside as the RPi board and the Battery case may end up switching places and rotating. The issues only compounded once I realized that some of the specific components I had bought (like the hdmi ribbon cable) were tailored to a very specific length, and now that everything is shifting I've got to reorder a longer one. Not the end of the world, but certainly something that will set me back time-wise.
<br><br><br>
This has certainly been enjoyable, however, even with the set backs I just mentioned. There's something genuinely fun about writing the software behind the game, assembling the hardware that will interact with the software, and then designing the case that will house the hardware. Maybe I'll write my own linux distro just for this platform... I'm kidding, I don't how to do that.
<br><br><br>
**If you want to preview what these look like (using GitHub's very poor in-built tool), reference these links:**<br>
[Front cover](https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_files/front-cover.stl) / [Back cover](https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_files/back-cover-center.stl)
<br><br><br>
**If you want to download these files and manipulate them yourself, I will link them below:**<br>
[Front cover as STL](https://github.com/fe-moldark/wesleykent-website/raw/gh-pages/assets/3d_files/front-cover.stl)<br>
[Front cover as MCX](https://github.com/fe-moldark/wesleykent-website/raw/gh-pages/assets/3d_files/front-cover.mcx)<br><br>
[Back cover as STL](https://github.com/fe-moldark/wesleykent-website/raw/gh-pages/assets/3d_files/back-cover-center.stl)<br>
[Back cover as MCX](https://github.com/fe-moldark/wesleykent-website/raw/gh-pages/assets/3d_files/back-cover-center.mcx)<br>
