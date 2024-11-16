---
layout: post
title: "Unit Testing Really Is Great"
date: 2007-12-12
comments: false
categories:
 - nUnit
 - unit-testing
---
Everyonce in a while I work on something that reminds me how great unit
testing is. No, it isn't the end all be all of testing - but boy, it sure does
make your life a lot easier if you use it.  
  
For example, tonight I was working on an object we will call "COMPONENT" and
the component has a collection of objects called "CURVES" and each curve has a
collection of "POINTS". The COMPONENT has two dates associated with it - a
basis date and a cut off date. If the basis date changes any POINT on the
CURVEs with a date after the cutoff date have to shift the same amount of time
as the basis date just shifted on the change.  
  
This kind of thing would be a real bear to test any other way besides unit
testing. With unit testing I was able to quickly craft some tests that shift
the basis date forward and backward and check all sorts of random POINT date
values - and their value relative to the basis date AND make sure the dates
before or on the cutoff date don't shift. I can't imagine testing this sort of
situation so completely without unit testing.

