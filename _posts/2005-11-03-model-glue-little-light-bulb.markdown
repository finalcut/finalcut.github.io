---
layout: post
title: "Model Glue - a little light bulb"
date: 2005-11-03
comments: false
category: coldfusion
tags: [modelglue,framework,mvc]
---
Today I was reading the MG mailing list (at topica, ugh :( ) and I saw
something that _should_ have been apparent in the first place but that I
missed.  

You can have multiple controllers.  

I know, if I had just paid attention to ModelGlue.xml I would have realized
this but I didn't. Instead it took a message from Nando to Joe and Joe's reply
back in March to make this feature obvious to me.  

I was getting kind of concerned that my controller would get huge and unwieldy
with so many different things being controlled in one file. But with multiple
controllers I can logically separate things which, to me, is pretty important
from a maintenance perspective.  

Obviously the temptation may arise to have too much controller separation -
but I don't think that will be an issue. However, right off the bat I can see
some handy dandy uses for the separation.  




  1. Security - I think I would probably like to have all of my security accessed through a security controller. Any security related message (checkIsValidUser, userHasPermission, userIsLoggedIn, etc, etc..) would be handled by the Security Controller.


  2. Actions - I really don't like having purely action based events handled in the same controller as events that are basically just view generating events. I like to know that my actions (save, update, etc) are going to occur in one place that will be easy for me to scan, while my drawing events (showItem, listItems) etc are in another easilly scanable location.


  3. AJAX - I tend to treat xmlHttpRequets kind of special so I like the fact I can have a singular controller for AJAX type requests. Typically I have just a few (1-20) different AJAX events I might need to handle in an app that I am using AJAX with so having them pushed into their own controller should make maintenance eaiser (this is how I did things pre-MG so it also fits into my workflow nicely)



If you can think of a reason why separating some of these things into separate
controllers is a bad idea please share your thoughts with me. The whole point
of me digging into MG in the first place is to learn something new - so shoot
me down if I need it!  

\--- further update ----  
I still think MG runs a little slow so I'm wondering if maybe it is my
machine. I have debugging turned off for this app (cfsetting showdebugout=0)
and the MG debugging turned off, but I do use getTickCount onRequestStart and
then at the end of my main template I output the difference (getTickCount -
request.mystartTickCount) and it is always well over 1 second to show a pretty
simple page. In fact my little apps home page just loads two views (a content
view and the wrapping template view) and renders them. No DB hits, nothing.
Yet I haven't seen a time below 1200ms - and I have seen times as high as
2100ms.  

Anyone with a suggestion? While I don't need instant respones they do need to
be faster than this, especially since the site is being hit by 1 person (me)
and it is being hit directly (same machine has the server and the client). I
can imagine what would happen under load - and I don't think it would be
pretty.  

\--- further timer update ---  
well, it appears that maybe my timer was not working perfectly. I tried
putting it very simply in application.cfm and in a new onRequestEnd.cfm -
which did work but maybe wasn't accurate.. I'm not sure  

When I put my timer in onRequestStart (of my controller) and onRequesteEnd
(which I force a broadcast of during my main template layout) the timer is
close to 500-700ms on the simple page. I'm sure by doing it this way I'm
cutting out some stuff (ie the final rendering, but it does give me a better
idea of the time involved upto that part. I'm still eager to here any thoughts
anyone has on performance with MG.

## Comments

Bill

Thanks for the heads up on that Sean.

Anonymous

Another setting that can have a pretty dramatic effect on Model-Glue
performance is Trusted Cache. Because there are so many CFCs being created on
each request, the overhead of checking file last modified timestamps for each
instantiation is enough to make a difference to execution time.  

Obviously you can't have Trusted Cache on for developement machines but it's
just something to bear in mind.  

\- Sean Corfield

Bill

Dave, I'm sort of embarassed to say I didn't realize turning off debugoutput
in the cfapplication tag didn't actually stop the debugging from happening.  

What a pain.  

thanks  
Bill

Anonymous

Bill,  

Have you turned off debugging in CFAdministrator? The slow execution times due
to CF Debugging are not due to it being displayed, just it happening while the
request is executing.  

-Dave Ross

Raymond Camden

I wasn't aware of this feature at first either. Hopefully with more and more
MG apps out there people wil be able to learn from one another.
