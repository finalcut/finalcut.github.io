---
layout: post
title: "If You Can't Beat Em..."
date: 2009-04-06
comments: false
categories:
 - herald-dispatch
 - calendar-aggregation
 - ics
 - newspaper
---
No, I am not going to say join 'em. I live in Huntington, WV - it's a small
city on the western most edge of WV with a population of around 40,000 people.
It's a great little place with an abundance of things to do the trouble is it
has always been hard to discover what all those things are.  
  
Fortunately, things are changing for the better in that regard. The net is
making things much easier and, thankfully, our local newspaper, The Herald
Dispatch, is helping everyone by offering up an online event calendar. They
have a full time person on staff whose job is almost entirely consumed with
keeping the calendar up-to-date. It's fantastic. Sadly, however, it isn't
published as an ICS feed; instead the only interface to the system is via
their web widget. The staff at the paper are happy to share the widget with
websites that want to display the calendar but honestly I just didn't think it
was enough.  
  
I really want an ICS feed to be available for that calendar. It has 6000+
events stored in it for the upcoming months and they are each categorized and
sub-categorized. By providing a feed for all of these events that can be
broken down by category the citizens of Huntington and the surrounding area
can keep track of events in whatever fashion they want. If they want to
subscribe with Outlook or Google calendar they could and it wouldn't hurt
traffic flow via events to the newspapers website at all - instead I think it
would have the net effect of increasing traffic.  
  
Fortunately, the folks at the paper agree. In fact they have been great about
the idea and instantly bought into it! However, they didn't have anyone
available to create the script that would generate the ICS feed from their ad-
hoc database of events so I volunteered to do it for them. Amazingly, even
though this is an old company, they nimbly accepted my offer and put me in
touch with the right guy. That day (last Thursday) I had the schema
description, a dump of two months worth of events, and a basic overview of
their current calendar's architecture so I could get my work to fold in
seamlessly. Last Friday I delivered the first iteration of the script!  
  
Honestly, the script was a piece of cake to write thanks to having a pretty
[clearly defined standard](http://www.ietf.org/rfc/rfc2445.txt) to write
against and the invaluable tool that is the online [ICS
validator](http://severinghaus.org/projects/icv/) plus a few nudges in the
right direction from Wikipedia. Wikipedia has [a chart that shows various
elements and how they apply to different types of data in the
ICS](http://en.wikipedia.org/wiki/File:ICalendarSpecification.png). I used
that chart to help navigate the standard which is very lengthy.  
  
I'm not sure when it will go live but I'm super happy the paper was so forward
thinking and open to my suggestion and my offer to help. [The Herald
Dispatch](http://www.herald-dispatch.com/) does a great job of being focused
on the local community, its news, and needs and I think this is another
example that highlights their commitment to the community. I'm thankful that
the small team I've been working with has been so helpful and open to my
suggestions!

