---
layout: post
title: "Name Your Objects Carefully"
date: 2005-07-27
comments: false
---
I spoke about this briefly earlier this month on the CF-DEV mailing list but
thought I should put a reminder here for posterity sake. Sometimes the most
obvious name for a CFC is not the best.  
  
For example, I was modelling an application that dealt with student
enrollments in classes. I had defined a student object, a class object, a
studentenrollment object, an address object and some others.  
  
The studentenrollment object consisted of the student info, the class info,
and a bunch of other information regarding the students performance in the
class.  
  
All of this was working fine until I went to instantiate the class object and
do something with it. I can't remember what it was I tried to do but CFMX
threw an error saying that CLASS was a reserved word in ColdFusion. Now, it is
kind of obvious once you see it - especially when you consider that CFMX is
just a Java wrapper - but I was kind of shocked at first since CLASS isn't
defined as a CF reserved word.  
  
Because the CF documentation never mentions CLASS being a reserved word you
need to be careful to consider not just [CF reserved words](http://livedocs.ma
cromedia.com/coldfusion/7/htmldocs/wwhelp/wwhimpl/common/html/wwhelp.htm?conte
xt=ColdFusion_Documentation&file=part_cfm.htm) but also [Java reserved words](
http://java.sun.com/docs/books/tutorial/java/nutsandbolts/_keywords.html). I
ended up using an alternative name for my object but had to spend some time
refactoring due to the rename.  
  
So save yourself the trouble in the future and carefully choose your object
names bearing in mind words that may be applicable but are reserved by more
than just CF.  
  
Here are some links that might be useful to you:  

  

  * [CF Reserved Words](http://livedocs.macromedia.com/coldfusion/7/htmldocs/wwhelp/wwhimpl/common/html/wwhelp.htm?context=ColdFusion_Documentation&file=part_cfm.htm)
  

  * [Java Reserved Words](http://java.sun.com/docs/books/tutorial/java/nutsandbolts/_keywords.html)
  

  * [MS SQL Reserved Words](http://msdn.microsoft.com/library/default.asp?url=/library/en-us/tsqlref/ts_ra-rz_9oj7.asp)
  

  * [Oracle 8 Reserved Words](http://www-rohan.sdsu.edu/doc/oracle/server803/A54656_01/vol2_wor.htm)
  

