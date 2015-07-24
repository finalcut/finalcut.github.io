---
layout: post
title: "C# : Parsing a URL for its Component Parts"
date: 2008-07-17
comments: false
categories:
 - http
 - uri
 - url parsing
 - c#
 - url-parsing
---
I recently had need to break a URL down to it's component pieces so that I
could use just those parts that I needed at different times. My initial
approach to solving this problem was to Google for a built in solution to
parsing URLs in C# but I couldn't find one. So then I feel back to a RegEx
pattern. .Net in general has some nice regex features (including being able to
name groups) and so this is the RegEx I came up with (after looking at some
others that already existed):


```c#
private static Regex pattern = new Regex("(?<protocol>http(s)?|ftp)://(?
<server>([A-Za-z0-9-]+\\\\.)*(?<basedomain>[A-Za-z0-9-]+\\\\.[A-Za
-z0-9]+))+((:)?(?<port>[0-9]+)?(/?)(?<path>(?<dir>[A-Za-z0-9
\\\\._\\\\-]+)(/){0,1}[A-Za-z0-9.-/]*)){0,1}");

```


However, that RegEx has a problem where it won't get the full Port number if
the port is immediately followed by a query like so:
http://my.domain.com:8000?arg1=this&amp;arg2=that

Instead of returning the port of 8000 the regex ends up with the port of 8.
That sucks. Fortunately, I know someone else who I could ask about it and he
pointed me at the useful built in C# library : System.Uri.

Why this library didn't pop up in my Google queries I don't know but, let me
tell you, it does pretty much everything I need. However, I do have one minor
quibble. The protocol portion of the URL is parsed out and identified by
Scheme.

Now, with a string based representation of a URL I can break it down quickly
using the System.URI class. Lets say you want to get the port:


```c#
string url = "http://my.domain.com:8000?arg1=this&amp;arg2=that";
System.Uri uri = new System.Uri(url);

// get the port
int port = uri.Port;

// get the host name (my.domain.com)
string host = uri.Host;

// get the protocol
string protocol = uri.Scheme;

// get everything before the query:
string cleanURL = uri.Scheme + "://" +
uri.GetComponents(UriComponents.HostAndPort, UriFormat.UriEscaped);

```


As you can imagine there is actually a lot you can do. If you don't think you
can find a bit from the URL check out that uri.GetComponents method - the
UriComponents enumeration has a bunch of options you can dig into!

