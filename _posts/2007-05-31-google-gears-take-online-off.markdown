---
layout: post
title: "Google Gears - Take the online off"
date: 2007-05-31
comments: false
category: javascript
tags: [google,gears,localstorage]
---
Google has released a new beta product called "Google Gears" which looks to be
a really slick JavaScript API that will allow you to take dynamic website
applications and give them an off line instance. This way users can work in a
disconnected state and then, when back online, resynchronize their data.

Gears contains three components:


LocalServer


Cache and serve application resources (HTML, JavaScript, images, etc.) locally

Database


Store data locally in a fully-searchable relational database

WorkerPool


Make your web applications more responsive by performing resource-intensive operations asynchronously



The offline version is updated automatically everytime a user reconnects so
long as the online versions "manifest.json" file has it's version number
properly incremented.

Overall it looks really slick and I can't wait to dig into it a bit. You can
check it out at <http://gears.google.com>
