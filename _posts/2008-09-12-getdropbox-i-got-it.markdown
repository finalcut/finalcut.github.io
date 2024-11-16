---
layout: post
title: "GetDropBox? I got it."
date: 2008-09-12
comments: false
categories:
 - synchronization
 - file-sharing
 - filestream
---
I do a lot of work for a wide array of people and companies. A lot of times
that work is done remotely via some kind of vpn or remote desktop or thin
client (citrix) that keeps my local files completely separate and unavailable
on the remote machine. However, sometimes I need to share a file between the
two machines yet there is no way to do so.  
  
For instance with some of the client machines I can't ftp, I can't email out a
large (over 5mb attachment), I can't ssh or rsynch or anything else that might
help me move a file between the two locations. For a while I had a good
solution in strongsafe.com but that server was eventually blocked by one or
more of the client firewalls.  
  
In general they have very very good reasons for blocking this stuff; they
really want to make it hard for sensitive stuff from getting out of the house.
However, the things I need to move around are often large images, or
development libraries (dlls, jars, etc) that I work on locally (where there is
no keyboard lag) and then I want to push them to the client machine for use in
the overall project. I really need a way to share these files to maximize my
productivity and now, thankfully, [getdropbox.com](http://www.getdropbox.com/)
is on the scene to solve my problem - at least temporarily (so long as my
files aren't more than 2gb in size).  
  
With getdropbox I just install the app and it creates a pseudo-directory on my
machine. Then any file I plop in that directory is automatically pushed to any
other machine that I have linked to my getdropbox.com account. It works over
the clients http proxy and it works pretty well. So far I've only tested it
out with small files but I feel like this is going to be a good way to move
forward (well, until they block it too).  
[  
Getdropbox.com](http://www.getdropbox.com/) just came out of private beta this
week so if you are looking for a good way to synch or share files you might
want to give them a look. It's free, encrypted, and pretty damn easy to use.

## Comments

Nexus Rex

Never mind - I figured it out. GetDropBox uses a Python client and Amazon S3
(simple storage service).  
  
\--  
Travis Cable

Nexus Rex

Anybody know what they built GetDropBox with? Java, Python, C+?

daryljames

Thanks for the heads up. Sometimes it's hard to tell them all apart.

Bill

so far I'm happy. I haven't had to use it much but it works like a charm and
fills a definite need I had.

Elvis

How has your experience with it been so far? I just installed it yesterday to
share files between my computer at work and at home.

