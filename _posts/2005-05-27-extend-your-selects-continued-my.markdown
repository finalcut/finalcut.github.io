---
layout: post
title: "Extend Your Selects Continued (My Mistakes)"
date: 2005-05-27
comments: false
category: javascript
tags: [dom]
---
Well, it seems I stepped in a pile of something. First, I have to come clean
with the facts. Before today the methods I showed earlier for extending a
SELECT box were just functions that took in the select box and the other
properties. However, I decided to rewrite them as methods of the select box
object. It works in Mozilla; but alas not IE.

Some of the methods I showed earlier needed to be rewritten anyway as they
were neither efficient or practical and at least one was just reinventing the
wheel.

First let me reiterate these will only work in Mozilla. I'm not sure why they
work in Mozilla at all since it sounds like they shouldn't work at all
according to the spec - but that is a debate for others to worry about. I can
extend the STRING and the ARRAY objects just fine across browsers but not the
HTMLSelectElement.

Anyway, first we need to just dump the new method I wrote earlier called
HTMLSelectElement.prototype.dropOption as it is already a built in method
called remove:


```js
objSel.remove(4);

```


Secondly the insert, prepend, and append methods were all pretty poorly done.
So I just dropped the prepend, and append and rewrote insert.


```js
HTMLSelectElement.prototype.insertOption = function(id,textValue,position){
var newOpt = new Option(textValue,id);

if(!isNaN(position) && position < this.length-1 && position >= 0) {
this.add(newOpt,this.options[position]);
} else {
this.add(newOpt,null);
}
}

```


Now if I want to prepend I can just call the above with position of 0, to
append I don't pass in a position, and to insert I pass in any numeric value.
If the value is not numeric, too small, or too big it just appends the new
option.

You might also notice I'm now using the built in method "add" instead of
AppendChild. Add is basically the same as my insertOption except it handles
the creation of the new OPTION object.

I discovered my IE mistake by trying to run my test page in IE easilly enough.
After some google research it seems it just isn't possible. I also discovered
my other mistakes by, now hold on here, reading the SPEC. That's right by
reading the DOM spec at the W3C page I was able to learn how stupid I am! You
can see the spec for the HTMLSelectElement if you want.

Here is the full library of updated methods (plus a couple extra). I'm not
sure how useful they are as is since they don't work in IE. But they should be
easy to transform back to functions if you need one.


```js
// removes all options from the select box
HTMLSelectElement.prototype.clear = function(){
while (this.length > 0) {
this.remove(0);
}
}

// changes the selection to a specified position
HTMLSelectElement.prototype.select = function(position){
if(position > this.length-1) position = this.length-1;

this.selectedIndex = position;
}


// changes the selection to a specific id
HTMLSelectElement.prototype.selectID = function(id){
var idx = 0;
for (idx=0;idx<this.length;idx++){
if(this.options[idx].value == id){
this.select(idx);
break;
}
}
}

// changes the selection to a specific text value
HTMLSelectElement.prototype.selectElementByText = function(textValue){
var idx = 0;
for (idx=0;idx<this.length;idx++){
if(this.options[idx].text == textValue){
this.select(idx);
break;
}
}
}


// changes the selection to a specific text value
HTMLSelectElement.prototype.textValue = function(){
return this.options[selectedIndex].text;
}



// clears a select box and optionaly inserts a first object
HTMLSelectElement.prototype.init = function(id,textValue){
this.clear();
if(textValue){
this.options[0] = new Option(textValue,id);
}
}


HTMLSelectElement.prototype.insertOption = function(id,textValue,position){
var newOpt = new Option(textValue,id);

if(!isNaN(position) && position < this.length-1 && position >= 0) {
this.add(newOpt,this.options[position]);
} else {
this.add(newOpt,null);
}
}

```


## Comments

Anonymous

fwiw it seems that you can attach methods to instances of HTMLSelectElement in
IE. Not nearly as convenient as attaching to the prototype, but it may help
you out in some situations.

cheers,

mathieu
