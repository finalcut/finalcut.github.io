---
layout: post
title: "Insert Radios in the DOM"
date: 2006-05-31
comments: false
categories:
 - javascript
 - dom
 - ajax
---
In my prior posts about an IE DOM Gotcha I talked about how to insert a radio
button into the DOM dynamically in a fashion that worked in both IE and
Firefox but still failed to work properly in Opera. The problem wasn't getting
the radio button in place - but rather getting it to function as a radio
button. The initial problem in IE was that the radio button couldn't be
selected. Once the IE/FF solution was found the same problem persisted in
Opera. Today, a guy named Torbjorn Gyllebring sent me a function that he
believes takes care of all of our radio-insertion needs.  
  
I honestly haven't had a chance to test it out yet - but I didn't see anything
alarming in a casual glance. Please try it out and see how it works for you.
I'd be particularly interested in hearing how it works in various Mac and
Linux browsers.  
  
```js  
\-----[ Browswer.js follows ]-----  
  
/*  
Browser facade to smooth over the worst misstakes that IE does.  
*/  
  
function Browser(){}  
  
Browser.initIE = function()  
{  
Browser.createInput = function(name)  
{  
var element = document.createElement("<input name='" + name + "'>");  
if(element.toString() == "[object HTMLElement]")//detect Opera masquerade  
{  
Browser.init();  
return Browser.createInput(name);  
}  
else//skip future checks  
Browser.createInput = function(name){ return  
document.createElement("<input name='" + name + "'>");}  
return element;  
}  
}  
  
Browser.init = function()  
{  
Browser.createInput = function(name)  
{  
var element = document.createElement("input");  
element.name = name;  
return element;  
}  
}  
  
if(navigator.appName == "Microsoft Internet Explorer")  
Browser.initIE();  
else  
Browser.init();  
```

