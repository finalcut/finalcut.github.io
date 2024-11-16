---
layout: post
title: "UDF: GetTagContent"
date: 2005-09-15
comments: false
category: coldfusion
tags: [regex]
---
This is a UDF I wrote a while ago (that probably alredy existed on the net in
many forms) that I need to use on occasion. For instance I had to write a
tool that would import a static HTML website into our CMS. However, the client
only wanted certain parts of the page imported as content, they wanted the
page names to reflect the old "title" etc. So this UDF made it easy to get the
chunks of each page that I wanted.


```cfc
<cffunction name="getTagContent" returnType="string" output="false"
hint="returns all contents between an open and closing tag">
<cfargument Name="tag" type="string" required="true">
<cfargument Name="str" type="string" required="true">

<cfscript>
var matchStruct = structNew();
var startTag = "<#tag#[^>]*>";
var endTag = "</#tag#>";
return REReplaceNoCase(str, "(.*)(#startTag#)(.*)(#endTag#)(.*)", "\3");
</cfscript>

</cffunction>

```
