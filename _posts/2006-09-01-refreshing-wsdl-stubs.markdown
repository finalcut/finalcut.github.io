---
layout: post
title: "Refreshing WSDL Stubs"
date: 2006-09-01
comments: false
category: coldfusion
tags: [wsdl,rpc]
---
This is actually something I got from [an old blog post by Brian
Purcell](http://www.bpurcell.org/blog/index.cfm?mode=entry&entry=965) but I
figured I should have it handy in case his blog ever disappears and I need to
reference it again.

Basically it is just a programatic method for refreshing WSDL Stubs in CF that
I stick at the top of every test file I have that access a remote method call
on a CFC..


```cfc
<cfset serviceURL = "http://127.0.0.1/lb2/remote.cfc?wsdl" />

<cfobject type="JAVA"
action="Create"
name="factory"
class="coldfusion.server.ServiceFactory" />

<cfset RpcService = factory.XmlRpcService>

<cfset RpcService.refreshWebService(serviceURL)>


<cfinvoke
webservice="#serviceURL#"
method="someMethodName"
returnvariable="someVariableName" />


```


## Comments

Jeff Coughlin

This just made my life so much easier! Thanks so much (well, thenks to Brian,
but I wouldn't have seen it if you didn't repost :) ).
