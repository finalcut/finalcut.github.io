---
layout: post
title: "Firebug and Gmail - make friends!"
date: 2006-08-29
comments: false
categories:
 - gmail
 - firebug
---
This is my final post, I hope, on the topic of Firebug and Gmail
compatability. A recent reader of my blog has posted a [xpi hack that will get
Firebug to not interact with Gmail ](http://www.paulchaplin.com/blog/firebug-
and-gmail-friends-at-last/)at all so you can keep a Gmail tab open and keep
Firebug active.  
  
If you decide to edit the xpi yourself I have summarized the code change here:  
  
```js  
FireBug.isWindowInspectable = function(win)  
{  
var isOK = false;  
  
if(win.location.href != "about:blank" &&amp;
win.location.href.indexOf('mail.google.com') == -1){  
isOK = true;  
}  
  
  
return isOK;  
  
}  
```  
  
This change goes in the following file:  
  
<your documents and settings path>\Application
Data\Mozilla\Firefox\Profiles\<your profile>\extensions\firebug@software
.joehewitt.com\chrome\firebug.jar\content\firebug\firebug.js  
  
After you make the change just restart your browser to have it take effect.
Before making any changes though I encourage you to [read his blog
post](http://www.paulchaplin.com/blog/firebug-and-gmail-friends-at-last/). It
provides much more complete and step -by- step instructions or an alternative
already edited XPI file you can install.  
  
Thanks Paul

## Comments

Bill

thank you for digging in and finding the hack.  
  
I should have done the same but the thought never even occured to me. I'm
getting lazy I guess :O)

Paul Chaplin

Ah, update: just after bumping that thread, I saw Joe's [recent blog post
about FireBug](http://www.joehewitt.com/blog/next_firebug.php) \- someone had
already posted a comment requesting domain filtering, so I echoed it. Here's
hoping!

Paul Chaplin

Glad I could help, and thanks for posting about it. :)  
  
I'll be keeping my fingers crossed that Joe will add a GUI blacklist (and
possibly whitelist) option soon, since someone else [requested
it](http://www.joehewitt.com/software/firebug/forums/viewtopic.php?t=14) a
while back on his forum (and I just bumped it).  
  
If that doesn't happen, I'll see about doing it myself, to make the current
solution more generalised - it can't be just us and just Gmail experiencing
problems.  
  
Cheers Bill.

