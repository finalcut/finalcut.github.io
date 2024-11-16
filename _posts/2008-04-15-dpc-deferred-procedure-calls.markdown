---
layout: post
title: "DPC - Deferred Procedure Calls"
date: 2008-04-15
comments: false
categories:
 - share
 - dpc
 - windows
 - cpu-usage
---
First I need to retract my statement that Flock was causing all of the DPC
issues I was having. It wasn't - instead it was a much more subtle problem and
I'm still not entirely sure what to do about it.  
  
DPC's or Deferred Procedure Calls have been intermittently bringing my laptop
to its proverbial knees over the past few weeks. Initially I had blamed the
social browser, Flock. After I removed it the problem persisted though (this
was a pretty intermittent problem) and I have waited until know to admit I was
wrong becuase I wanted to know what the heck was going on.  
  
This morning the DPC situation arose again. I was cruising along getting some
work done when suddenly my machine became unusable. ProcessExplorer told me
the DPC's were back eating up 60-80 of my CPU and there was nothing I could do
to stop it short of a reboot but I really didn't want to reboot.  
  
I keep all of my music on an external USB harddrive and I had some background
processes going that were converting some songs from one format to another but
when I stopped them the DPC issue didn't go away. I tried to disconnect the
USB drive but it wouldn't let me - windows said it was in use. WTF? I wasn't
using it.  
  
One of my office mates was though. He was copying the install for Open Office
off my share. I didn't know that however so I just turned off the drive.
Instantly the DPC problem disappeared. I started the drive back up and the DPC
problem didn't resume for a bit but then, suddenly, it was back. After
stopping the drive again and then having my friend ask what was up with my
drive I put 2 and 2 together. His access of the drive was causing the DPC's.  
  
My initial thought was that maybe there was something wrong with my external
harddrive. So I copied the OpenOffice file to my internal harddrive, shared
it, and then my friend tried to copy it from the new location. DPC Spike! What
a pain!  
  
I don't know why copying stuff off of my computer would cause a CPU usage
spike on my machine but for the time being I am now off the local net with my
share. If anyone knows what might cause the DPC usage and how I can alleviate
it while still helping out my co-workers I would greatly appreciate it!

## Comments

Bill

the problem I am having is definitely related to my external hard drive and
copying files from it.  
  
Three of us in my office have the same laptop and none of us have a DPC
problem normally - regardless what we are doing with them - until the external
harddrive is connected and you try to copy a file off of it.  
  
I didn't know the cause before because I have a shared directory on the drive
that people were copying from. For the time being I have just disabled the
share however, eventually, I'd like to fix the problem.

Anonymous

Probably your video card that's causing the DPC's. I recently installed a new
video card in my machine and would get DPC's that would cause the computer to
come to a crawl. Once the card was removed, the DPC's disappeared. There is a
lot of information on forums regarding the issue, a search of google should
turn up lots of relevant results. I believe it has something to do with the
GPU unit on the video card becoming too hot, either that or a driver issue
with the card.

