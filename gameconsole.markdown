---
layout: page
title: Designing the Game Console
subtitle: (A work in progress...)
permalink: /femoldark/gameconsole/
---

# The 3D modeling and slicing software

I was initially going to push this onto the main [femoldark](/femoldark/) page but I figured this will be a consistently updated topic, so I might as well create a seperate space for it. I settled on designing this case using <a href="https://www.matterhackers.com/store/l/mattercontrol/sk/MKZGTDW6" target="_blank" rel="noopener noreferrer">MatterControl</a> for the following reasons:
- It's free
- It's a relatively straight-forward 3d design software, nothing complex like you would see with Blender, etc
- It also acts as a slicer, so I can directly export the stl files into gcode for my Ender 3 Pro
<br><br>

All in all, it provides exactly what I'm looking for without a steep learning curve, and I would recommend it to any beginner. The one thing that it does not allow as a slicer is the ability to edit the nozzle and bed temperature, and the print speed by layer, which I only recently needed after upgrading to a glass bed instead of the magnetic one. Since then I have been using <a href="https://ultimaker.com/software/ultimaker-cura" target="_blank" rel="noopener noreferrer">Cura</a> as the slicer with great results, although a bit slower (as intended).
<br><br>
The game console has gone through many iterations and I think I've finally settled on a working design. It can be difficult to tell what will or won't work until it's actually off the print bed and in hand, but with enough trial and error I think it's nearing the final print stages.
<br><br>
There's something genuinely fun about writing the software behind the game, assembling the hardware that will interact with the software, and then designing the case that will house the hardware. Maybe I'll write my own linux distro just for this platform... I'm kidding, I don't how to do that.
<br><br><br>

# Files for download
If you want to preview what these look like (using GitHub's very poor in-built tool), reference these links:<br>
<a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_files/frontside_stl_for_github.stl" target="_blank" rel="noopener noreferrer">Front Cover</a> / <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_files/backside_stl_for_github.stl" target="_blank" rel="noopener noreferrer">Back Cover</a> / <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_files/side_pieces_stl_for_github.stl" target="_blank" rel="noopener noreferrer">Side Pieces</a> / <a href="https://github.com/fe-moldark/wesleykent-website/blob/gh-pages/assets/3d_files/buttons_stl_for_github.stl" target="_blank" rel="noopener noreferrer">Buttons</a>
<br><br><br>
If you want to download these files and manipulate them yourself, I will throw the link to the entire folder housing them <a href="https://github.com/fe-moldark/wesleykent-website/tree/gh-pages/assets/3d_files" target="_blank" rel="noopener noreferrer">here</a>. That folder has all of the above files in both their MCX and STL formats.
<br><br><br>

<h1><img alt="gear_gif" src="https://wesleykent.com/assets/gif gear.gif" width="45" height="45" style="vertical-align:bottom"/> Updates </h1>
<br>
_(Newer updates will appear at the top here, older ones at the bottom)_
<br><br><br>

#### Update, November '22:
The side pieces are now both complete and the center pieces (front and back) both nearly finalized. Every piece so far has taken at least one test print to identify some very minor adjustments (usually just a millimeters or so), after that everything prints off as expected. The downside is the time it takes to print - the side piece you see in the first video below took 5 hrs to print, so it's never a "quick" fix. I'm also paranoid that the 3D printer will catch on fire, so I never run it while I'm away. Check out the two updates below:
<br><br>
##### Part 1:
<center>
<iframe width="840" height="445" src="https://player.vimeo.com/video/765484157?h=6da0820cfa&amp;badge=0&amp;autopause=0&amp;autoplay=0;player_id=0&amp;app_id=58479" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>
<br><br>
##### Part 2:
<center>
<iframe width="840" height="445" src="https://player.vimeo.com/video/767171969?h=ca6b97c298&amp;badge=0&amp;autopause=0&amp;autoplay=0;player_id=0&amp;app_id=58479" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>
<br><br>

#### Update, October '22:
One issue I am working through right now is redesigning how the battery is going to work, which actually has more layers to it than you might think. What I've currently settled on should work, however based on some measurements it likely means I will have to heavily redesign the backside as the RPi board and the Battery case may end up switching places and rotating. The issues only compounded once I realized that some of the specific components I had bought (like the hdmi ribbon cable) were tailored to a very specific length, and now that everything is shifting I've got to reorder a longer one. Not the end of the world, but something that will set me back time-wise. Check out the update below:
<br>
<center>
<iframe width="840" height="445" src="https://player.vimeo.com/video/756628586?h=9c7c184f0b&amp;badge=0&amp;autopause=0&amp;autoplay=0;player_id=0&amp;app_id=58479" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</center>
<br><br>
