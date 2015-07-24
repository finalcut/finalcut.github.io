---
layout: post
title: "Windows 7 : Apache Won't Start on Port 80 - PID 4 Blocking"
date: 2011-05-02
comments: false
categories:
 - sql server ce
 - windows7
 - apache
---
Today I ran into a strange problem where Apache wouldn't start. I kept getting
an error saying it couldn't bind to the socket (I only saw the error detail if
I tried to start Apache from the command line). I then ran the following
command:  
  
netstat -o -n -a | findstr 0.0:80  
  
And saw that something unidentified was listening on Port 80 - netstat
couldn't figure out what but it knew it was assigned Process ID (PID) 4. I
then went to task manager, turned on the PID column, and saw that the NT
Kernel was PID 4. WTF? Why would the OS be listening on Port 80?  
  
Well, it turns out the OS was just sort of acting as a proxy - and I wasn't
getting the full story. Thankfully, a little Googling turned up an[ article
that identified the
culprit](http://www.honk.com.au/index.php/2010/10/20/windows-7-pid-4
-listening-port-80-apache-cannot-star/) for me.. SQL Server Reporting Services
(I installed SQL Server 2008 last week).  
  
I went into the Service manager, killed that service, and bam! Apache started
right up.  
  
  
Crazy.

## Comments

Anonymous

Same happened to me and in my case it was also the World Wide Web Publishing
Service.. Thanks  
  
  
  
  
  
  

Briton

Wow... thank you so much. That's exactly what it was for me too after stopping
at least 20 different services.

Anonymous

I found that windows 7 was running "world wide web publishing service" it was
listning on port 80.  
After I stopped it I was able to run Apachie.  
  
World Wide Publishing Service is used for IIS.

pghn

Hi.  
  
In my case was the service  
"Web Deployment Agent Service"  
that was blocking the port.

