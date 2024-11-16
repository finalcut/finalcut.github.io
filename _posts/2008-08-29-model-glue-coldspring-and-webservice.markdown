---
layout: post
title: "Model Glue, ColdSpring, and a Webservice"
date: 2008-08-29
comments: false
categories:
 - model-glue
 - coldspring
---
Last year I had to work on a website project where I chose to use Model
Glue:Unity as the MVC framework. It worked out really well. However, once I
was done with the app I ended up having to create a C# client app that could
synchronize with my web application. As you might imagine a webservice was
needed which would expose parts of my model to the client application.

Now, while using MG:U I ended up coming to really appreciate Cold Spring -
this post isn't really going to evangelize that great tool - but instead it
will explain how I was able to make use of the ColdSpring work I had used with
MG:U from within my webservice.

As a minor introduction I really didn't know anything about ColdSpring when I
started that project and I definitely didn't know how MG:U was utilizing
ColdSpring - I just knew it worked. However, once I created my webservice I
didn't really know how to access all of the objects that ColdSpring was
managing for me; all my services and gateways were inaccessible to me unless I
could somehow get a reference to the MG:U framework that was instantiated by
running the web application.

This coupling between my webservice and MG:U was obviously not ideal. However,
I really didn't know how to avoid it nor did I have a ton of time to figure
out a better solution. So I ended up with a bit of a kludgy hack in my
webservice so that I could get the objects from ColdSpring via MG:U thusly:


```cfc
<cffunction name="getServiceObject" access="private" returntype="any"
output="false">
<cfargument name="beanName" type="string" required="true" />
<cfset var keypos= "" />
<cfset var key = "" />
<cflock type="readonly" scope="Application" timeout="10">

<cftry>
<cfset key = cgi.path_translated />
<cfset keypos = listfindnocase(key, "WebServices", "\") -1 />
<cfset key = listgetAt(key, keypos, "\") />
<cfcatch>
</cfcatch>
</cftry>

<cfif Len(key)>
<cfreturn
application["#key#"].framework.getBeanFactory().getBean(arguments.beanName)
/>
<cfelse>
<cfsavecontent variable="key">
<cfdump var="#structKeyList(application)#" />
</cfsavecontent>
<cfthrow type="WebServiceUnavailable" message="The Website has not been
initialized since last reboot." />
</cfif>
</cflock>
</cffunction>

```


Nasty isn't it? Basically my webserivce sits in a subdirectory of the initial
application which is how that nasty kludgy approach worked. However my
webservice had the dependency that the website had been loaded at least one
time since the last reboot of the server in order for the webservice to work -
ugh; talk about bad code smell.

Well it turns out there is a much, much easier and cleaner solution to my
problem. All of you ColdSpring guru's are probably still trying to figure out
why I approached the problem like I did in the first place - and some of you
are probably wondering why I didn't just use the ColdSpring Proxy stuff to
create the webservice (I don't really know how nor do I understand it yet).
Anyway here is what I ended up doing to fix my problem of accessing ColdSpring
from my webservice.

Basically I just plopped a new Application.cfc file in my webservices
directory. I set a few application settings and then defined just the
onApplicationStart method:


```cfc
<cffunction name="OnApplicationStart">
<cfset application.coldspring =
createObject("component","coldspring.beans.DefaultXMLBeanFactory").init()
/>
<cfset application.coldspring.loadBeansFromXMLFile("path\to\my\mg:u\config\
ColdSpring.xml",true) />
</cffunction>

```


Now my function in my webservice is simplified to this:


```cfc
<cffunction name="getServiceObject" access="private" returntype="any"
output="false">
<cfargument name="beanName" type="string" required="true" />
<cfset var keypos= "" />
<cflock type="readonly" scope="Application" timeout="10">
<cfreturn application.coldspring.getBean(arguments.beanName) />
</cflock>
</cffunction>

```


Holy Crap that's a lot cleaner. It's amazing what happens when you read the
documentation on using ColdSpring and not just on configuring it.

Moral of the story? RTFM

