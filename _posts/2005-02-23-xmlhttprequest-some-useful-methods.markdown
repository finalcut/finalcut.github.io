---
layout: post
title: "XMLHttpRequest - Some Useful Methods"
date: 2005-02-23
comments: false
categories:
 - javascript
 - ajax
 - xmlHttpRequest
---
First off, sorry I haven't posted. My wife's grandmother passed away and I
have been unavailable.

Now, on to more plesant thoughts. The wonderful XMLHttpRequest object. I love
the thing. A few years ago I needed to use something like it and I didn't even
know about the activeX object in IE. However, IE did support this cool thing
called DataIslands that worked basically the same way. I had a pretty decent
IE only dataisland library that I could use for all sorts of cool interaction.
However, time has passed and it is important that the applications I work on
support, at a minimum, both IE and Mozilla. Hence my love of the
XMLHttpRequest object.

Today I was working on an "Audit" application that the customer requires saves
it's state no matter where the user is at in the audit. The audit is many
pages long and there are MANY options on each page. Using the old non
XMLHttpRequest method I had two choices: either design for IE only or make the
page refresh on EVERY option change. Obviously, neither of those options are
very good. So, digging into the articles on the XMLHttpRequest object that I
have bookmarked previously, I built a couple of my own routines for
interacting with the XMLHttpRequest object. Before I begin code listings
though I must give credit where it is due. This code is based off of the work
already existing at [Apple's developer
site](http://developer.apple.com/internet/webcontent/xmlhttpreq.html).

The Apple solution was a little clunky though and so I broke it up a bit so
that the code was a little cleaner and, perhaps, a bit more reusable. First
thing first I need an XMLHttpRequest object regardless of the browser I'm in
(this is also a nice place to do minor browser id).


```js
isIE = false;
var xmlhttp;

function xmlObjInit(){
if (window.XMLHttpRequest) {
xmlhttp = new XMLHttpRequest();
} else if (window.ActiveXObject){
xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
isIE = true;
}

}

```



I use a global object as my xmlhttp object simply because I reference it in
all of these functions and passing it around isn't very clean.

The second method I need is the backbone of the whole process and it
"executes" the GET on the XMLHttpRequest object.


```js
function loadXMLDoc(xmldoc,stateHandler,debug){
var xmlURL = xmlRoot + xmldoc;
var xmlData = '';
var idList = '';

if(debug)
alert(xmlURL);

xmlObjInit();

xmlhttp.open("GET", xmlRoot + xmldoc,true);
xmlhttp.onreadystatechange = stateHandler;
xmlhttp.send(null)
}

```


This is pretty straightforward and is almost identical to how the Apple stuff
works in the end. Except I don't have a stateHandler hardcoded anymore and the
construction of the XMLHttpRequest object has been removed to the xmlObjInit()
method. I also added a convenience optional parameter of debug. If a non-zero
value is passed in as the third parameter it will popup the url it is
attempting to read. This is VERY handy and saves me from typing alert(xmlURL)
everytime something goes wrong during development.

The stateHandler parameter is actually a function passed in. The fact that you
can do that in Javascript has always impressed me (I really never expected it
in JavaScript) and it comes in really handy here.

I also have a template stateHandler defined that other developers can use to
model theres off of. Again, it is very similar to the Apple example:


```js
function xmlStateChange(){
if (xmlhttp.readyState==4) {
if (xmlhttp.status == 200) {
alert(xmlhttp.responseText);
} else {
alert("There was a problem retrieving the XML data:\n" +
xmlhttp.statusText);
}
}
}

```


Finally, here is an example of my using the code somewhere in my application:


```js
<button
onclick="loadXMLDoc('sample.xml.cfm',xmlStateChange);">Test</button>

```



You may have noticed that I only pass in the filename and not the full URL
path to the file to "execute" - I do this as convention. I store all of my
files of this nature in one directory within the application and then have a
javascript variable defined as a global with the full path to that directory
already stored. That's why the first thing I do in loadXMLDoc() is some string
concatenation.

