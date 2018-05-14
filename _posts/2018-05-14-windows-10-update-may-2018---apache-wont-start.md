---
layout: post
title: "Windows 10 Update May 2018 - Apache Wont Start"
description: Windows 10 May 2018 Update stopped Apache start.  The fix is simple!
headline: 
date: 2018-05-14 09:23:25 -0400
category: windows,development
tags: []
imagefeature: 
mathjax: 
chart: 
comments: true
featured: false
---
Today I came into the office to find my machine was waiting to apply a big Windows 10 update.  So I applied it and when it was done I couldn't start Apache.  The Apache logs showed nothing and the System Log showed a pretty useless error

```log
The Apache2.2 service terminated with the following service-specific error: 
Incorrect function.
```

I initially figured some service had been started that was blocking port 80 so I dug into the services and saw that `World Wide Web Publishing Service` was started automatically now (i set this to manual all the time).  So I stopped it and set it to manual but Apache still wouldn't start.

So I ran `netstat -o -n -a	findstr 0.0:80` and saw that something was running on port 80 with PID of 4.  [That seemed familiar](http://code.rawlinson.us/2011/05/windows-7-apache-wont-start-on-port-80.html).  So I looked around for the `Web Deployment Agent Service` and lo-and-behold it too was running automatically again. So, I turned it off and set it to manual.  Tried Apache again and bam; everything worked fine.


