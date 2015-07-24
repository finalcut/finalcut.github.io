---
layout: post
title: "RegEx Gotcha to Avoid"
date: 2005-05-18
comments: false
categories:
 - phone number
 - regular expression
 - regex
---
Last week I posted about [a great javascript validation library](http://cf-
bill.blogspot.com/2005/05/great-javascript-form-validation.html). However,
prior to even knowing about it I had often used javascript regular expressions
to validate form data for format before passing it on. One of my regular
expressions was designed to test for the proper formatting of phone numbers
and it was almost perfect for my needs.

Well, except for one major bug that let pretty much any garbage pass.

Now, I also tested somewhat on the serverside as well so it hand't really
caused me a data problem but the possibility was there. The funny thing is
this regEx and so many others like it on the net have been in use for years
and almost all that I have seen have the same problem.

I know alot of them do because when I first needed one I found it on the net
(before I knew anything at all about how to build my own regEx). Then later
when I needed it to be more capable I found others and snipped clipped and
pasted together many to get the one I needed. All of them have the same
problem though and that is they let arbitrary characters in at the beginning
of the string.

So, if your regex is supposed to limit to a number format of xxx-xxx-xxxx
where the area code is optional and you write:
(\d{3})?\d{3}\\-\d{4}$

You might think you're ok. But, you're not. Sure, this will stop you from
doing some things but it isn't foolproof.

you need to change it to:
^(\d{3})?\d{3}\\-\d{4}$

Notice, I added the ^ which means "match start of string" Without that you can
enter pretty much whatever you want before your valid phone number pattern and
still get it to pass the validation routine that should have cut it out. Note
also that you can't use the optional \A regEx anchor instead of the ^ as it
will not work. That little caveat caused me some issues.

So instead of only allowing:
304-525-5555 or
525-5555
it also allows:
falsdfjoij304-525-5555
fjsadkqlfjdsa525-5555

not really what you want is it? Anyway, here is my final regular expression
for phone number validation. I did this a bit differently than I normally
would so I could really explain each part of the regEx. Normally I would just
build the regEX and be done with it.


```js
function isValidPhoneNumber(s){
var pat = "^";
var exp;
// BEGIN THE ARA CODE GROUPING
pat = pat + "(";
// OPTIONAL OPENING (
pat = pat + "\\\\(?";
// 3 DIGIT AREA CODE
pat = pat + "\\\d{3}";
// OPTIONAL CLOSING )
pat = pat + "\\\\)?";
// OPTIONAL DASH OR SPACE BETWEEN AREA CODE AND PREFIX
pat = pat + "(\\\\-| )?";
// END THE AREA CODE GROUPING
pat = pat + ")?";
// PREFIX
pat = pat + "\\\d{3}";
//OPTIONAL DASH OR SPACE BETWEEN PREFIX AND SUFFIX
pat = pat + "(\\\\-| )?";
// SUFFIX
pat = pat + "\\\d{4}";
// OPTIONAL SPACE
pat = pat + "\\\s?";
// OPTIONAL EXTENSION ID - xt, ext, x, space, or dash
pat = pat + "(\\\\-|x|X|ext|EXT|ex|EX| )?";
// OPTIONAL SPACE
pat = pat + "\\\s?";
// OPTIONAL EXTENSION UP TO 6 NUMBERS
pat = pat + "\\\d{0,6}?";
// END OF INPUT
pat = pat + "$";
exp = new RegExp(pat);
return exp.test(s);
}

```


## Comments

Bill

Thanks, while I am definatly not a master of them I am pretty comfortable -
however I will take your advice to heart and not be very trusting of others
RegExs.

I guess that was the point of my post in some ways. Nearly every phone number
validation RegEx I found online (i even searched for more again yesterday
while posting this) have the same problem of the missing ^ (match start of
string).

The phone number regex I was using has been in place for quite a while and it
never revealed its problem until this week when a user tried to put a / in
between the areacode and phone number prefix - and it was accepted.

I'll give the book you suggested a look. I have also thought of getting
Forta's (RegEx's in Ten Minutes) just as a handy desk reference.

I think this would be a good place for a javascript unit test library.

gus

Regular Expressions can be daunting to learn, but are well worth the effort.
Without a solid understanding of regular expressions you should be very
skeptical of any regex you find online.

My general rule of thumb with any code I find online is... if I don't
understand it, I don't use it.

I highly recommend the O'Reilly book "Mastering Regular Expressions". It's not
an easy read, but well worth the effort.

