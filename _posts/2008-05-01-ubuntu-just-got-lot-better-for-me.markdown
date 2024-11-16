---
layout: post
title: "Ubuntu Just Got A LOT better for me"
date: 2008-05-01
comments: false
categories:
 - linux
 - development
 - citrix
 - ubuntu
---
If you read my prior post about my troubles with Ubuntu during my first week
you will know I have been having troubles with my shift key in the Citrix
Client. 90% of my development time is spent in the citrix client so getting
this resolved was a deal breaker. Fortunately, today, I found a fix!  
  
The Citrix Support Website had a posting on [SHIFT Key Fails Using RDP in a
Java Client Session](http://support.citrix.com/article/CTX110281) however it
says it only applies from a windows environment. Fortunately for me they are
wrong because this fix also takes care of the problem from my Linux
environment. Sweet!  
  
In case the solution ever gets taken down here is the basic gist:  
  
1\. Launch your Remote Desktop Client.  
2\. When you get to the point where you are supposed to pick a computer to
connect to hit the "advanced options" button  
3\. On the advanced options dialog select the "Local Resources" tab  
4\. On the local resources tab under Keyboard > Apply Windows key
combinations, select On the local computer.  
  
That's it. Now you won't be able to alt-tab inside the remote computer BUT you
will be able to use the shift key, and frankly, I think shift is far more
important than alt-tab.

## Comments

Anonymous

Thanks for the fix. I have this issue with Dell Workstation, and it is SUCH A
PAIN IN THE ASS.  
  
Actually, just because of this issue, i was thinking of going back to Windoz
Vista crap!.  
  
You saved me from jumping into a pile of shit!  
  
I will go home today and try!!

Anonymous

wow THANK you. i have been so annoyed when having to do remote in from home on
my linux box. but with this fix, it's so much easier now. i KNEW i wasn't the
only one having this issue. thanks again!

Dave

Nice find, this was such a pain in the ass to deal with. Thanks

