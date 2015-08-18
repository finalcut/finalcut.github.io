---
layout: post
title: "Introducing ColdJack - a Coldfusion Wrapper to Jackcess"
description: Jackcess is a Java library for interacting with MS Access. ColdJack makes Jackcess a little easier to use from Coldfusion
headline:
modified: 2015-08-18 15:05:13 -0400
category: coldfusion,access,java,jackcess
tags: []
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
Earlier today I wrote [a brief post on using Jackcess](/2015/08/using-jackcess-to-read-access-files-with-coldfusion.html) - a java library for manipulating MS Access databases.  Now I'm following that up with a new Coldfusion component I call "[ColdJack](https://github.com/finalcut/coldjack)" that is a wrapper cfc for [Jackcess](http://jackcess.sourceforge.net/).  It basically builds on the simple concept I talked about earlier (reading in the contents of an Access table into a cf query object).

If I end up needing it to do more (or if there seems to be demand beyond just me) then I'll expand the capabilities to do other things.

Anyway, you can read all about it and it's usage at [its' github repository](https://github.com/finalcut/coldjack).

I suspect demand for this will be next to null but it was still fun to write.


For more information on Jackcess visit that [projects home page at sourceforge](http://jackcess.sourceforge.net/).
