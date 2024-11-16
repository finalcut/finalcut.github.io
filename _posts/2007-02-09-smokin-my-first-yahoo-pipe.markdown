---
layout: post
title: "Smokin My First Yahoo Pipe"
date: 2007-02-09
comments: false
category: general
tags: [yahoo,pipes,yahoo-pipes,music,amazon,last.fm]
---
You may have heard about Yahoo pipes in the past couple of days however, if
you haven't, here is a very basic rundown.  

Yahoo Pipes lets you combine a variety of different data sources (RSS feeds)
and manipulate them to create your own customized feed on the other end.  

Intrigued I decided to setup a pair of pipes that would work together to take
my last.fm recently played list and output a feed that contains links to the
artist at amazon.com so, theoretically, someone could buy the music. Overall
it seems like a pretty simple idea and, in general, it was fairly simple to
implement once I figured out how to use the interface.  

Honestly, there are a few bugs in the interface - for instance on the string
concatenate tool if you bring in a URL to one of the fields it forgets what
part of the URL you want to concatenate whenever you reload the pipe for
editing. However, because my pipes are fairly trivial I don't mind so much -
but if I was dealing with a large complicated pipe that would be a show
stopper.  

The only real "flaw" with this system is that if one of your data sources
isn't available then none of the data comes back. This is an understandable
limitation however it does detract, somewhat, from it's utility, at least for
the pipes I made. Last.fm seems to have some connectivity issues at times and
thus, on occassion, no results are returned.  

You can check out my [Last.Fm at Amazon
Pipe](http://pipes.yahoo.com/pipes/zMGOrlO42xGtP_LkJphxuA/) if you'd like. It
utilizes my [Amazon Webservice Music Search
Pipe](http://pipes.yahoo.com/pipes/QkyOlVO42xGscnc4ZVUMqA/). Enjoy!
