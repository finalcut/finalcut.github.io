---
layout: post
title: "Model Glue : Upto my Singletons"
date: 2005-11-10
comments: false
categories:
 - coldfusion
 - singletons
 - model-glue
---
Ok, so the title of this one stretches the theme of depth in my exploration of
Model Glue but it does highlight an important feature of Model Glue - the
Singleton.

A few days ago I talked about caching my security object kind of like this:

```cfc
<cfif NOT ExistsInCache("security")>
<cfset
AddToCache("security",createObject("component","lb2.util.Security").init())
/>
</cfif>

<cfreturn GetFromCache("security") />

```


Well, today as I was digging into the Model-Glue website I came across a post
that mentioned a method named "createSingleton()" which, oddly enough, doesn't
exist anywhere in Model Glue. Fear Not though Joe has this covered in much the
same way I often create Singletons when not using Model Glue.

Within your controller you can call getModelGlue.getSingleton(param1,param2)
and it handles the creation if necessary - otherwise it returns the previously
crafted Singleton.

param1 is the type of object you want to create. So, in my case I am almost
always creating a "component" singleton. Basically param1 is the same thing
you pass into createobject in CF as the first parameter.

Likewise param2 is the "component" to be created, again just like with
createobject (hint GetSingleton calls, you guessed it, CreateObject if your
singleton doesn't exist).

So now my method getSecurity looks like this

```cfc
<cfreturn getModelGlue().getSingleton("component","lb2.util.Security")
/>

```


