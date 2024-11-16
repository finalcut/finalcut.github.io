---
layout: post
title: "Java and the BSOD"
date: 2006-08-01
comments: false
category: java
tags: [eclipse,bsod]
---
I have been having a crazy problem with any java application (except for
Eclipse and it's derivatives like WebSphere) running on my machine. It will
start but the drawing routines never seem to happen correctly and then when I
force them to close (clicking the "x") I would get a Blue Screen of Death
(BSOD). After some research I discovered I could just turn off hardware
acceleration and the BSODs would go away. Sure enough that fixed the problem.  

However, that really isn't a very useful solution. So today I did a little
more research and found out the root cause of my problem. In my video settings
I had tweaked anti-aliasing to be a set value (8xs) instead of leaving it at
"application controlled". It turns out that, for some reason, java didn't like
my anti-aliasing settings and when I changed it to "application controlled"
the BSOD issue was resolved.  

This solution is ideal for me. However, for some this may be unacceptable as
well. It turns out you can be even more fine grained in your control of the
problem by setting some environment variables for Java. Instead of going into
full detail on this solution I will point you to two useful pages on the
topic:  
[Java Forum](http://forum.java.sun.com/thread.jspa?threadID=661574) and the
actual [Bug
Report](http://bugs.sun.com/bugdatabase/view_bug.do;:YfiG?bug_id=6267861).  

The forum was the source of my solution and it really provides all the
information you might need. So if your Java apps are causing you BSODs or just
aren't drawing properly (gray window) then check out that thread.
