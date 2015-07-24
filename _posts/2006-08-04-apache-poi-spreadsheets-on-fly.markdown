---
layout: post
title: "Apache POI - Spreadsheets on the FLY"
date: 2006-08-04
comments: false
categories:
 - coldfusion
 - java
 - poi
---
Using CF 6.1 I have a task where I need to export a bunch of data to an excel
spreadsheet. Not wanting to use the html table with cfcontent headers method
for streaming the excel data to the browser I decided to dive into the pond
with Apache Poi. Thanks to some blog posts by [Dave
Ross](http://www.d-ross.org/index.cfm?objectid=9C65ECEC-
508B-E116-6F8A9F878188D7CA) and [Christian Cantrell](http://weblogs.macromedia
.com/cantrell/archives/2003/06/using_coldfusio.cfm) I was able to build my
spreadsheet pretty quickly AND stream the contents to the user without having
to create a spreadsheet on the server's filesystem.  
  
I'm not going to go into much detail on creating the spreadsheet since Dave's
post goes into that with great detail. However, I did have to add a touch of
new logic to Christian's streaming solution in order to get it to work.  
  
The following function is a method within a "ExcelWriter" wrapper CFC I have
for working with POI - just so my code elsewhere isn't muddied up with java
calls.  
  
```cfm  
<cffunction access="public" output="true" name="stream" returntype="void"
hint="writes the spreadsheet to a bytearray output stream">  
<cfset var o = "" />  
<cfset var book = getBook() />  
<cfset var context = "" />  
<cfset var response = "" />  
<cfset var outStream =
createObject("java","java.io.ByteArrayOutputStream").init()/>  
<cfset var len = 0 />  
  
<cfset book.write(outStream) />  
<cfscript>  
book.write(outStream);  
len = arrayLen(outStream.toByteArray());  
outStream.flush();  
outStream.close();  
  
context = getPageContext();  
context.setFlushOutput(false);  
// must call getResponse twice to get to the correct output stream (otherwise
it is a character output stream which will corrupt my binary data)  
response = context.getResponse().getResponse();  
out = response.getOutputStream();  
response.setContentType("application/vnd.ms-excel");  
response.setContentLength(len);  
book.write(out);  
out.flush();  
out.close();  
</cfscript>  
</cffunction>  
```  
  
I'll be the first to admit that there may be a better way to get the length of
the spreadsheet bytearray. But this is the only way I know to do it. If I
didn't determine the byte array length then JRUN kind of hangs up if I try
another request after the excel was streamed (unless I close the requesting
browser). I think, if you fail to provide a contentLength value to the
response stream that it just keeps on streaming until it either times out or
the request is killed (browser close).

