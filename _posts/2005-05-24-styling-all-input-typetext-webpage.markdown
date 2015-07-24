---
layout: post
title: "Styling All input type=text webpage controls"
date: 2005-05-24
comments: false
categories:
 - javascript
 - css
---
CSS provides the facility to use selectors in order to narrow down your style
application to a subset of controls. For instance, if you want to apply a
style to all input boxes of type text there is a css selector to help you do
that. Sadly, the selector won't work in IE. But, thanks to unobtrusive
javascript there is a solution.

Using the power of the DOM and the very useful method "getAttribute" we can
apply a class to all input boxes of type text, or checkbox, or radio - or
whatever.

Now, if your using Firefox or Opera this isn't really required. And who knows,
maybe someday IE will support full CSS selectors as well. When that day comes
it will be easy to remove by just cutting out the line that adds the event.

Before we get into the code first I'll show you the CSS way of doing it!






```html
<style type="text/css">

 input[type=text] {

  background: red;

 }

</style>


```




Now, in order to illustrate I provide the javascript/css code that makes it work in IE as well.






```html
<html>

<head>

<script type="text/javascript">

function addEvent(elm, evType, fn, useCapture)

// addEvent and removeEvent

// cross-browser event handling for IE5+,  NS6 and Mozilla

// By Scott Andrew

{

  if (elm.addEventListener){

    elm.addEventListener(evType, fn, useCapture);

    return true;

  } else if (elm.attachEvent){

    var r = elm.attachEvent("on"+evType, fn);

    return r;

  } else {

    alert("Handler could not be removed");

  }

}



function prepareTextBoxes(){

 if (!document.getElementsByTagName) return;

 var oi=0;

 var thisObj;

 var objs = document.getElementsByTagName("input");



 for (oi=0;oi<objs.length;oi++) {

  thisObj = objs[oi];

  if(thisObj.getAttribute('type') == 'text'){

   thisObj.className = 'text ' + thisObj.className;

  }

 }

}


addEvent(window, "load", prepareTextBoxes);


</script>


<style type="text/css">

 .text {

  background: red;

 }

 input[type=text] {

  background: red;

 }

</style>

</head>

<body>



<input type="text" name="1" value="test1" /><br />

<input type="text" name="5" value="test5" /><br />


<input type="text" name="2" value="test2" /><br />

<input type="text" name="3" value="test3" /><br />

<input type="text" name="4" value="test4" /><br />



</body>

</html>


```




Now, you may notice that I prepend the class "text" to the className field as opposed to appending it.  I do this so it is a bit more like a real application of a class to a text area.  This way, any classes you manually assign to the text field will override the default behaviors defined in class text.


If you wanted to do the same for checkboxes or radio buttons you could just change one line of code:


```js

  if(thisObj.getAttribute('type') == 'text'){

or

  if(thisObj.getAttribute('type') == 'radio'){

or

  if(thisObj.getAttribute('type') == 'checkbox'){


```




Jur remember that javascript is case sensitve (and always use lowercase with HTML) and you'll be good to go.





## Comments











KairosDrasis






@ricardo


There actually is an (odd way) to get it to work in blogger.


replace all occurrences of < with <

replace all occurrences of > with >


Somehow blogger parses this server-side before sending it to the client, thus your JavaScript code actually remains intact.  Generally this is used for HTML, but blogger is odd...











Bill






I think you need to add a javascript module to the page to add the javascript because right now it is taking the < and thinking you are trying to open a tag no using as a less than symbol.











Bill






I never tried this on blogger.  I am not sure we can add javascript to the  template; or if we can I haven't done it before.  sorry.











Ricardo Sousa Martins






hi, great work, i did find a problem though. blooger doesnt accept the code very well..


'Your template could not be parsed as it is not well-formed. Please make sure all XML elements are closed properly.

XML error message: Element type "objs.length" must be followed by either attribute specifications, ">" or "/>".'


any way around this?

ricardo











Bill






ronx,

yes the styles will work if they are an external included css file.











ronx






Bill, I'm somewhat a newbie on CSS ... I'd just like to confirm, the technique'll still work if the CSS bit (the one below)


<style type="text/css">

 .text {

  background: red;

 }

 input[type=text] {

  background: red;

 }

</style>


... was stored in a separate CSS file? I wouldn't want to place the same CSS in each HTML I'm creating... Hehehe thanks!











Bill






thanks for the clarification Anthony.


So the order that the classes are defined as CSS classes is all that matters - the order they are applied to an element is immaterial.


I think I will continue to apply them in the order they are defined (if possible) so that it is easier for me to tell what classes on an object take precedence.











Anthony Jones






You state that by appending the any existing class names after the extra 'text' class name causes the any existing classes to have priority.


This isn't in fact true.  The order of class names defined on the element is immaterial.  It is the order the selectors are found in the document that affects the order the styles get applied.


Hence for you technique to work the .text class needs to be defined early in the document.











Chris






finally who uses the the possibility to style type's of input.


I was looking for this, but all i found was the usage of classes to style checkboxes, radiobuttons, text's, ...


nice work !










