---
layout: post
title: "problem with cfqueryparam and lists"
date: 2005-02-02
comments: false
categories:
 - coldfusion
 - cfqueryparam
---
Knowing the value of a database plan I pretty much always use the
<cfqueryparam> tag inside queries with variable parameters. However,
recently I encountered a problem with the <cfqueryparam> tag and
ColdFusion 5. You may be wondering why I'm still using CF5 and the answer is -
its what that specific customer is using. So, now that I have justified my use
of CF 5, and explained why I can't use MX on this project, I'll explain the
problem with some code.  
```cfm  
<cfset someListOfIds = "1,2,3,4,5,,7,10,21">  
  
<cfquery name="someQuery" datasource="somedsn">  
SELECT * FROM someTable where id IN <cfqueryparam
cfsqltype="CF_SQL_INTEGER" value="#someListOfIds#" list="true" />  
</cfquery>  
```  
  
On CFMX this runs without a problem. But, on CF5 it does not. Instead it
crashes saying that I can't pass in a "" value as an integer in my list. (I
would put some official error text here but I don't have it handy sorry.)  
  
The problem arises with the list. You will notice that between the 5 and 7 of
the list is an empty element. Now, CF ALWAYS treats that list as a 8 element
list, ignoring the empty elements, right? Well, not in CF 5 with the
<cfqueryparam> tag. Instead it treats it as a 9 element list and tries
to pass in the empty string value. Because of that, and because the
application using this might have empty element lists being passed around I
now have to introduce a new function to strip out empty elements.  
  
```cfm  
function listDropEmpty(list){  
var newList = "";  
var i = 1;  
var tArray = ListToArray(list);  
for(i=1; i LTE arrayLen(tArray); i=i+1){  
newList = listAppend(newList,tArray[i]);  
}  
return newList;  
}  
```  
  
With this simple function I am able to drop the empty elements. Another option
I could use instead is ListSort as it returns a sorted list and will thus drop
the empty element. I suppose it is just a matter of preference and the
performance. I don't know how one performs against the other. It seems like
ListSort might take longer since it is actually doing quite a bit more than my
listDropEmpty option but I haven't tested this.  
  
So beware lists and <cfqueryparam> in CF 5!

