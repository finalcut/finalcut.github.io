---
layout: post
title: "PHP: Zend Framework"
date: 2007-03-14
comments: false
category: php
tags: [wordpress,picasa,picasaweb]
---
Anyone who reads this blog on any occasion will know that I jump around from
language to language quite a bit. So it should come as no surprise that I had
some PHP work to do yesterday. This, at least, was a personal project.  

I have a few plugins I have developed for the wordpress blogging platform and
one, the PicasaWeb plugin had stopped working because Google had changed the
structure of their ATOM feed that I was using. No biggie I figured, I'll just
make a minor update to the code and be done with it. Not so fast!  

It turns out Magpie (the rss/atom parser wordpress uses by default) was not
upto the task of handling these extra namespaces that Google was using. I
could have edited the core rss.php file (which I did temporarily) but as a
plugin author it really isn't my place to muck with core files instead I
needed to find a better solution.  

So I checked out some other rss/atom parsers; lastRSS but it doesn't do atom,
simpleRSS but it didn't really look like it was going to handle the "media"
namespace either, and then, finally, Zend_Feed a part of the Zend Framework.  

The Zend_Framework worked pretty well at pulling in the feeds and it is easy
to tell it to handle other namespaces - however, and I'm sure it is possible
if I had some more time, it doesn't do everything perfectly. For instance the
main "entity" node has an "id" node. The gphoto namespace also has an id node
- so Zend_Feed returns these as an array - however I have no idea how to
reference each element in the array in a way that would return the value. If
you have multiple links it uses the "rel" value so you can say
"$feed->link('relvalue'); to get back a specific href attribute of the link.
I'd love to know how to do this with the id (or any other element).  

In the end it wasn't a show stopper because I could just "explode" one of the
links to get the id value I needed. Explode is kind of like CF's "listToArray"
method where you specify a delimiter - in this case a forward slash (/).  

I ended up paring the Zend Framework down to the barest essential files I
needed (the framework itself is quite large) so hopefully my instance of the
Zend Framework won't end up breaking some other plugin (that I am presently
unaware of) that also uses the Zend_Framework.  

If you use wordpress and want to take a look at the plugin you can find it on
my non-tech blog: [rawlinson.us](http://rawlinson.us/blog/articles/picasaweb-
wordpress-plugin/).  

Another bright spot of the process was using OpenOffice to write the
readme.txt. For once I wrote it as a full .odt document and then exported as
PDF. The PDF export was great and, because I used structural markup (headings)
in my document the PDF contains "bookmarks" to help you jump to the four main
sections of the readme document. It is pretty cool (and is available in the
zip file with the plugin).
