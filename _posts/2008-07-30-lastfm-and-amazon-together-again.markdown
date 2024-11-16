---
layout: post
title: "Last.Fm and Amazon Together Again"
date: 2008-07-30
comments: false
categories:
 - last.fm
 - yahoo
 - amazon
 - yahoo-pipes
 - amazon web services
 - mashup
 - aws
---
A [while ago](http://cf-bill.blogspot.com/2007/02/smokin-my-first-yahoo-
pipe.html) I debuted my first Yahoo Pipe; [last.fm @
Amazon](http://pipes.yahoo.com/finalcut/lastfm_amazon) that basically took
your listening list and did a lookup on amazon. The idea being that anyone who
could consume an rss feed could then monetize their listening habits.  
  
The cool thing about Yahoo pipes are that you can mashup a bunch of different
services into one nifty data source. That trick, I have discovered, is that
not all of the data sources you use necessarily remain the same. A case in
point is the Amazon Web Service which, at some point between now and Feb 07
has changed to requiring a new token to identify the developer who is making
the service call and a different sort by enumeration.  
  
Needless to say my pipe had broken. Fear not however as I managed to get it
back up and working in almost no time. I did learn a valuable lesson in doing
so though - don't accidentally delete your pipe! Fortunately, a bunch of
people had cloned my old broken pipe so I was able to "re-clone" it so to
speak and get it going again without much trouble.  
  
Finally, if you don't really care how the pipe works but would like to use it
you can use the following URL as the feed URL you want to display in your blog
(or feed reader)
http://pipes.yahoo.com/pipes/7d20665c0dc0240fd18516ec360efe21/run?_render=rss  
  
You can append the following to the URL if you want to provide your own
last.fm username and/or amazon associate ID;  
  
&amp;username;=YOURUSERNAME&amp;associateTag;=YOURASSOCIATEID  
  
Just replace YOURUSERNAME with your last.fm username and YOURASSOCIATEID with
your amazon associate id. Just note if you publish this feed anywhere and you
don't provide an associateTag value it will use mine by default; granted, I
wouldn't mind that - but I figured i should tell you.

