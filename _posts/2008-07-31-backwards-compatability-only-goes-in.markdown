---
layout: post
title: "Backwards Computability Only Goes In One Direction"
date: 2008-07-31
comments: false
categories:
 - stupid mistakes
---
This is just a little story of a stupid moment by me. This morning I was
working on some stuff for a client when a weird error popped up. The error
occurred after I had updated the client library side of a client server pair
to be at version 2; the server, however, is at version 1.3.  
  
Version 2 is supposed to be backwards compatible with 1.3 but it wasn't
working. It seemed crazy; I even asked someone else to look at it and he too
was stumped. From the subject line you have probably already identified the
problem. The Server side is backward compatible with clients running 1.3.
There is no way the server, which was running 1.3, could be forward compatible
with 2.0 clients. Duh.  
  
I'm such a moron sometimes.

