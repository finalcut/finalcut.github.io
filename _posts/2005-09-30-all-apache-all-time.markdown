---
layout: post
title: "All Apache All The Time"
date: 2005-09-30
comments: false
category: apache
tags: [iis]
---
I have had apache 2 installed on my development machine for quite some time.
However, I have almost always used IIS when developing Coldfusion Apps (even
though I had the Apache connector setup on Apache too). Mostly I started IIS
out of habit; plus 90% of my customers use IIS so it just made sense to use
IIS all the time.  

Recently we started a very large PHP project and it has been done using
Apache. However, just because I'm working on that project doesn't mean I can
neglect my other customers so I have been turning one server off and then
starting up another (becuase I hate entering port numbers in a URL and I like
just typing localhost/{website} or whatever.  

So this morning I moved all of my sites over to my Apahce development
directory and setup some aliases for all (but one which needed a virtual
server setup - OH so easy) and everything almost worked perfectly.  

I had to muck with some mappings as the directories I had mapped moved to the
apache dev directory, I had to muck with one datasource (that has a
placeholder access database), and I had to muck with some customtag paths.
Then it worked almost perfectly. I had to go and delete the class files CF had
generated and then restart CF and voila' everything worked perfectly.  

Total time of transition from IIS to Apache apx 20 minutes.  

This is handy cause now on one webserver I can develop in CF, PHP, and Ruby
without any extra work. I know you can use PHP with IIS and maybe you can Ruby
- but it was fairly easy to get Ruby working with Apache so I don't have much
desire to figure it out for IIS. If you want to try Ruby out on a Windows
machine with Apache I have a tutorial up at:
<http://rawlinson.us/blog/?page_id=309>

## Comments

Bill

thanks for the tip - but using the extra domain names don't you have to add
the virtual host in the apache conf file?  

alot of my sites actually are subdirectories at different domains. they are
"sub-applications" at the domain. mostly large organizations with tons of
things going on, used internally (but with public access to the login screen)
so the alias works pretty well for that scenario.

Jeff Coughlin

If your workstation is WinNT (Win2k/WinXP) then you don't have to develop the
sites from alias folders if you don't want to (ie. localhost/site1). This will
also help to eliminating the need to customize mappings and stuff (in other
words, replicate the site as best as possible).  

If you like you can make fake domain names in your host file (default is
C:\windows\system32\drivers\etc\host [ascii file]). What I do is make a local
subdomain for the site (so, if the live site is www.mysite.com, I make my dev
site as local.devsite.com and point Apache to use it accordingly).  

Example host file:  
127.0.0.1 localhost  
127.0.0.1 local.domain1.com  
127.0.0.1 local.domain2.com  

I added localhost to that list in case you still want to use it just like you
are now (and use the newer method for newer projects).  

After editing the file the change is instant (no reboot necessary). If you add
or change a record in Apache you'll need to restart Apache (as I'm sure you're
aware). No CF sessions will be lost.  

\- I have to thank Spike Milligan for the idea (Just trying to give credit
when I can remember :) ).

trib2207

Paul, Apache run something like >65% of web servers, so it's definitely
enterprise class. It should run CF just fine, although for production you will
probably want to tweak and harden it a bit (there are entire books on the
matter).  
Email me offline if you'd like (trib at stephencollins dot org) and we'll see
if we can't get you happening with Apache).

Bill

Well, my setup isn't optimal for either but overall it feels pretty
responsive.  

I didn't do any wierd tweaks mainly because I don't know enough about apache
to tweak it.  

The initial sites I loaded loaded slowly. But that is becaue of the initial
compilation going on. Once things were hit more than once it all seemed to go
pretty well.  

I would say the speed w/cf is about the same on my laptop. However, places I
do gain speed are:  

1\. faster service startup  
2\. faster service restart  
3\. faster to add virtual directories (Alias in apache conf file)  

Other nice advantages so far are  
1\. super easy to setup for multiple "servers" using apache's virtual
directory option in the conf file  
2\. i moved all my sites to c:\dev\websites - which is easier to type for me
than c:\inetpub\wwwroot - trivial true but still nice for me.  
3\. I can reproduce this setup fairly easy on my home PC without needing a
lisence of IIS - nice for consistency in my development environments.

PaulH

how does apache's performance stack up to iis w/cf? we just tried it the other
day and it ran like a dog (out-of-the-box setup, no tweaking). does it require
any modifications/behind kicking beyond running the web connector?  

thanks.
