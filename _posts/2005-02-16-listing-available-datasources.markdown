---
layout: post
title: "Listing Available Datasources"
date: 2005-02-16
comments: false
category: coldfusion
tags: [utilities,database]
---
Here is some code I wrote quite a while ago to list the available datasources
on the server. More than likely it is some code I found somewhere else as I
doubt I was anywhere near the first person to do this.

However, I figure it might be useful to someone else so here goes:


```cfc
<CFLOCK Name="ServiceFactory" Type="Exclusive" TimeOut="10">
<CFSET Factory = CreateObject("java",
"coldfusion.server.ServiceFactory")>
<CFSET Service = Factory.getDataSourceService()>
<CFSET DataSources = Service.DataSources>
<CFSET Datasources = StructKeyArray(Datasources)>
<CFSET Temp = ArraySort(Datasources, "textnocase", "asc")>
</CFLOCK>

<select name="datasource">
<CFOUTPUT>
<CFLOOP From="1" To="#ArrayLen(Datasources)#" Index="i">
<option value="#Datasources[i]#">#Datasources[i]#</option>
</CFLOOP>
</CFOUTPUT>
</select>

```


## Comments

Mohsin Raza

Thanks. This was very helpful in sorting out a hosting related problem.
