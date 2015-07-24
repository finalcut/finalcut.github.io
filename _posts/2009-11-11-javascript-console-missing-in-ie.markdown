---
layout: post
title: "Javascript Console - Missing in IE?"
date: 2009-11-11
comments: false
categories:
 - javascript
 - logging
 - debugging
 - console
---
Ok so lets say your hacking away at your favorite web app using Firefox or
Chrome and your dropping some "conole.log()" calls around to help you debug.
Then you try the site in IE and it doesn't work. You look at the javascript
error and you see that "console" is undefined.  
  
You don't really want to have to remember to change your console.log() calls
to alerts or something else when you test in IE so what do you? Well, it's
easy to fix actually. Just plop this bit of Javascript in your file and worry
no more.  
```js  
if(console === undefined){  
function _console(){  
return {  
log : function(v){  
alert(v);  
}  
  
}  
}  
var console = new _console();  
}  
```  
  
Admittedly that is a pretty weak implementation of the console.log() but it is
a good starting place for you. If you want you can extend that do do things a
little better (like append the log messages to the bottom of your webpage) but
you get the basic idea. Enjoy!  
  
Here is a slightly better version to give you an idea how you might extend it
(requires the $ function such as that found in JQuery):  
```js  
if(console === undefined){  
function _console(){  
return {  
log : function(v){  
this.prepLog();  
var l = '<tr><td>'+v+'</td></tr>';  
$('#divConsoleLog').append(l);  
},  
prepLog : function(){  
if(!$('#divConsoleLog')[0]){  
var d = '<table
id="divConsoleLog"><caption>Console</caption></table>';  
$('body').append(d);  
}  
}  
}  
}  
var console = new _console();  
}  
  
```  
  
Unsurprisingly, someone had this idea before me and they have a more feature
rich implementation - check out "[faux
console](http://icant.co.uk/sandbox/fauxconsole/)" - but for whatever reason
his didn't work for me and I don't feel like debugging it. However, his style
sheet is pretty much just what I want:  
  
```css  
#divConsoleLog{  
position:absolute;  
top:0;  
right:0;  
width:300px;  
border:1px solid #999;  
font-family:courier,monospace;  
background:#eee;  
font-size:10px;  
padding:10px;  
}  
html>body #divConsoleLog{  
position:fixed;  
}  
#divConsoleLog a{  
float:right;  
padding-left:1em;  
padding-bottom:.5em;  
text-align:right;  
}  
```

