---
layout: post
title: "CFUnit and a Custom Tag"
date: 2008-03-21
comments: false
categories:
 - customtags
 - coldfusion
 - test driven development
 - unit testing
 - cfunit
 - tdd
---
I'm not spending much time working in ColdFusion right now. However, on
occasion I need to go back and do a little maintenance on a legacy product.
One of those had a pretty poorly written (by me) custom tag for figuring out
the number of days in the month.  This is a custom tag that has been in use
since 2000 and yet the bug with it wasn't noticed until this month.  It should
have been noticed back in 2004 but it wasn't.  Heck it would have been noticed
when I wrote it if it had some unit tests associated with it.  But it didn't
so this month the customer came back upset that a report wasn't showing the
right numbers because the data for the 29 of Feb. wasn't being shown.  
  
Ok, so it was a stupid bug but those are the ones that slip by so easily if
you don't have unit tests in place.  Fortunately, we now have nice frameworks
like CFUnit that make writing unit tests easy.  However, I didn't really see
any good documentation on writing tests for custom tags so this brief article
is designed to show one simple example:  
  
Just like with the rest of the CFUnit examples you need two files a CFC which
contains the tests and a cfm page that invokes those tests. I'm just going to
show you the CFC with the tests since invoking them is the same as every other
CFUnit test.  
  
```cfm  
<cfcomponent name="LastDayInMonth"
extends="net.sourceforge.cfunit.framework.TestCase">  
<cffunction name="setUp" returntype="void" access="public">  
<cfimport taglib="/aemis/CustomTags/StandardCustomTags" prefix="standard"
/>  
</cffunction>  
  
  
<cffunction name="testFebruaryInLeapYear" returntype="void"
access="public">  
<cfset var output="" />  
  
<standard:Days_In_Month month_id="2" year="2008"
returnvariable="output">  
  
<cfinvoke method="assertEquals">  
<cfinvokeargument name="expected" value="29" />  
<cfinvokeargument name="actual" value="#output#" />  
</cfinvoke>  
  
</cffunction>  
  
<cffunction name="testThirtyOneDayMonth" returntype="void"
access="public">  
<cfset var output="" />  
  
<standard:Days_In_Month month_id="5" year="2008"
returnvariable="output">  
  
<cfinvoke method="assertEquals">  
<cfinvokeargument name="expected" value="31" />  
<cfinvokeargument name="actual" value="#output#" />  
</cfinvoke>  
  
</cffunction>  
  
<cffunction name="testThirtyDayMonth" returntype="void" access="public">  
<cfset var output="" />  
  
<standard:Days_In_Month month_id="4" year="2008"
returnvariable="output">  
  
<cfinvoke method="assertEquals">  
<cfinvokeargument name="expected" value="30" />  
<cfinvokeargument name="actual" value="#output#" />  
</cfinvoke>  
  
</cffunction>  
  
<cffunction name="testFebruaryInNonLeapYear" returntype="void"
access="public">  
<cfset var output="" />  
  
<standard:Days_In_Month month_id="2" year="2007"
returnvariable="output">  
  
<cfinvoke method="assertEquals">  
<cfinvokeargument name="expected" value="28" />  
<cfinvokeargument name="actual" value="#output#" />  
</cfinvoke>  
  
</cffunction>  
  
<cffunction name="testLastMonthOfYear" returntype="void"
access="public">  
<cfset var output="" />  
  
<standard:Days_In_Month month_id="12" year="2008"
returnvariable="output">  
  
<cfinvoke method="assertEquals">  
<cfinvokeargument name="expected" value="31" />  
<cfinvokeargument name="actual" value="#output#" />  
</cfinvoke>  
  
</cffunction>  
  
  
</cfcomponent>  
  
```  
  
This is pretty straight forward based on the code I think. I basically just
import the customtag library using the setUp method and then test the specific
tag I'm interested in here. Now this custom tag just happens to have a
returnVariable. However, your custom tag might just output stuff directly. If
that is the case use the <cfsavecontent> tag to capture the output and
then run your assertions against the output like so  
  
```cfm  
  
<cffunction name="testPrintLastMonthOfYear" returntype="void"
access="public">  
<cfset var output="" />  
  
<cfsavecontent variable="output>  
<standard:Print_Days_In_Month month_id="12" year="2008">  
</cfsavecontent>  
<cfinvoke method="assertEquals">  
<cfinvokeargument name="expected" value="31" />  
<cfinvokeargument name="actual" value="#output#" />  
</cfinvoke>  
  
</cffunction>  
```

## Comments

jones

Nice blog...  
visit also [**coldfusion example**](http://coldfusion-example.blogspot.com/)

