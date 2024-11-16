---
layout: post
title: "getElementsByTagName"
date: 2005-01-24
comments: false
category: coldfusion
tags: [utilities]
---
Not everything I am going to write about here is as obscure and theoretical as
my prior two posts. Indeed this post, like many others, will deal with real
problems I face at work and some of the ways in which I address solving thos
problems. Friday, I was assigned the task of checking HTML content chunks for
a distinct set of [section 508](http://section508.gov/ "Accessability
Guidelines" ) problems. At first glance this might seem like a semi-complex
problem. However, I have two things going for me. First, I am not required to
check for html well formedness. That means if a tag is missing its closing
tag, I don't need to care. Secondly, and most importantly, I only have to test
for a specific subset of tags and the presence of their corresponding
attributes. For example I need to make sure all image tags have an alt
attribute and that all table tags have a summary attribute.

Basically, I am looking for the same type of pattern in both of the
aforementioned examples. Now, this would be super easy if ColdFusion supported
DOM functions on html fragments such as getElementByTagName. Java does support
this thanks to the Xerces parser and some open source libraries for html
parsing. However, at this point I think invoking these java objects would be
overkill. Instead, until I know even more about the problem domain, I think I
can use two pretty simple functions to get all of the tags of a certain type
and then to test those tags for the presence of the specified attribute.

Here is my UDF to grab all of the elements of a tag name - named, obviously
enough, getElementsByTagName


```cfc
<cffunction name="getElementsByTagName" returntype="array" hint="returns an
array of the specified tag elements">
<cfargument name="html" type="string" required="true">
<cfargument name="tag" type="string" required="true">

<cfset var startPos = 0>
<cfset var endPos = 0>
<cfset var count = 0>
<cfset var findTag = "<" & arguments.tag>
<cfset var htmlString = arguments.html>
<cfset var tagArray = ArrayNew(1)>

<cfset startPos = findNoCase(findTag,htmlString)>

<cfloop condition="startPos GT 0">
<cfset endPos = find(">",htmlString,startpos)>
<cfif endPos>
<cfset count = endPos - startpos + 1>
<cfset thisTag = Mid(htmlString,startPos,count)>
<cfset arrayAppend(tagArray,thisTag)>
<cfset count = Len(htmlString) - endPos>
<cfif count>
<cfset htmlString = Right(htmlString,count)>
<cfset startPos = findNoCase(findTag,htmlString)>
<cfelse>
<cfset startPos = 0>
</cfif>
<cfelse>
<cfset startPos = 0>
</cfif>
</cfloop>


<cfreturn tagArray>

</cffunction>

```


This function returns to me an array of "tags" from the opening bracket to the
closing bracket. This way I am sure to have all of the attributes of the tag.
So now all I need to do is loop over the array and find the elements that
don't have a specific attribute. Here I make two assuptions.

  1. all attributes will be proceeded by at least one space
  2. all attributes names will be followed by an equal sign (=)
Now, to improve this later I should probaly say an attribute name will be
followed by 0 or 1 spaces and then an equal sign, or maybe even 0 or more
spaces before the equal sign. However, at the moment I'm running with this
very basic, and probably false assumption. Heres the UDF:


```cfc
<cffunction name="checkTagForAttribute" returntype="array" hint="returns an
array of tags missing the specified property" access="private">
<cfargument name="tagArray" type="array">
<cfargument name="attribute" type="string">

<cfset badarray =" ArrayNew(1)">
<cfset arraycount =" 1">
<cfset thistag = "">
<cfset findattribute = " #arguments.attribute#=">
<cfloop condition="arrayCount LTE ArrayLen(arguments.tagArray)">
<cfset thistag =" arguments.tagArray[arrayCount]">
<cfif>
<cfset>
</cfif>
<cfset arraycount =" arrayCount">
</cfloop>
<cfreturn>
</cffunction>


```


this function also returns an array - a subset of the tags but this time only
those tags that fail to have the specified attribute. If the array is empty
then no obvious 508 problems are present in that tag set. Now, to test an HTML
code snippet I can just call these two functions back-to-back for each
tag/attribute pair I need to test against. At that point I can then do a
variety of things; present a list of problems or even prompt the user for
fixes to each problem and then update the html snippet automatically.

Since I have captured the entire text of each tag I can also show the entire
HTML snippet and highlight the problem tags if I need to as well. While both
functions could probably be improved both work against the problem domain as I
currently understand it and are both easilly extensible as I understand the
problem better. Oh, and I guess both could use a little bit of commenting too!
