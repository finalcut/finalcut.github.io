---
layout: post
title: "Javascript: When a String isn't"
date: 2008-10-27
comments: false
categories:
 - javascript
 - int
 - gotcha
 - string
 - cast
---
This is actually pretty simple and is best explained with example code:  
  
```js  
var x = "0E1234";  
  
if(x != 0){  
alert("ok, makes sense!");  
}  
```  
  
If you stick that source code into any browser and try to execute it you'll
never see the alert. Look at it again and see if you can tell why?  
  
Javascript is pretty agressive in casting things so if you have an int on the
right and a value that can be successfully cast as an int on th left
Javascript will cast the second half of the expression to an int as well.
0E1234 casts to an int as 0.  
  
Basically, if you wanted that javascript to do what you expected you'd need to
write:  
```js  
var x = "0E1234";  
  
if(x != "0"){  
alert("ok, makes sense!");  
}  
```  
  
Note the quotes around the zero now. Now it treats both sides of the
expression as a string and voila' the alert box will appear.  
  

### ===

  
There is another option to test for equality, the === (triple equal sign).
What this does is check for absolute equality in not just value but base type
as well.  
  
```js  
var x = "0E1234";  
  
if(!(x === 0)){  
alert("ok, makes sense!");  
}  
```  
  
That would cause the alert to go off as well. Just remember that "0" and 0
aren't the same either so:  
```js  
var x = "0";  
  
if(!(x === 0)){  
alert("ok, makes sense!");  
}  
```  
  
would also evaluate to the point where the alert dialog appeared. Pretty
simple stuff but it can really bite you when you least expect it.  
  
For instance, let's say you were trying to evaluate a dropdown boxes selected
value. The first value {Please Select A Value} evaluates to "0"  

    
    
      
    ...  
       &tl;option value="0">Please Select A Value</option>  
    ...  
    ```
      
      
    If you try to make sure the selected value isn't equal to zero wrap the zero your comparing against in quotes because, otherwise, you'll end up confused as to why "0" doesn't equal 0.
    
    
    

