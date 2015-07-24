---
layout: post
title: "Regex for matching floating point numbers that include commas"
date: 2010-09-15
comments: false
categories:
 - period
 - comma
 - float
 - decimal
 - regex
 - numbers
---
Honestly, I thought it would be easy to find a regex that would match
something like:  
  
1,234.56 OR 1234.56 OR 123,456.789029329 or even -223.233434332 etc.  
  
But it wasn't. I found some but they didn't quite work or  
  
Anywhere here is the regex I crafted and settled on:  
  
**^(\d|-)?(\d|,\d{3})*\\.?\d*$**  
  
  
It isn't perfect, but it is as close as I could manage. Here are some matches:  

  * 1322.23
  * 1,322.23
  * 1,322
  * 1132

Here are some numbers that fail to match

  * 1,32
  * 1,32,2
  * 1320.223,232

So, in general this works great but it is possible to get by the regex
somewhat because I just am not strong enough with regex's at the moment to fix
it:

  

Here is an example:

  * 1,2345,232

Notice there are four numbers between the first and the second commas.  My
rule insists there has to be at least 3 numbers but doesn't insist on a comma
before the next number.  The reason for this is the fact that I don't want
commas to be required before the decimal point.  My initial effort which
insisted on three numbers after the first comma and a second comma before the
next three numbers etc required that any number in the thousands or higher had
to have a comma if I wanted to use a decimal point.  That wasn't acceptable so
the current regex is my best compromise.

  

If you can offer one better let me know in the comments.

## Comments

AdamNation

Try this:  
  
^0(\\.0*)?$|^(-?0?\\.0*[1-9]\d*)$|^(-?[1-9]((\d{0,2},(\d{3},)*\d{3})|(\d)*)(\\
.\d*)?)$  
  
  
It doesn't allow trailing zeros ("012") ("0.000x" is allowed). Negative zero
is not allowed. A number is valid if it ends with a period, as in "12."

Bill

Sorry that doesn't work.  
  
I just tested it and with the number  
1,234.232.232 it fails in two ways:  
  
first, it selects 234.232.232 so it drops off the 1, and it allows multiple
decimal points.

AdamNation

The following is untested, but I think it may be on the right track, unless
I'm breaking the regex engine somehow...  
  
Basically, it first tries to match "0". If it can't, it tries to match -1 <
x < 1\. If it still fails, it tries to match ddddd.ddddd with optional
commas. No leading 0's are allowed.  
  
The only problem I see is that -0.0000 is currently allowed, but I think that
could be resolved.  
  
^  
0  
|  
-?0?.\d+   
|  
-?[1-9]  
(  
(\d{0,2},(\d{3},)*\d{3}) |  
(\d*)  
)  
(.\d*)?  
$

