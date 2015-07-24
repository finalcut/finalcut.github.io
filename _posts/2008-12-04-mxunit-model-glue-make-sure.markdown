---
layout: post
title: "MxUnit + Model Glue : Make Sure ModelGlue.xml Doesn't have Duplicate Events"
date: 2008-12-04
comments: false
categories:
 - coldfusion
 - model-glue
 - mxunit
---
This is a simple test I threw together to make sure our fairly complex
ModelGlue.xml config file doesn't end up getting two events named with the
same name. While this shouldn't happen it did and so I needed a test to make
sure it didn't happen again.  
  
```html  
<cffunction name="testConfigFileForDuplicateEventNodeNames" access="public"
returntype="void">  
<cfset var local = structNew() />  
  
<cfset local.filepath = ExpandPath('\lb2\config\ModelGlue.xml') />  
  
<cfset local.xml = XmlParse(local.filePath) />  
  
<cfset local.events = local.xml.modelglue["event-handlers"].XmlChildren
/>  
<cfset local.usedKeys = structnew() />  
  
  
<cfloop from="1" to="#ArrayLen(local.events)#" index="local.i">  
<cfset local.node = local.events[local.i].XmlAttributes.name />  
<cfif StructKeyExists(local.usedKeys, local.node)>  
<cfset fail("the node " & local.node & " is defined more than once in
ModelGlue.xml") />  
</cfif>  
<cfset local.usedKeys["#local.node#"] = "" />  
</cfloop>  
  
</cffunction>  
```  
  
This is obviously an incredibly simple test and it doesn't collate problems,
it just fails on the first one. Nor will it tell you where in your
ModelGlue.xml file to find the problem; but it works for a simple peace of
mind test. Hope it helps someone else!  
  
Finally I mention mxUnit but obviously you can easily update this to work with
the unit test framework of your choice. I just happen to choose mxUnit.

