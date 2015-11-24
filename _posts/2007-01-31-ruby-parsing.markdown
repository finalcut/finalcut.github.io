---
layout: post
title: "Ruby Parsing"
date: 2007-01-31
comments: false
category: [programming,ruby,coldfusion]
tags: [api,parsing,windows,win32]
---
I had to write a little ruby script the other day - it was really trivial - to
parse a tab delimited file.  

I haven't had much opportunity to use Ruby before (though I have played with
it a little bit) so I was happy for an excuse to try it out. I won't post the
code (it's kind of clunky) but even so I can say, Ruby is fast at parsing
these kinds of files.  

My file was about 2800 rows and 14 columns and almost as soon as I hit enter
on "ruby myrubyscript.rb" at the command prompt it was done parsing the file
and writing the new file (which created a bunch of SQL insert statements for
an upgrade script).  

It was far faster than I expected; blindingly fast. It was refreshing to say
the least. I use CF (not necessarily the right tool for the job all the time)
to accomplish small tasks like this a lot (because CF is so easy) but Ruby was
just as easy and it was definitely faster to complete this type of task.  

One problem I had initially was that Ruby can't generate Guid's natively (or
if it can I couldn't find a reference about it). However, [Brad Wilson posted
a solution](http://www.agileprogrammer.com/dotnetguy/archive/2005/10/27/8991.a
spx) that worked great. It's pretty cool how easy it was to integrate the
win32 api calls into Ruby.

## Comments

Bill

well "Anonymous" thanks for the less than helpful comment.

Anonymous

Anyone who develops in Cold Fusion deserves a good kick in the balls.

Bill

Simeon,  
I can see how you would feel that way. However, I personally don't have that
much of an attachment to any one language primarily because I have to switch
so often at work.  

For example I am currently working on a C# project, a VB.net project, a CF
project, and I'm using Ruby to make some tasks easier.

Simeon

Ok, this will sound stupid, but I have to ask. Do you ever feel like a traitor
when working with ruby?  

I think its important to always expand your skills so I have been learning
ruby and rails. I like ruby because it offers me a new scripting lanugage, as
well as a free web language. It also acts as another backend for my flex work.  

But everytime I start to build something with it I feel guilty, like i am
betraying my CF roots. It sounds so silly but I thought I would see if you
also felt some of that. I know cf is not the right tool for every job, but i
still feel weird. :)
