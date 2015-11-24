---
layout: post
title: "Model-Glue - faster than I thought it was"
date: 2005-11-04
comments: false
category: coldfusion
tags: [modelglue,framework,mvc]
---
Ok, so Dave Ross told me to turn off debugging in CFADMIN - and I didn't
listen to what he said exactly - and that in turn led me to a false
conclusion.  

Well, my lack of understanding of exactly what happens when you use cfsetting
showdebugoutput led me into trouble.  

All these years I have been under the false impression that turning off debug
output actually turned off the debugging for the request and thus I wouldn't
need to turn it off in the CFADMIN console for a specific app. Wishful
thinking on my part I guess.  

I turned off debugging in CFADMIN and now all my simple MG pages load in
30-100ms: a VAST improvement.  

I apologize Dave that you had to tell me twice.

## Comments

Anonymous

hey don't apologize! glad to help!  

-Dave

Anonymous

Just a note that debugging affects ANY CFC-heavy application in a huge way.
Fusebox, Model-Glue, Mach-II, homegrown...any app that uses lots of CFCs and
method calls absolutely must have the option "report execution times"
unchecked. But if you want to be totally sure, just disable debugging
completely.  

Brian Kotek
