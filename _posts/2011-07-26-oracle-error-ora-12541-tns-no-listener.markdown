---
layout: post
title: "Oracle Error: ORA-12541 - TNS: no listener"
date: 2011-07-26
comments: false
categories:
 - oracle
---
I was on vacation last week and when I returned, I could no longer connect to
my local Oracle instance. My C# apps and PL/SQL developer both reported a
ORA-12541 TNS: no listener error.  
  
I hadn't changed anything before I left and I certainly hadn't changed
anything as soon as I got back so I was a little perplexed. Fortunately, there
was a pretty easy solution which I extracted from [The Oracle
FAQ](http://www.orafaq.com/wiki/ORA-12541).  
  

  1. Check your listeners status by going to the command line and entering the Listener Control Program using command LSNRCTL. Once in the program enter the command: STATUS  
  
  
The tool suggests you also start and stop the listener but that had no effect
for me. My listener just didn't want to work.  

  2. Recreate your listener. Again, go to a command prompt but this time open up the Network Configuration Assistant using the command: netca
  3. Inside this tool you first need to delete your listener. Mine was actually called "listener" and I just accepted all of the defaults when deleting it. Once it is deleted, recreate it, again I used all of the defaults.
  4. After it was created I went back to the Listener Control Program (LSNRCTL) and ran the STATUS commaned. This time it looked pretty good and, sure enough, my apps and PL/SQL Developer were able to connect to the database.

## Comments

jai

thanks for no listener issue resolution steps.It worked for me.

