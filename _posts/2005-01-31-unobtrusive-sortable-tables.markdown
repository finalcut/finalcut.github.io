---
layout: post
title: "Unobtrusive Sortable Tables"
date: 2005-01-31
comments: false
category: javascript
tags: [table,sort,html]
---
In my post on the standards compliant HTML editor I mentioned a script I wrote
before dealing with [unobtrusive sortable
tables](http://rawlinson.us/blog/index.php?p=147 "unobtrusive sortable tables"
). If you missed the prior post I'll recap: Unobtrusive javascript is a really
cool way of applying javascript to pages by using the DOM to attach events to
objects. So, instead of hardcoding hooks all over the place, you use the DOM
and element properties (such as ID or className) to attach javascript to the
object.  

This method of adding javascript to your document is great as far as
maintenance goes becuase if the "hook" ever changes you only have to change it
in your initialization method and not all over the place with your code.
Secondly, if your lucky enough to work in a shop that has page designers,
content authors, and then backend programmers the only people who EVER have to
deal with the javascript in your site are the programmers. It is just one more
way to separate presentation and content.  

Anyway, instead of repeating myself I'm going to direct you to my other blog,
where I initially posted about [the sortable table
script](http://rawlinson.us/blog/index.php?p=147 "unobtrusive sortable tables"
). Hopefully it helps you and perhaps, even better, inspires you to start
using unobtrusive javascript. As always when I dicuss this particular script I
want to give credit where it is due: Stuart Landridge
([kyrogenix.org](http://kyrogenix.org/)), Scott Andrew
([scottandrew.com](http://scottandrew.com/)), and Mike Hall
([brainjar.com](http://brainjar.com/)) all provided prior work in this area
that led to my solution. If it weren't for their efforts and the commentary of
Stuart advocating unobtrusive javascript I may never have heard of, or tried
to implement, this idea.
