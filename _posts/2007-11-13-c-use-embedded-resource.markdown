---
layout: post
title: "C#: Use Embedded Resource"
date: 2007-11-13
comments: false
categories:
 - embedded
 - xml
 - c#
 - stream
 - resource
 - filestream
---
I recently had the need to embed a few xml files into a project and wanted to
write a wrapper class that would deal with these embedded resources. I'm lazy
though and didn't want much cruft around them so I wanted a very simple method
for getting the resource and returning it as an XmlDocument - or null if it
wasn't found.

My other code will use the XmlDocument or not even show a form field if the
returned value is null.

**I made some minor changes to the following code so that you can see what references I'm using and I'm getting the Assembly via reflection now.**

Here is the code for fetching the resource:

```c#
using System.Reflection;
using System.IO;
using System.Xml;

public XmlDocument GetResource(string resourceCode)
{
XmlDocument xml = null
try
{
string filePath = "Com.MyDomain.MyProject.Resources" + resourceCode + ".xml";
Stream fileStream =
Assembly.GetExecutingAssembly().GetManifestResourceStream(filePath);
if (fileStream != null)
{
xml = new XmlDocument();
xml.Load(fileStream);
}

}
catch {
// if anything goes wrong I don't care - just return a null object.
}

return xml;
}

```


## Comments

abatishchev

Thanks!

Anonymous

how to save an xml which is stored as an embedded resource in my project..

Anonymous

Totally awesome post! Was looking all over for this. Thanks!

B-dizzle

Sweet!!! Exactly the example I'm looking for up here in MD.

**P**etros

This is **exactly** what I needed :)

@Ste

very nice, thank you!

