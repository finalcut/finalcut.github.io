---
layout: post
title: "CFC Webservice and C#"
date: 2007-06-27
comments: false
category: [coldfusion,c#]
tags: [webservices]
---
So here I am working on yet another project, this one integrates a ColdFusion
website with a tablet PC based app written in C#. The CF side needs to expose
a few things via webservices since it is the master of all data. On the
surface this seems pretty straight forward. But is it?

In Visual Studio 2005 you can add a Web Reference to your project and it will
build a nifty little proxy class to your webservice. Very neat. But sometimes
VS fails to create the proxy class even when it can find the webservice. What
gives?

For instance, I created a webservice that is responsible for sending out
updates to all of the referential data the client apps will be using (so they
will work in a disconnected environment later). I figured the best format for
all of this data would be an XML document so I built a big string, had CF
parse it into an XML document and then returned it from my webservice. The
thing is though that VS couldn't create the proxy. It gave me a really useless
error message about wsdlSoap which made me think maybe, just maybe, my wsdl
file was whacked. It wasn't, well not exactly, but it at least got me moving
in the right direction.

Next I tried the handy command line tool in the VS/Bin directory called
"wsdl.exe". It still failed but it gave me a bit more to go on. Specifically
the error:





```
Error: Unable to import binding 'foo.cfcSoapBinding' from n

  - Unable to import operation 'FetchReferentialData'.

  - The datatype 'http://xml.apache.org/xml-soap:Document' is missing.


```






When I went back and reexamined the wsdl created by my "foo.cfc" I saw that it was indeed referencing this http://xml.apache.org stuff and I honestly didn't know why the Visual Studio tools were having issues with it.  So, just out of curiosity I decided to send the XML document back as a simple string (serialized the XML basically) and voila' what do you know? It worked.  I was able to crank out the proxy class from the wsdl tool and from within Visual Studio.


It seems this is a known limitation of the interaction between these two technologies.  C# can't really handly any kind of complex entity being returned from the ColdFusion webservice.  This doesn't really surprise me - how could it possibly map a CF Query Object to a C# anything?  Maybe it can in CF 8 with the .net integration (know how to deserialize a CF Query object) but I'd be surprised unless your .net project had a reference to some C# coldfusion classes - I seriously doubt they (Adobe) are converting the query object on the server side to a "standard" C# class, serializing it, and then sending that out.


The point of this post really isn't to shed new light on a topic (it has been covered before) but to hopefully shine that light at some new people who haven't dealt with this before.  I hope it saves someone some time.





## Comments











David Garthe






Came across the same problem.  Seems c# has a problem when the returntype is "xml".  We solved the problem by changing the returntype to "string", and returned the same xml doc.  The c# system was then able to ingest the web service correctly.











Anonymous






Bill,


Nice topic. I am doing the exact thing now and am having issues. So I understand that you cannot return a query, but I would like to provide simple updates using webservices. When you said you serialized the xml, what were you referring to.


I went in and added a web reference and pointed to mycfc.cfc?wsdl...


the error reads:

The document at the url http://inside2dev.mdanderson.org/dept/atc/webservices/timePointProvider.cfc?wsdl was not recognized as a known document type.

The error message from each known type may help you fix the problem:

- Report from 'DISCO Document' is 'DTD is prohibited in this XML document.'.

- Report from 'WSDL Document' is 'There is an error in XML document (0, 0).'.

  - DTD is prohibited in this XML document.

- Report from 'XML Schema' is 'The root element of a W3C XML Schema should be schema and its namespace should be 'http://www.w3.org/2001/XMLSchema'.'.
