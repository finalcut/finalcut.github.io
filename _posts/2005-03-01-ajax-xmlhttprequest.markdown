---
layout: post
title: "AJAX - XMLHTTPRequest"
date: 2005-03-01
comments: false
category: coldfusion
tags: [ajax,xmlHttpRequest]
---
I just read over at MossyBlog about the term AJAX (Asynchronous Javascript and
XML). And, since I have recently been posting code that deals with that I
figured I would post this little blurb as well. Technically it is just an
update to some code I posted last week but it allows for slightly more
flexibility.


```js
isIE = false;
var xmlhttp;

function newXMLobj(){
var xmlObj;
if (window.XMLHttpRequest) {
xmlObj = new XMLHttpRequest();
} else if (window.ActiveXObject){
xmlObj = new ActiveXObject("Microsoft.XMLHTTP");
isIE = true;
}

return xmlObj;
}


/**
* loads an xml document object and executes the appropriate method
*
* @param xmldoc STRING the name of the file to load. The URL will be
* built from this filename.
* @param stateHandler FUNCTION the function to call on state change to the xml object
* this is the method that will do something with the XML
* fetched
* @return NULL
* @see http://developer.apple.com/internet/webcontent/xmlhttpreq.html
*
*
* sample usage:
* <button onclick="loadXMLDoc('sample.xml.cfm',xmlStateChange);">Test</button>
*
**/
function loadXMLDoc(xmldoc,stateHandler,debug,xmlObj){
var xmlURL = xmlRoot + xmldoc;
var xmlData = '';
var idList = '';


if(debug==1){
alert(xmlURL);
}
if(xmlObj){
xmlObj.open("GET", xmlRoot + xmldoc,true);
xmlObj.onreadystatechange = stateHandler;
xmlObj.send(null)
} else {
xmlhttp = newXMLobj();
xmlhttp.open("GET", xmlRoot + xmldoc,true);
xmlhttp.onreadystatechange = stateHandler;
xmlhttp.send(null)
}
}

```


Now basically all I really changed is the fact that loadXMLDoc now contains an
optional parameter, xmlObj. If xmlObj is provided then we know an
XMLHTTPRequest object has been passed in and I reference it. Otherwise we
initialize the global variable xmlhttp and go from there.

Why did I do this? Well if you have to call loadXMLDoc multiple times on the
same page its for the best. Using the same objet (xmlhttp) on multiple
consecutive calls you will get unexpected and unwanted results.

Bear in mind, because of the response handler system you need to define a new
global variable for each xmlhttprequest object you want to use. Here is a
simple example:


```js
<script type="text/javascript">
var xmlCat = newXMLobj();
var xmlCmp = newXMLobj();

function fireActivityClick(linkID){
// get categories based on activity
loadXMLDoc('someURL.cfm?linkID=' + linkID,catHandler,0,xmlCat);

// get compliance issues based on activity
loadXMLDoc('someOtherURL.cfm?linkID=' + linkID,cmpHandler,0,xmlCmp);

}


function catHandler(){
...
}
function cmpHandler(){
...
}
</script>

```


## Comments

Bill

Hey Bruno,

you may want to check out my more recent post regarding AJAX - and a wrapper
library called SACK which is now my preferred method.

http://twilightuniverse.com/2005/05/sack-of-ajax/

just note that I added a line to SACK

self.responseXML = self.xmlhttp.responseXML;


I added that down just after the line that says:
self.response = self.xmlhttp.responseText


in the case statement for option 4 (done).

Bruno Oliveira

Hi, Bill.

I'm Bruno Oliveira from Portugal.

I'm using firefox 1.0.1 and your example don't work for me except if I change
this line:

xmlhttp.onreadystatechange = stateHandler;

for this:

xmlhttp.onreadystatechange = eval(stateHandler);

Keep up the good work.

Bruno Oliveira
