---
layout: post
title: "Building the Memento Tree"
date: 2005-06-27
comments: false
categories:
 - coldfusion
 - patterns
 - memento
---
I know some may frown on the idea of having a base "bean" class but that is
exactly what I have settled on in order to support composite objects that
consist of multiple beans. Bascically there are two things I always want to be
able to do with my bean:

  1. dump it
  2. get a memento
When I dump a bean though I don't want all the stuff in the var scope but
instead the variables.instance structure. Also, my memento is basically just a
copy of the variables.instance structure (sort of).

The reason I say sort of is because what if my variables.instance.{somevar} =
another bean? Then what I really want in its place is that beans memento
(variables.instance struct).

Here is an example from a recent project. I have studentenrollment object. It
consists of a few things:

  * student - an instance of student.cfc

* address - an instance of address.cfc

  * class - an instance of theclass.cfc (named that way so i don't accidently call getClass())

  * entryassessment - an instance of assessment.cfc
  * interimassessment - an instance of assessment.cfc
  * exitassessment - an instance of assessment.cfc
  * a bunch of other things specific to that student+class relationship
So when I go to get the memento of the studentenrollment I really want the
memento that is crafted from studentenrollment.variables.instance and all the
composite objects variables.instance structs. To that end I added two methods
to my base bean.cfc (that all of my beans extend).


```cfc
<cffunction name="getMemento" access="public" output="false"
returntype="struct">
<cfreturn copyMementoStruct(variables.instance) />
</cffunction>

<cffunction name="copyMementoStruct" access="private" output="false"
returntype="struct">
<cfargument name="memento" type="struct">
<cfset var newMemento = structNew() />
<cfset var keylist = structKeyList(arguments.memento) />
<cfset var key = 0 />

<cfloop list="#keyList#" index="key">
<cfif isSimpleValue(arguments.memento[key])>
<cfset newMemento[key] = arguments.memento[key] />
<cfelseif isQuery(arguments.memento[key])>
<cfset newMemento[key] = arguments.memento[key] />
<cfelseif isStruct(arguments.memento[key])>
<cftry>
<cfset newMemento[key] = arguments.memento[key].getMemento() />
<cfcatch>
<cfset newMemento[key] = copyMementoStruct(arguments.memento[key]) />
</cfcatch>
</cftry>
<cfelseif isXMLDoc(arguments.memento[key])>
<cfset newMemento[key] = arguments.memento[key] />
<cfelseif isWDDX(arguments.memento[key])>
<cfset newMemento[key] = arguments.memento[key] />
</cfif>
</cfloop>

<cfreturn newMemento />
</cffunction>

```


This returns me a nice structure that contains all of the appropriate memento
information. Then my handy dump method works in conjunction


```cfc
<cffunction name="dump" access="public" output="true" return="void">
<cfargument name="abort" type="boolean" default="0" />
<cfdump var="#getMemento()#" />
<cfif arguments.abort>
<cfabort />
</cfif>
</cffunction>

```


What do you think? I think it works out pretty well but would love to hear the
opinion of others.

## Comments

Bill

odd question, but I was born in 1972 - so I'm a Rat.

Anonymous

How can you be a rat when you are 32yr? My calculation says you are an "Ox",
or "30yr".

-Mee

