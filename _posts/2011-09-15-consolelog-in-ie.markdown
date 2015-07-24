---
layout: post
title: "console.log in IE"
date: 2011-09-15
comments: false
categories:
 - javascript
 - debugging
 - console
---
If you're like me you've probably been happily working on a web project in
chrome or firefox; using console.log to debug and then tried the site out in
IE and had it fail due to a javascript error. The error? console is undefined
of course. Here is my simple and very limited solution to the problem. At the
beginning of my site, before any other javascript is defined I have this
little snippet:  
```js var console = console || {  
log : function(text){  
/*  
do nothing.. this prevents us from having errors  
in ie when we accidentally leave console.log calls in the js code  
on deployment:  
  
if we want a cheap console in ie just add alert(text); to this outside the
comments  
*/  
  
}  
}  
``` Basically what this does is it checks to see if console is defined, if so
it returns the already defined console object. If the console object isn't
defined, then it returns a new object that contains a method of log. The log
method takes in a value and then does nothing with it. The comment block tells
you how you can make it do a bit more. There are plenty of more feature rich
solutions to this problem out there but, in general, this works for me. It's
lightweight and easy to use. I hope it saves you a few tiny headaches in the
future.  
  
Update, I had a small issue today where the aforementioned wasn't working in
IE8 - I'm not sure why. So here is an alternative:  
```js var console = console || {  
if(!console){  
console = { log: function(text){alert('text'); } }  
}  
```

## Comments

Bill

Thanks Michael. I have used some other similar libraries before but,
oftentimes, I don't need/want anything that heavy and this little snippet
fills the bill perfectly.  
  
  
Typically I try to make sure there is no left over code buried in my JS that
calls console.log, but, occassionally I miss it so having this tucked away in
my production code prevents any silly mistakes from causing a JS error in
production on IE.

Michael

Our intranet is primarily IE so I do must of my testing with it and also
wanted to be able to log to the console. Then I discovered
[fauxconsole](http://icant.co.uk/sandbox/fauxconsole/). Works great, although
it does require linking to JS/CSS files but I limit the use of it to my
development environment.

durbonix

Great post. I've definitely felt your pain.

