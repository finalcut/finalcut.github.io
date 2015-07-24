---
layout: post
title: "Extend Your Select Box"
date: 2005-05-27
comments: false
categories:
 - javascript
---
Since javascript is a nice object oriented language you can do some pretty
cool things with it. For instance you can extend the functionality of various
objects - such as the SELECT box control.

About 4 years ago when I first wrote an application that used "AJAX" like
techniques one thing I needed to do was dynamically populate a select box
based on the selections of other select boxes, radio buttons, and text fields
(LOTS of business rules). Obviously, at that point the app was IE only since
they invented the whole xmlHttpRequest object. Anyway, I digress.

What I needed was some simple functionality that would add new options, remove
options, clear options, or insert options within an existing SELECT. These are
the scripts I came up with.


```js
/***********************************************

Basic Javascript library that adds extended
functionality to some standard objects used
in javascript and an html document.

***********************************************/





/********
STRINGS
********/
// like Trim( ) in vbscript. removes trailing and
// leading whitespace from a string
String.prototype.trim = function() {
return this.replace(/^\s*|\s*$/g, "")
}




/********
SELECT BOXES
********/
// removes all options from the select box
HTMLSelectElement.prototype.clear = function(){
while (this.length > 0) {
this.remove(0);
}
}

// adds a new option to a select box
HTMLSelectElement.prototype.appendOption = function(id,textValue){
var opt = new Option(textValue,id);
this.appendChild(opt);
}

// clears a select box and optionaly inserts a first object
HTMLSelectElement.prototype.init = function(id,textValue){
this.clear();
if(textValue){
this.options[0] = new Option(textValue,id);
}
}

/* helper function */
function copyOptionsToArray(obj){
var optArray = new Array(1);
var idx = 0;

for(idx=0;idx<obj.length;idx++){
optArray[idx] = obj[idx];
}

return optArray;

}


HTMLSelectElement.prototype.prependOption = function(id,textValue){
var opt = new Option(textValue,id);
var optArray = copyOptionsToArray(this);

var nopt;
var idx=0;

this.init(id,textValue);

for(idx=0;idx<optArray.length;idx++){
this.appendChild(optArray[idx]);
}
}


HTMLSelectElement.prototype.insertOption = function(id,textValue,position){
if(!isNaN(position)){
if(position >= this.length){
this.append(id,textValue);
} else {
var optArray = copyOptionsToArray(this);
var idx = 0;

this.init();

for(idx=0;idx<optArray.length;idx++){
if(idx==position){
this.appendOption(id,textValue);
position = -1;
idx--;
} else {
this.appendChild(optArray[idx]);
}
}
}
}
}


HTMLSelectElement.prototype.dropOption = function(position){
if(!isNaN(position) &&amp; position < this.length){
var optArray = copyOptionsToArray(this);
var idx = 0;

this.init();

for(idx=0;idx<optArray.length;idx++){
if(idx!=position){
this.appendChild(optArray[idx]);
}
}
}
}

```


I realize there is next to no documentation there. Sorry, but most of them are
pretty self explanitory. If you need help just leave a comment.

Calling them is pretty easy; lets assume you already have a reference to a
SELECT object (objSel):


```js

objSel.prependOption("1","prepend");

objSel.dropOption(4);

objSel.appendOption("someval","append");

objSel.init();
or
objSel.init("someval","append");

objSel.insertOption("1","insert2",2);


```


## Comments

Bill

I don't just set the length to 0 because I am not certain the memory is
cleared - whereas I feel the remove function is going to initiate the
necessary garbage collection.

mclow

Hi!

Why don't just:

// removes all options from the select box
HTMLSelectElement.prototype.clear = function(){
this.length = 0;
}

?

mclow

Bill

very true, the inherent limitation in the plan sucks.. but it was a fun
exercise.

maybe IE7 will let us extend the SELECT..and Opera some day..

Dan Delaney

Personally, I love the idea of using HTMLSelectElement.prototype to extend the
select element's capabilities. Unfortunately, however, it only works in
Mozilla browsers. IE and Safari both complain that there is no
HTMLSelectElement object. It would be wonderful if all browsers supported this
fucntionality. But alas, the Web is an imperfect place, and coding for one
browser, whatever that browser may be, is a move in the wrong direction.

Dan Delaney

Personally, I love the idea of using HTMLSelectElement.prototype to extend the
select element's capabilities. Unfortunately, however, it only works in
Mozilla browsers. IE and Safari both complain that there is no
HTMLSelectElement object. It would be wonderful if all browsers supported this
fucntionality. But alas, the Web is an imperfect place, and coding for one
browser, whatever that browser may be, is a move in the wrong direction.

