---
layout: post
title: "ListToQuery UDF"
date: 2009-10-28
comments: false
categories:
 - coldfusion
 - udf
---
Today I happened to find myself at CFlib.org - I don't go there often - and I
was browsing the newer function submissions just for the heck of it and I came
across the function [ListToQuery](http://cflib.org/udf/listToQuery) by Russ
Spivey. It's a straight forward enough function but I thought it could be a
little cleaner, and potentially a little faster when dealing with large lists.  
  
Here is my version:  
```cfm  
<cffunction name="listToQuery" access="public" returntype="query"
output="false"  
hint="Converts a list to a single-column query.">  
  
<cfargument name="list" type="string" required="yes" hint="List to
convert.">  
<cfargument name="delimiters" type="string" required="no" default=","
hint="Things that separate list elements.">  
<cfargument name="columnName" type="string" required="no" default="column"
hint="Name to give query column.">  
<cfargument name="includeBlanks" type="boolean" required="no"
default="false" hint="include empty elements in the list as empty values in
the query">  
  
<cfset var query = queryNew("")>  
<cfset QueryAddColumn(query,arguments. columnName,ListToArray(arguments.lis
t,arguments.delimiters,arguments.includeBlanks))>  
  
<cfreturn query>  
  
</cffunction>  
```  
  
Sadly, I couldn't contact Russ directly to share my contribution so hopefully
he doesn't mind me sticking this here. If it weren't for his initial cut at
the function I wouldn't have thought to even try and write it.  
  
<del>If anyone wants to benchmark the two it would probably be interesting to
see if my intuition is correct.</del>  
UPDATE:  
Ok, well, I benchmarked it with 5000, 10000 and 30000 element lists (I didn't
have the patience for a 100,000 element list sorry (i suppose I could optimize
my list building). Here were the results:  
  
  
5000 element list  
Function| Time in ms  
---|---  
  
Using QueryAddColumn| 0  
  
Origional Version| 31  
  
  
  
10000 element list  
Function| Time in ms  
---|---  
  
Using QueryAddColumn| 47  
  
Origional Version| 235  
  
  
  
30000 element list  
Function| Time in ms  
---|---  
  
Using QueryAddColumn| 110  
  
Origional Version| 453  
  

