---
layout: single
title: "Let's Encrypt"
intro:
category: blogging
tags: [website,github-pages]
comments: false
featured: false
---

I use a droplet to host some, mainly, apache redirects at this point.  IT has some SSL certs managed via Lets Encrypt which is awesome. I was using the snapd install of certbot but that stopped working so I had to switch to the python version.

To remove the old one I had to manually delete a directory, then delete a link in the /usr/bin directory before I could successfully follow the install instructions.

It seems to be working.  Hopefully I can stop mucking about with this stuff soon.