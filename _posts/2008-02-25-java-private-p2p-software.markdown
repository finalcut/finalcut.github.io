---
layout: post
title: "Java - Private P2P Software"
date: 2008-02-25
comments: false
categories:
 - java
 - contribution
 - p2p
 - opensource
---
My co-workers and I have started to dig into the guts of an open source
private p2p software package called [Alliance](http://www.alliancep2p.com/).
Overall it looks to be pretty well written and it has a nice UI so we have
decided to spend some time working on it and adding some features we want. The
current developers of the project are too busy to really do anything with it
at the moment so, hopefully, the changes we make will be ones they like and
will end up incorporating into the main release branch.  
  
We've already fixed a few minor bugs and added a few small features. Right now
the biggest new task we are working on is improving the search functionality
to not just search across files based on their file name but also upon the
meta data that is embedded within the file.  
  
To grab the meta data from audio files we are also just using a portion of a
different open source projected called
"[entagged](http://entagged.sourceforge.net/)" which will extract tag
information from about 10 different audio file formats.  
  
Once the audio file portion is done and working we will also do the same for
video. I am not sure if we will spend much time working on any other formats
though.  
  
So far I have been pretty impressed by the existing code from both projects
and, thanks to the good work each projects develeopers adding on is going
pretty smoothly.  
  
If you haven't checked out [Alliance](http://www.alliancep2p.com/) before I
recommend it. It's a nice package. This is my first time messing around
extending someone else's open source project and so far I've been enjoying the
work. Plus, it has been nice to muck with Java a bit more as I haven't really
used it with any rigorousness since 1999 (most of my time is spent dealing
with CF, C#, PHP, and some occassional Ruby).

## Comments

Bill

maciek,  
  
thanks for stopping by. I will have to herd all the guys here together and get
them to check in their changes.

Maciek

Hi there, stumbled upon this page while googling (yahooing actually..) for
Alliance.  
  
Did you complete the changes in the Alliance code? I'm one of the developers
and I'd be happy to merge it into the Alliance 1.0 code base.  
  
Feel free to post in the Alliance forum about this.

