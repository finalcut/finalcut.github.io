---
layout: post
title: "Don't Reinvnet The Wheel"
date: 2005-04-13
comments: false
---
Im working on a project now that involves quite a few different parties; our
company, the customer, the customer's agent agency, and then yet another
company (I'll call them Company X) developing another system that our system
must have some interoperability with.  
  
The keystone to the workflow is the system I am working on. However, our
customer has also contracted to have some other system developed by Company X.
I'm not sure of the scope of work involved in Company X's system but I do know
it was recently scaled down and much of the scope was shifted to what I am
working on.  
  
In the end my system needs to be able to export data to their system (I think
they will generate some reports with it). I spoke with their representative
yesterday about what format he wants the export file in (our systems are not
allowed to speak directly) and their Chief Software Architect went down a
slippery path when determining the format of the export file.  
  
Much of the data is stuff entered in a textarea control - so it is pretty free
form stuff that can have any type of character in it. The format I was being
dictated to involved a bunch of delimiters and then I would have to parse the
data to escape any occurances of the special delimiters. At first this wasn't
looking like to big of a deal. He had only specified one delimiter (a pipe |)
but things slowly started going downhill from there. He was also going to use
a carriage return (CR) or line feed (LF) or a combination of the two as a
delimeter. Then he was trying to come up with a multi-character delimiter for
something else. Then he wanted to make up a file extension so a user's browser
woulnd't open the download automatically.  
  
So after listening to all of this I suggested, "Why not just use XML?" I
figure that is what it was developed for - its clean, simple, structured, and
fits the bill perfectly. I'm exporting from a CF5 app and he is importing with
a CF MX app so life would be pretty easy for him. He wasn't so sure.
Eventually their system will be in Java and mine might be in CF 7 shortly
(PLEASE!!!) an XML import would be so much easier than trying to parse a
document with oddly delimeted "lists" of data sets. Sure both are fully
doable. But this guy said he knows Java. If he wanted he could get a jump on
their Java upgrade and just write the importer in Java and leverage that work
with CF MX. And if not CF MX has some pretty useful XML handling operations
built in.  
  
Why reinvent the wheel? Alot of thought went into XML - lets use it!

