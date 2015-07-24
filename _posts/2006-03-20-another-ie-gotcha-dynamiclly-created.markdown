---
layout: post
title: "Another IE Gotcha - Dynamically Created Radio Buttons"
date: 2006-03-20
comments: false
categories:
 - javascript
 - ie
 - dom
 - ajax
---
As soon as I think I have it all worked out I bump into another oddity between
Firefox and IE and handling the DOM. Specifically adding a radio button (or
set of them) dynamically.  
  
My initial javascript went something like this:  
  
```js  
var rdo = document.createElement('input');  
rdo.type = 'radio';  
rdo.id = 'someUniqueID';  
rdo.name = 'myRadio';  
rdo.value = 1;  
  
myDocumentsBody.appendChild(rdo);  
  
```  
  
This almost worked perfectly. The input was added, it was a radio button, but
it was totally unselectable. I could select it via javascript but the normal
"click" event didn't cause the radio button to assume the "selected" state in
IE? What gives?  
  
Well, I don't know what gives but it turns out I can't assign the type
independently of creating a radio control. Instead, I have to create my radio
object like so:  
  
```js  
var rdo = document.createElement("<input type=\"radio\" name=\"fldID\"
>");  
```  
  
By specifying the type during the creation process the radio button was then
selectable in the normal manner. <strike>This method works inboth IE and
FF.</strike>  
  
Update: 9 May 2006  
Well, as has been reported by many people I was crazy when I said this
technique worked in both IE and Firefox. What was I thinking? It doesn't work
in Firefox at all. However, there is a fairly easy solution that will insert a
selectable radio button in both IE and Firefox - however, I'm sorry to say, it
doesn't work in Opera. Damn these browsers; well, really, damn IE for not
working properly - and damn Opera for not throwing an error when we use IE's
crazy syntax.  
  
So here is the javascript that is needed to create a radio button that will
work in IE and Firefox:  
  
```cfm  
try{  
rdo = document.createElement('<input type="radio" name="fldID" />');  
}catch(err){  
rdo = document.createElement('input');  
rdo.setAttribute('type','radio');  
rdo.setAttribute('name','fldID');  
}  
```  
  
Here is a [demo page](http://rawlinson.us/blog/documents/jsradio.html) \- just
view the page source to see what I am doing and how it works. If anyone has a
good solution that will work in all three browsers please let me know.  
  
Final Update (18 July 2008) - the [demo
page](http://rawlinson.us/blog/documents/jsradio.html) is also updated to
reflect this change.  
  
```cfm  
try{  
rdo = document.createElement('<input type="radio" name="fldID" />');  
}catch(err){  
rdo = document.createElement('input');  
}  
rdo.setAttribute('type','radio');  
rdo.setAttribute('name','fldID');  
```  
  
That works in IE 7, FF 3, Opera 9, and Safari 3.1 for windows.

