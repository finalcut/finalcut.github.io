---
layout: post
title: "Glutton For Punishment"
date: 2008-11-14
comments: false
categories:
 - ruby
 - coldfusion
 - java
 - continuous-integration
 - cruisecontrol.rb
 - .net
 - cruisecontrol
---
So, if you've been paying attention to my activity lately you'll know I spent
a bunch of time getting CruiseControl to work and to successfully build a
ColdFusion project. You might also know that not every project I do is in CF.
Some are in .Net, some in Java, some (maybe soon) are in Ruby. What I really
need is a single solution that I can use to do CI in all of those
environments; plus I don't want to have to learn how to configure a different
CI tool for each project.  
  
Enter CruiseControl.rb. CruiseControl.rb is a ruby implementation of the
CruiseControl service that will build pretty much any project whose build file
can be called from the command line. I suppose it is possible that the other
CruiseControl implementations can do that as well but I haven't seen any
documentation on it. Thus I'm strongly considering redoing all my recent work
but by using CruiseControl.rb.  
  
This will leave me needing to learn 2 major things. First off how to get
CruiseControl.rb setup in the first place and secondly how to craft a rake
file. Rake is a ruby build file (sort of like make in the C world). Each
project will get its own rake file which will, subsequently, make command line
calls to the projects specific build tool (so Ant or Maven for my CF and Java
projects, Nant or MSBuild for .Net) etc etc. As I did with the standard
CruiseControl I'll try to document my efforts here so the process is painless
for those who follow.  
  
Stay Tuned!

## Comments

Bill

Ant - I talk about it some in the following posts:  
  
[CC, Ant, and SVN](http://cf-bill.blogspot.com/2008/10/cruise-control-ant-and-
subversion.html)  
  
[Setting up MX Unit, ant and CC](http://cf-bill.blogspot.com/2008/10/setting-
up-mxunit-ant-and-cruisecontrol.html)  
  
That second one details my ANT build file a bit. I have a whole collection of
articles discussing my stuff [with ANT](http://cf-
bill.blogspot.com/search/label/ant)

SMHolck

Bill,  
Did you decide to go with Maven or Ant for CF? How is this working out for
you?

