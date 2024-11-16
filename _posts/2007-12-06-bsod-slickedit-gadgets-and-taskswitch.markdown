---
layout: post
title: "BSOD: SlickEdit Gadgets and TaskSwitch XP"
date: 2007-12-06
comments: false
categories:
 - alttab
 - visual-studio
 - slickedit
 - plugins
 - taskswitchxp
 - windows
 - smarttab
---
I have been doing a lot of .Net development these past few months and one
thing about visual studio that drives me crazy is keeping track of what line
the focus is on when I jump to a search result. The cursor is not intrusive at
all which is great when you're typing but it sucks when you are trying to jump
to a line of code.  
  
I found the solution to that a few days ago thanks to SlickEdit Gadgets for
Visual Studio 2005. They have this "ruler" tool that highlights the current
line in the color of your choice. I was so happy! Well, until today [when I
was alt-tabbing](http://community.slickedit.com/index.php?topic=768.msg3364)
between two instances of Visual Studio and BAM I got a Blue Screen of Death
([BSOD](http://www.google.com/search?q=BSOD&ie=utf-8&oe=utf-8)).  
  
It turns out that the [gadget does some
trickery](http://community.slickedit.com/index.php?topic=659.0) to generate
the highlight because, quite frankly, there doesn't seem to be many other ways
to do it. The trickery deals with double buffering and some calls to the
PrintWindow API call. That works great so long as you aren't using a special
ALT-TAB replacement for windows that shows you a thumbnail of the screen
you're alt-tabbing to. As it turns out I was using a wonderful free tool
called [TaskSwitch XP](http://www.ntwind.com/software/taskswitchxp.html) which
makes the same PrintWindow API call at the same general time as the gadget
did. Windows doesn't like this double call to PrintWindow and so you get the
dreaded BSOD. Crap.  
  
I personally don't really need the little thumbnail. What I liked about the
TaskSwitch XP was that I could be alt-tabbing with my left hand and using my
mouse with my right hand and clicking on an entry in the task list to switch
to it; plus TaskSwitch XP gives a better textual description of what you are
switching too. What's a spoiled alt-tabber to do when he needs to better be
able to see where he is contextually in his code?  
  
I didn't want to drop TaskSwitch XP but I did because I found a replacement
that is perfect for me. It does everything TaskSwitch XP did but without the
thumbnails and, just like TaskSwitch XP it is free. I am now using
[SmartTab](http://www.smarttab.org/).

