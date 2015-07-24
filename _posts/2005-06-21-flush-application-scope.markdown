---
layout: post
title: "Flush the Application Scope"
date: 2005-06-21
comments: false
categories:
 - coldfusion
 - utilities
---
I was looking at the model-glue framework today (haven't done much with it yet
so I won't talk about it yet) and decided I wanted to see how fast one of the
same apps was with the built in model-glue debugging turned off.

To do so I had to edit the ModelGlue.xml file - however it turns out that the
xml file (as it should be) is cached in the application scope. So I was forced
to do a restart of the CF service. I typically prefer not to do that (just
becuase it is kind of slow on my machine).

So, I wrote a very simple flush.cfm file that will flush the application
scope. Obvioulsy, you don't want to leave this lying around but you might find
it helpful if you aren't already using a similar technique:


```cfc
<cfloop list="#structKeyList(application)#" index="key">
<cfif key NEQ "applicationname">
<cfset structdelete(application,key) />
</cfif>
</cfloop>
```


I had to update the prior code to check and make sure I'm not deleting the
applicationname value.

Obviously, nothing real groundbreaking here - but I figured it might save some
people the frustration of clearing their application cache while they develop.
If anyone knows of any dangers/risks in doing this please leave a comment. Oh,
and this has only been tested on MX 6.1 (but I see no reason why it wouldn't
work on 7).

## Comments

Anonymous

If you edit your Coldspring.xml file and then append init=true to the URL
anywhere, this will flush your application scope

Bill

thanks for sharing your approach Mark. I think I will stick with my "flush"
just becuase
1\. I don't like editing my application.cfm file (no real reason)
2\. I prefer not having duplicated application scopes (from changing the
application name) in memory
3\. typically if I flush the scope I don't really care how often I have done
it. If I'm doing it is usually to reload a changed cfc (such as a DAO) into
application scope after my model has changed in some way.

likewise with the model-glue framework I didn't really care that I was
flushing all I really cared was to get rid of the model-glue debug info to see
if had any effect on the overall performance of the framework.

However, I will keep your method in mind should I be working on a project
where I do need that extra information!

Cheers,
Bill

Anonymous

Bill - during development you can set the application timeout to something
small - like an hour, and then simply change the name of the application when
you want to reset the scope. I usually use a number of some kind to tell me
how often I've modified the static parameters of the scope - like
"myapplicationname_v1_21" (modified 21 times for example).

-Mark Kruger

