---
layout: post
title: "Monitor Your Java Heap on the Fly"
date: 2010-11-05
comments: false
categories:
 - coldfusion
 - java
 - memory
 - heap
---
This sample code will be in ColdFusion as that was where I decided to test it.
However, it can obviously be used within a Java app if you wanted.

I'm not going to get into the pros and cons of manually calling the garbage
collector but feel free to hash it out in the comments.

Anyway, here is how you check your currently used Heap and, if you want, how
you call the garbage collector.




```cfc
<cffunction name="cleanGC">

 <cfset var rt = createObject("java","java.lang.Runtime") />

 <cfset var used = rt.getRunTime().totalMemory()  - rt.getRuntime().freeMemory() />

 <cfset var half = rt.getRunTime().totalMemory()/2/>

 <cfif used GT (half)><!--- more than half as many megs as are available being used? Clean up if we can --->

  <!--- call garbage collection --->

  <cfset rt.getRunTime().gc() />

 </cfif>

</cffunction>


```



It's pretty straight-forward really.  Use at your own risk.





## Comments











Bill






Thanks Larry. I'll fix it as soon as im at a real computer











Bill






Thanks Larry. I'll fix it as soon as im at a real computer











Larry C. Lyons






I saw a very minor issue in your code, you repeat the <cffunction line twice.


other than that nice post.


regards,

larry










