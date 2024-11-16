---
layout: post
title: "Google Maps - the good and bad"
date: 2005-02-08
comments: false
category: general
tags: [google,maps]
---
This is an offtopic post: Today Google released [Google
Maps](http://maps.google.com/) and overall it looks pretty slick. This is my
quick and dirty review.  

The good points that I see initially are that the user inteface is very simple
and the download time is very fast. In fact this review is based off of a 30
second run with the site where I found four different addresses and one set of
simple directions.  

However, to offset the pluses there are two negatives as well. First some of
the features are "hidden" and you don't know they will be there until you
happen to find them. Secondly, the download loses some data at times and you
end up with some empty blocks of map. I know they have the missing data
becuase when I repeated the same search the missing blocks would be filled in.
Now, I don't know if this missing data is caused by a wierd FireFox
incompatability or not but it does seem odd.  

As far as the hidden feature goes it is a negative that you have to find it -
but it is cool once you do. I entered my home address and when it loads you
get a waypoint (thumbtack) on the map at the address. Clicking on the waypoint
gives you some options - one of which is "get directions from here" - clicking
on that option loads a form in the same place (a flyout from the waypoint).
The new form simply asks for another address. I entered it and then it loads a
zoomed out map that highlights the route from adddress 1 to address 2. Each
address has a thumbtack on it. Now, if you click on a thumbtack you get a
different flyout entirely. I had thought I would be given the ability to
extend my trip to a third address. Instead it shows a zoom-in view of the area
immediately around the waypoint.  

I think the zoomed in view is pretty cool. I just thought it was less than
obvious you would get that data when you clicked on the waypoint based on the
initial waypoint click experience the application teaches you. Granted, like
many applications now-a-days the event is context sensitive and the
consequences are very easilly learned. However, it still would have been nice
to still have the option to extend my trip to a third address.  

If the flyout that loads the zoom will end up off the viewable map area the
map auto scrolls to account for this and provides you with the ability to see
the entire zoom. Also, the zoom in shows up instantly. I'm not sure yet if
they are using the xmlHTTPRequest object for the zoom in map - or if they
preload the zoom when the initially draw the map. I would imagine, to cut down
on trips between the client and server, that it is all populated on the first
request and the xmlHTTPRequest object is not used for this app.  

Regardless of the technology behind it - or my small nitpicks - it looks to be
a pretty powerful tool that may give competing map sites a run-for-their money
once they move beyond beta stage. If the product team is anything like the
Gmail group then we will see steady improvements to the user interface over
time as well as extended features. I would say that, right now, google is
headed in the right direction.  

UPDATE: well, I just mucked with it some more, using the drag and zoom feature
and now I have changed my mind. They must be using the xmlHTTPRequest object.
The drag and zoom is pretty slick - but I did accidently hit the "recenter"
map button a couple times thinking it was the zoom all the way in button. This
caused me to go back out to the entire North America view and lose what I was
focusing on. It would also be nice if they colored state borders a different
color so that when your zoomed in and panning around you know when you hit a
border - without having to watch out for every towns name.  

UPDATE 2: Check out: [Simon Willison's
post](http://simon.incutio.com/archive/2005/02/08/maps "Google Maps and XSL" )
for a little more information including some insight into googles usage of
XSL.  
