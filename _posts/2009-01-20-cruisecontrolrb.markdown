---
layout: post
title: "CruiseControl.rb"
date: 2009-01-20
comments: false
categories:
 - ruby
 - java
 - continuous-integration
 - virtual-machine
 - linux
 - cruisecontrol.rb
 - cruisecontrol
 - pivotal-tracker
---
I mentioned in the past that I was going to try to setup CruiseControl.rb on
my CI server. However, there seems to be some kind of conflict in system
settings between CC.rb and vanilla CC (the java version). Thus, I wasn't
really able to proceed since I needed the java version to keep running because
some active projects are being built with it.  
  
I also tried it on my laptop but that ended up causing me some problems
because of my current ruby needs; thus I was kind of stuck. However, I think I
am going to do a couple things to change things up and make it more practical
for me to run CC.rb.  
  
First I'm going to get rid of my ubuntu install. I never boot into it really
and I need the harddrive space back for step 2. The second step is installing
ubuntu in a virtual machine. I'm not sure why I didn't do it that way in the
first place. This will let me continue to work in windows (where all of my
project work is) while also working on getting CC.rb setup. I think this will
give me a great opportunity to experiment and will also give me more time in
linux mucking around.  
  
I will probably take the easy way out of installing CC.rb and that is by using
a handy tool/script pack called
[cinabox](http://github.com/thewoolleyman/cinabox/tree/master) that was
created by one of the authors of a cool tool I like to use called [Pivotal
Tracker](http://www.pivotaltracker.com/).  
  
I'll probably post about my VM setup experience as well as how well cinabox
works out for me. So stay tuned.

