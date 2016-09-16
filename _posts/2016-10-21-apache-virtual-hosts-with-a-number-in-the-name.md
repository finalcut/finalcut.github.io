---
layout: post
title: "Apache Virtual Hosts With a Number In the Name"
description:
headline:
date: 2016-10-21 13:35:27 -0400
category: development
tags: [apache,virtual-hosts]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
I'm mostly hoping someone can comment on this with some guidance to explain why my apache configuration for a virtual host didn't work.

I'm on a dev machine using Apache webserver v2.4 on windows 10.  I created a virtual host called warp2016.com like so:

```aconf
<VirtualHost 127.0.0.1:80>
    DocumentRoot "c:/dev/websites/wcs2016/site/"
    ServerAdmin nobody@nowhere.com
    ServerName warp2016.com
    ServerAlias *.warp2016.com
    ErrorLog c:/dev/websites/wcs2016/log/server.log
</VirtualHost>
```

I also have a hosts entry for warp2016 that points to 127.0.0.1; however, whenever I try to hit warp2016.com I get the default directory index and not the one specified by this `DocumentRoot`

If I change the host entry and the domain name info in the virtual host to warptest it works fine:

```aconf
<VirtualHost 127.0.0.1:80>
    DocumentRoot "c:/dev/websites/wcs2016/site/"
    ServerAdmin nobody@nowhere.com
    ServerName warptest.com
    ServerAlias *.warptest.com
    ErrorLog c:/dev/websites/wcs2016/log/server.log
</VirtualHost>
```

I have a few different virutal hosts, all with just alpha characters in the name and they all work fine (all on 127.0.0.1) but for some reason when I added the numbers to the domain name it failed to work.
