---
layout: post
title: "Prototype Library"
date: 2007-03-30
comments: false
categories:
 - javascript
 - development
 - prototype
---
I have finally decided to give the Prototype JS library a try on a project I
am working on. It is a long standing project with a pretty extensive home-
rolled javascript library however there were a couple areas where it was
starting to look long in the tooth. One of those was in finding and returning
groups of DOM Elements that meet certain criteria. For instance maybe I need
all of the input boxes of type text that have a specific class or all the
checkboxes of a specific class that are currently enabled.

Previously this was a relatively slow process as it involved grabbing all of
the inputs, looping, checking their type and class and perhaps their "checked"
status and then building a new array of any that matched all the rules. This
could take tens to hundreds of ms per call depending on how large the page's
Element collection was - and if I then needed to loop over all the returned
values multiple timmes to do something the page would get even slower to
execute. Looping over them once I have them couldn't be replaced but fetching
them could be and this is the first place Prototype seems to shine.

Now, when I need a collection of elements with specific rules I can use the
'[$$](http://www.prototypejs.org/api/utility/dollar-dollar)' method.

> Takes an arbitrary number of CSS selectors (strings) and returns a document-
order array of extended DOM elements that match any of them.



My huge loop is now reduced to a very simple method call which is, in my
casual observation, always faster by an order of magnitude or more!

For instance to get all those checkboxes I was describing before I can just
write:

```js
var checkboxes = 'input[type="checkbox"]:enabled';
```


It's a pretty cool and handy way of grabbing all of those Elements. However,
what I'm not sure of yet (though I'll be testing later today) is if you can
specify multiple attribute selectors in one call - if so that would be really
cool. I'll let you know.

