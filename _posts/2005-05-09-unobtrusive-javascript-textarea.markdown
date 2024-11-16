---
layout: post
title: "Unobtrusive Javascript  TextArea maxlength"
date: 2005-05-09
comments: false
category: javascript
tags: [textarea,maxlength]
---
One of the biggest failings of the textarea control to me is its lack of a
maxlength attribute. There are plenty of scripts out there that work to
simulate a maxlength but they always require adding onkeyup, onkeydown, and/or
onblur event handlers. What pain!

I just want to enter a maxlength="x" and have it be enforced. Thanks to the
wonders of DOM traversal this can be done as easily as anything else.


```js
<textarea name="briefbio" class="text" maxlength="500"></textarea>


<script type="text/javascript">

function textAreasInit(){
var objs = document.getElementsByTagName("textarea");
var oi = 0; //oi is object index
var thisObj;

for (oi=0;oi<objs.length;oi++) {
thisObj = objs[oi];
// note that maxlength is case sensitve
if (thisObj.getAttribute('maxlength')){
thisObj.onkeyup = forceMaxLength;
}
thisObj.onchange = saveEntryValue;
}
}

function forceMaxLength(){
var maxLength = parseInt(this.getAttribute('maxlength'));
if(this.value.length > maxlength){
this.value = this.value.substring(0,maxlength);
}
}
</script>

```

As is the case with most unobtrusive javascript you need the "addEvent" script
that will cause the textAreasInit function to be run when the page loads. Also
remember you can combine a bunch of different init methods together.

```js
<script type="text/javascript">
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


This is called via a very simple line of JS in the <head> section of
your site. The addEvent, forceMaxLength, and textAreasInit functions can be in
an external JS file for use whenever you need them.

```js
<script type="text/javascript">
addEvent(window, "load", textAreasInit);
</script>

```


## Comments

Bill

Thanks Anonymous though I'm not sure why you had to change to much. I've been
using the listed script for a long time and it works fine for me.

Anonymous

This is a working one, had to fix a lot of to make your examples work...

function textAreasInit(){
var objs = document.getElementsByTagName('textarea');
var oi = 0; //oi is object index
var thisObj;

for (oi=0;oi max_length) {
the_textarea_to_force.value = the_textarea_to_force.value.substring(0,
max_length);
}
}

Then put this somewhere in your HTML between script tags:

textAreasInit();

Bill

Charles just remove the line:

thisObj.onchange = saveEntryValue;

Charles

This didn't work for me at all. Keeps asking for saveEntryValue. hmmmm....
:-=(

Josh

function textAreasInit()
{
var fields = document.getElementsByTagName("textarea");
for(var i=0; i<fields.length; i++)
{
if(fields[i].getAttribute('maxlength') != undefined)
{
fields[i].onkeyup = function()
{
var maxLength = parseInt(this.getAttribute('maxlength'));
if(this.value.length > maxLength)
{
this.value = this.value.substring(0,maxLength);
}
}
}
}
}

frequency-decoder

Hey guys,

I've atually written a similar maxlength script:

http://www.frequency-decoder.com/demo/textarea-maxlength/

I passed the required maxlength within the textarea's classname e.g.

class="maxlength_50"

will give the textarea a maxlength of 50 characters (which has the added
benefit of not adding extra attributes to the actual textarea tag).

Oh, and it's unobtrusive (pretty much a requirement these days!).

Over and out..

Dustin Diaz

Oops. It's not valid xhtml...
I was just going over this today thinking of some way to get an unobtrusive
way of doing this. The original way I was doing this...

_
function maxIt()
{
var tot = 10;
if ( this.value.length > tot )
this.value = this.value.substr(0,tot);
}
function attachIt()
{
var ta = document.getElementById('maxed');
ta.onkeyup = maxIt;
}
_

but then i ran into the problems of being able to separately pass the total
amount as a different value per element. this assumes maxlength at 10... then
i couldn't figure out how to pass as an argument and it still being able to
use the keyword "this" which almost defeats the whole purpose.

I think eventually, the best way, would be to do a style just like yours, and
use a class like **class="maxlen50"** and pull a substr(6) on it. then instead
of **thisObj.getAttribute('maxlength')**, you'd replace it with className

Sue

I stumbled on this while googling a way to use maxlength with texarea and it
works perfectly -- on my single-line fields. Any clue as to why its not
working on my multi-line fields?

Any help would be appreciated! Thanks!!

sue at mmcxii dot com
