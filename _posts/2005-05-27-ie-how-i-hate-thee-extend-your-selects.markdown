---
layout: post
title: "IE How I Hate thee (Extend Your Selects Cont..)"
date: 2005-05-27
comments: false
categories:
 - javascript
 - ie
---
This is my final post about extending select boxes. It provides all of the
methods I described earlier in their functional equivilant. However, note that
IE does fail miserably one one - the built in HTMLSelectElement.add() method.
By the spec you should be able to pass in an OPTION to select before. However,
if you try that with IE it will crash. You can only append Options to the end
of a select element by default in IE.

If you need the functionality to insert elements anywhere into a SELECT box in
IE I leave that task for you to finish. If you look at my first post on the
topic it will show you a way to do it that just needs to be converted to
functions instead of methods.

These will all work in both browsers that I can test against today - with the
one caveat already noted (about insertion).


```js
// removes all options from the select box
function clearSelect(obj){
while (obj.length > 0) {
obj.remove(0);
}
}

// changes the selection to a specified position
function pickSelect(obj,position){
if(position > obj.length-1) position = obj.length-1;

obj.selectedIndex = position;
}


// changes the selection to a specific id
function pickSelectByID(obj,id){
var idx = 0;
for (idx=0;idx<obj.length;idx++){
if(obj.options[idx].value == id){
pickSelect(obj,idx);
break;
}
}
}

// changes the selection to a specific text value
function pickSelectByText(obj,textValue){
var idx = 0;
for (idx=0;idx<obj.length;idx++){
if(obj.options[idx].text == textValue){
pickSelect(obj,idx);
break;
}
}
}


// changes the selection to a specific text value
function getSelectText(obj){
return obj.options[selectedIndex].text;
}



// clears a select box and optionaly inserts a first object
function initSelect(obj,id,textValue){
clearSelect(obj);
if(textValue){
obj.options[0] = new Option(textValue,id);
}
}


function insertSelect(obj,id,textValue,position){
var newOpt = new Option(textValue,id);

var oldOpt = null;

if(!isNaN(position) && position < obj.length-1 && position >= 0) {
oldOpt = obj.options[position];
}
try{ // standards compliant
obj.add(newOpt,oldOpt);
} catch(err){
// ie hack
obj.add(newOpt);
}
}

```


