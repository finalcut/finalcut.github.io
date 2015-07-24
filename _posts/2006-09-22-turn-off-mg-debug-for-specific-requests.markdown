---
layout: post
title: "Turn off MG Debug for specific requests"
date: 2006-09-22
comments: false
categories:
 - coldfusion
 - cfc
 - ajax
 - xml
 - model-glue
 - debugging
---
It's funny how when one person is looking for an answer to a problem it seems
a bunch of other people are looking for the same thing, at the same time. As
it turns out this is exactly what happened to me today.  
  
I was working on creating a MG app that has some "AJAXy" goodness in it. I
want to leave the MG debug stuff on while I'm working (sometimes) but never
want it to output in an "XML" view (that which is returned to the AJAX
request). I figured it had to be possible and sure enough some other people
were just [asking Ray Camden a couple days
ago](http://ray.camdenfamily.com/index.cfm/2006/8/22/Using-AJAX-with-
ModelGlue).  
  
Thankfully, Jan Jannek, posted a comment reply with the answer:  
```cfm  
<cfset request.modelGlueSuppressDebugging = true />  
```  
Just stick that code in your XML view and debug output won't be shown. Ray
also posted a [blog entry](http://ray.camdenfamily.com/index.cfm/2006/9/18
/Per-request-debugging-in-ModelGlue) that covers this. I'm just recovering the
topic in case anyone missed this then.

