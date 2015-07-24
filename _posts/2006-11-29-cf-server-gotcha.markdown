---
layout: post
title: "CF Server Gotcha"
date: 2006-11-29
comments: false
categories:
 - coldfusion
 - windows
 - iis
---
I ran into an interesting problem today on a Windows Server box running IIS
and CF 6.1. When we deploy applications to it we typically just blow away the
existing copy of it and replace with the latest release from subversion. (this
is a fairly specialized box that is responsible for one application).  
  
When I did it today something wonky happened and the server locked me out of
the directory that I had tried to delete. It turns out the directory was
deleted but it was deleted pending a reboot of the server. So, since the app
wasn't working and the server was already down for maintenance I rebooted.
When it came back up the directory was gone so I replaced it with the new
version of the app.  
  
Then I hit the app in my browser to make sure it loaded OK and I got the error
index.cfm is not found (the CF error not a 404 error). Weird I thought. I made
a copy of the directory and called it a2 and hit that in the browser and it
worked fine. Hrm, very odd.  
  
I restarted the CF service and voila' the site started working. What gives?  
  
Well I don't have the time to investigate it fully but I suspect it is because
there is a custom tag path and, perhaps, a mapping defined to the applications
directory structure. When the server restarted, and CF first booted up it saw
that a directory it had defined in mapping/custom tag path settings was
missing so it kept track of that information and any request to that directory
subsequently failed. As soon as CF was started with the directory in place all
worked fine.

