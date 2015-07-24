---
layout: post
title: "Upgrading Eclipse"
date: 2005-02-01
comments: false
---
I currently have Eclipse 3.0 installed on my system. I would like to upgrade
to stable build Eclipse 3.1 M4 however I can't find any good definitive
information on the topic. What I found [here](http://help.eclipse.org/help30/i
ndex.jsp?topic=/org.eclipse.platform.doc.user/tasks/tasks-2.htm) tells me I
need to extract the new version to a directory different from my 3.0 version.
But which archive do I download? I'm also going to use the -data flag as the
link suggests and move my workspace to a more generic location out from under
my eclipse install.  
  
When I go to [download from the a mirror](http://www.mirrorservice.org/sites/d
ownload.eclipse.org/S-3.1M4-200412162000/) or anywhere else from that matter
the differences in each file aren't really explained. Since I already have the
sdk installed can I download one of the smaller archives or do I need to go
for the full 50+ meg monster? Do I even need the SDK or do only folks who are
working on Eclipse plugins need the SDK while the rest of us can get by with
the platform?  
  
Also, if I can just get by with the platform and not the entire SDK - will it
be a bit more responsive? I know my machine isn't that great but sometimes
Eclipse is a real chore to use due to "laggish" behaviour. I installed a
[plugin that helps](http://suif.stanford.edu/pub/keepresident/) some - but it
is by no means a cure. If you have any suggestions/tips/ideas or anything
please leave a comment.  
  
I'm going to download the vanilla platform for now and see if the plugins I
use typically will work with the platform and not just the SDK. I'll update
this post later with anything I find.  
  
UPDATE  
well it seems that the platform is sufficient for my needs. However, I keep
getting an error message when I try to close eclipse. I will post more here
once I figure out what is causing the error, and how to fix it.  
  
UPDATE 02 FEB 2005  
Well, i figured out what the problem was - sort of. I had been starting
Eclipse with the -data and -vm flags as suggested by the help article I
referenced earlier. Going back to starting it without it prompted me for the
workspace to open and it had a checkbox to make the selected workspace the
default. By picking the workspace location instead of specifying it via the
-data flag and telling Eclipse that it was default the shutdown error went
away.  
  
I am presuming the error was caused by Eclipse not being properly initialized
and not knowing where to save some data. I have not been able to reproduce the
error since I made the change.  

