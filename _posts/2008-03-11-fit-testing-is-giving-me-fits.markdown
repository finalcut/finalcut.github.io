---
layout: post
title: "FIT testing is giving me Fits"
date: 2008-03-11
comments: false
categories:
 - fitrunner
 - fitpro
 - antfit
 - ant
 - fit
 - agilifier
---
Maybe I'm just too stupid to figure this stuff out on my own - or maybe the
total lack of documentation is just too big of a hurdle for me but I can't
seem to get any of the available eclipse FIT plugins working quite the way I
need to.  
  
[FitRunner](http://fitrunner.sourceforge.net/) was the first one I tried - and
it worked but it ended up causing heap problems and eventually couldn't be run
anymore. So I removed it.  
  
[FitPro](http://www.luxoft.com/fit/) looked very promising but never seemed to
actually run the simple test I created.  
  
[Agilifier](http://sourceforge.net/project/showfiles.php?group_id=115468) is
being used by a colleague in Hong Kong but our timezones are so off - and the
documentation for it is truly nill, so I'd like to find a different solution.  
  
[AntFit](http://www.cmdev.com/antfit/) hates me. It refuses to execute saying
that the class fit/WikiRunner can't be found. I have fit.jar in my classpath,
I have the antfit task defined as necessary - and I've even set the attribute
useWiki="false" (as well as fork="true") but all to no avail. If anyone has
gotten AntFit to work with useWiki="false" I could really use some pointers.  
  
AntFit is the one I really want to get working simply so we can include it in
our automated builds; but so far no luck. Hopefully someone out there has used
this task and can help me out.

