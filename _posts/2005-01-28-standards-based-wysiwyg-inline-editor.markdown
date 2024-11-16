---
layout: post
title: "A standards based WYSIWYG inline editor"
date: 2005-01-28
comments: false
category: javascript
tags: [wysiwyg,standards]
---
I just bumped into this cool project that "The Man in Blue" is working on. He
has tried htmlarea, RTE, and FCKeditor and found them all lacking due to their
complexity so he set out to build his own -
[widgEditor.](http://www.themaninblue.com/writing/perspective/2005/01/27/
"widgEditor for standards compliant HTML" ) This is a project that I hope
really succeeds for two reasons.  

  1. Standards Complaint HTML - no ugly font tags floating all over the place
  2. Unobtrusive Javascript
Unobtrusive Javascript is probably the coolest web development idea I have
encountered. Basically with it you don't leave javascript hooks lying all over
the place; instead you use the DOM on the pageload to find what needs to be
hooked into and you take care of it there.  

Later today I will have to write about my unobtrusive sortable tables script.
If you haven't messed with Unobtrusive Javascript at all - you really should.
It makes maintenance SO MUCH EASIER and is very, very slick.  
