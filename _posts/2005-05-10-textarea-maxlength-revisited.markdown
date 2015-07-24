---
layout: post
title: "textarea maxlength revisited"
date: 2005-05-10
comments: false
categories:
 - javascript
 - maxlength
 - textarea
---
NOTICE: I updated all of the JS in this post on 5/24/2005 as there was some
cut-n-paste problems before. If you got the code from here before then, please
get it again now. You can also [download the file from
here](http://rawlinson.us/blog/codesamples/textareaMaxLen.js)[
](http://rawlinson.us/blog/codesamples/textareaMaxLen.js)



Yesterday I posted some code showing how to add, in a fairly unobtrusive
manner, a maxlength property and behavior to the textarea control using the
fundamental idea of "unobtrusive javascript". Today, I am going to expand on
the idea a little.

Basically, If I am using a textarea odds are good that my maxlength value is
going to be large. Becuase of that I want to give the user some form of clue
as to how much of the textarea's capacity they have used. Since this needs to
change dynamically it seems appropriate that I do this as part of the code
that also limits the size of the textarea.


```js
<script type="text/javascript">
function textAreas_init() {
/*
I initialize all textareas and send them to the addMaxLength method

@return null
@see addMaxLength()
*/
if (!document.getElementsByTagName) return;

objs = document.getElementsByTagName("textarea");
for (oi=0;oi<objs.length;oi++) {
thisObj = objs[oi];
// this part enforces the maxLength
addMaxLength(thisObj);
}
}

function addMaxLength(thisObj){
/*
I replace the onkeyup event of a textarea with a new action, forceMaxLength. I
also
insert a sibling object that displays the current areas content length

@param thisObj required the object whose content length we are constraining
@return null
@see forceMaxLength()
*/
if (thisObj.getAttribute('maxLength')){
thisObj.onkeyup = forceMaxLength;
insertSpanSibling(thisObj,thisObj.value.length + '/' +
thisObj.getAttribute('maxLength') + ' of maximum length used');
}
}

function forceMaxLength(){
/*
I replace an event on a textarea forcing the length of the textareas content
to be within the maxLength constraing

@return null
*/

var maxLength = parseInt(this.getAttribute('maxLength'));
if(this.value.length > maxLength){
this.value = this.value.substring(0,maxLength);
}

this.nextSibling.innerHTML = this.value.length + '/' + maxLength + ' of
maximum length used';
}


function insertSpanSibling(obj,msg,cssClass){
/*
I add a span after the current object
@param obj required the object that is getting the sibling inserted after it
@param msg required the contents of the sibling
@param cssClass not required a class name for the new sibling
@return null
*/


var newSpan = document.createElement('SPAN');
newSpan.innerHTML = msg;
obj = obj.nextSibling;
if(obj.readOnly)
obj = obj.nextSibling;
if(cssClass)
newSpan.className = cssClass;

obj.parentNode.insertBefore(newSpan,obj);
}

function addEvent(elm, evType, fn, useCapture)
// addEvent and removeEvent
// cross-browser event handling for IE5+, NS6 and Mozilla
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


</script>

```


As you can see I didn't do a whole lot of new stuff. However, I did clean up
the code some and make it a bit easier to use. It would probably be a good
idea to move the code the updates the tooltip text out into its own function
that would identify if the tooltip existed and create it if it didn't, other
wise update it. I should probably also update the insertSpan function to take
an ID value for the new span so that it would be easier to identify if the
tooltip is there.

