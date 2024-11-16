---
layout: post
title: "CFMX 6.1 Fails to Start"
date: 2005-11-14
comments: false
category: coldfusion
---
Today I have been wrestling with a problem that popped up out of the blue. My
devleopment machine's CF server wouldn't start. The error log showed that the
Jrun NameService was unable to start on port 2901 and the basic error from
Windows stated check with your vendor about "error 2".

I did some googling to try and find something about the error 2 and the port
2901 bit but kept on turning up blank. I also tried a port scanner since the
details of the port 2901 error suggested it might be in use. The port scanner
showed me that port 2901 was open. Odd.

Then, finally, I found [a technote at Macromedia](http://www.macromedia.com/cf
usion/knowledgebase/index.cfm?id=tn_18799) that discussed a possible solution
- it suggested increasing the default timeout for the CF service to start. The
technote is specifically for CF MX 6.1 but I imagine it applies for later ones
as well since it uses a switch that was first introduced for CF MX 6.1 (so I
can't imagine they got rid of it for 7+).

They say to go to the following direction in the cmd window: \cf-
root\runtime\bin then enter:





```sh
jrunsvc.exe -starttimeout 900 "ColdFusion MX Application Server"
```






The 900 is a variable amout of SECONDS you want CF to wait before it timesout.  The article does not mention what the default is.  I tried this with the 900sec setting and it still didn't work.


Looking at my system resources I saw that FireFox was using 128 MB of RAM.  WTF?  So, I killed FireFox and then tried again.  It worked.  So basically my memory was so consumed my machine was running like a dog and CF couldn't start.


This post is mostly for my own future reference - but it may help someone else out.  If what you are trying doesn't work, kill all the extra programs you can then try to start CF.  The wierdest thing about this was this is the first time I have ever had trouble getting CF to start and I picked today to defend CF Server over at digg.com


Oh, the Irony.





## Comments











anne






Thanks, Thanks, Thanks
