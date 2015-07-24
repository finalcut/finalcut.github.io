---
layout: post
title: "QuickSort"
date: 2006-12-19
comments: false
categories:
 - quicksort
 - algorithms
 - sorting
---
I was reading an [article on sorting algorithms](http://yagni.com/combsort/)
today and thought, "Hrm, I wonder how well CF compares to these others when
running a hand written QuickSort."

The answer, not very good - however, the good news is that it isn't really
important considering the built in array sorting method is VERY fast, even for
large datasets (10,000 elements).

I gave up waiting on CF to finish the QuickSort for 10,000 elements but for
just 1,000 it took over 4 seconds on average - with the built in sort the time
was not-measurable.

Here is the QuickSort Algorithim I used:


```cfc
<cffunction name="partition" returntype="struct">
<cfargument name="a" type="array" />
<cfargument name="first" type="numeric" />
<cfargument name="last" type="numeric" />

<cfset var pivot = arguments.a[arguments.first] />
<cfset var lastS1 = arguments.first />
<cfset var firstUnknown = arguments.first+1 />
<cfset var s = structNew() />

<cfloop condition="firstUnknown LTE arguments.last">
<cfif a[firstUnknown] LT pivot>
<cfset lastS1 = lastS1 + 1 />
<cfset arraySwap(arguments.a,firstUnknown,lastS1) />
</cfif>
<cfset firstUnknown = firstUnknown + 1 />
</cfloop>

<cfset arraySwap(arguments.a,arguments.first,lastS1) />

<cfset s.s1 = lastS1 />
<cfset s.a = arguments.a />
<cfreturn s />

</cffunction>

<cffunction name="quicksorter" returntype="array">
<cfargument name="a" type="array">
<cfargument name="first" type="numeric">
<cfargument name="last" type="numeric">

<cfset var pivotInfo = StructNew() />

<cfif arguments.first LT arguments.last>

<cfset pivotInfo = partition(a,arguments.first,arguments.last) />
<cfset arguments.a = pivotInfo.a />
<cfset arguments.a =
quicksorter(arguments.a,arguments.first,pivotInfo.s1-1) />
<cfset arguments.a = quicksorter(arguments.a,pivotInfo.s1+1,arguments.last)
/>
</cfif>

<cfreturn a />
</cffunction>

<cffunction name="quicksort" returntype="array">
<cfargument name="a" type="array" />
<cfargument name="size" type="numeric" />

<cfreturn quicksorter(arguments.a,1,arguments.size) />
</cffunction>

```


You can call it like so. This can be used to sort smaller portions of the
array if you want.

```cfc
<cfset l1 = quicksort(l1,arrayLen(l1)) />

```


The linked article has a couple of other sorting algorithms you can look at
and has them implemented in many languages (just not CF). CF, however, is best
not included in the conversation with languages like C++ which completes the
quicksort on 10,000 elements in 0.0038 seconds.

