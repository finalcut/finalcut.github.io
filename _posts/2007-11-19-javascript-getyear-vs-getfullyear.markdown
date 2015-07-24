---
layout: post
title: "Javascript getYear -vs- getFullYear"
date: 2007-11-19
comments: false
categories:
 - javascript
 - getyear
 - datetime
 - getfullyear
---
This is just a short reminder post to not use the getYear method on the Date
object in JavaScript. In case you weren't aware, or like me had forgotten,
getYear is not Y2K compliant and only returns a year relative to 1900 in
FireFox.

So, for instance, if you were write the following:

```js
var today = new Date;
alert(today.getYear());

```


You would end up seeing an alert box that showed 107 if you ran the script in
FireFox. Interestingly enough in IE you would see 2007. I don't know who is
following the standard, and frankly I don't care. Instead I just want to do it
right and in this case you do so by using getFullYear which returns a 4 digit
year value.


```js
var today = new Date;
alert(today.getFullYear());

```


This will return 2007 in IE, Firefox, and Opera.

## Comments

Bill Schneider

Interesting consequence - if you use getYear()/setYear() to set a cookie
expiration date in the past, it won't matter to Firefox, since 108 (as opposed
to 2008) is still in the past. Chrome is a little stricter.

http://wrschneider.blogspot.com/2011/08/javascript-getyear-and-cookie.html

Zach Gardner

Firefox's implementation of getYear() is consistent with the ECMAScript
definition for the function. It is IE that isn't standards complaint.

http://stackoverflow.com/questions/98124/why-does-javascript-getyear-
return-108

Anonymous

Thanks! Your post solved an issue I was having with some JavaScript that I
wrote.

Ricker

Thanks for the solution.

