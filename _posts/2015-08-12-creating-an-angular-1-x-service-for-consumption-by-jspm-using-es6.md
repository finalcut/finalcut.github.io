---
layout: post
title: "Creating an Angular 1.x Service for Consumption by JSPM using ES6"
description:
headline:
modified: 2015-08-12 19:18:32 -0400
category: personal
tags: [angular,jspm,ecmascript6]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
My coworker Jason and I have been working on a [Angular 1.x](https://angularjs.org/) application that we've been writing using [ES6](http://es6-features.org/) and compiling into standard EcmaScript using [Babel](https://babeljs.io/) via a gulp build task.  I was doing a minor review of some of our work and decided to extract two of the Angular services into their own repositories as they are sufficiently generic enough that we could use them on other projects.

The two services are a [caching service](https://github.com/StrictlyBusiness/angular-cache-service) which caches model objects that have been pulled down from our api server, and a [referential data service](https://github.com/StrictlyBusiness/angular-referential-data-service) which intelligently fetches referential objects based on a little bit of configuration in our model-services definition.  I'm  not really going to get into explaining how they both work here but rather I want to talk about a caveat I ran into while extracting these services into their own repositories and then attempting to consume them via our main application using [JSPM](http://jspm.io/).

For the rest of this article I'll mostly talk about the caching service as the unit test for the referential data service actually makes use of the caching service to do a little advanced testing.  

When creating the repo for the caching service I did the standard `npm init` and then edited the resulting packages.json file to tell identify the main like so:

```js
"main": "cache-service.js",
```
The cache-service.js file is written in ES6 so looks a little differently than most other angular service examples; but I figured since it worked okay calling it directly from our older parent project that this would work fine and proceeded to push everything up to github.  However, when I later tried to use this package via JSPM the file created by JSPM that points to the actual code looked sort of like this:

```js
import * from github:StrictlyBusiness/angular-cache-service@master
```

Typically the jspm files look more like this:

```js
module.exports = require("github:StrictlyBusiness/angular-cache-service@master");
```

I didn't think anything of it until I tried to use the CacheService to create a new instance. Here is the relevant ES6 syntax from the referential data service unit test:

```js
import CacheService from 'angular-cache-service';
  ...

  let cacheService = new CacheService();
  ...
```

The CacheService import was undefined.  Interestingly, if I just had the cache-service.js file local and imported it exactly the same the CacheService import was a function (as I expected it to be).

Jason and I both figured the odd jspm file format of `import * ...` was probably just caused because our source file was a different format and that the jspm file was correct.  However, I had a hunch that maybe JSPM didn't like our ES6 at all.  I then went back to the cache service and added a compile step using Babel which generates a very differently formatted file in dist/cache-service.js.

I then updated the package.json file to point main to this copy:

```js
"main": "dist/cache-service.js",
```

And pushed back to github.  Then I re-installed the angular-cache-service using JSPM in the referential data service and everything worked as expected.  And, now, the jspm file looks like so:

```js
module.exports = require("github:StrictlyBusiness/angular-cache-service@0.0.4/dist/cache-service");
```

**NOTE: I'm not pointing at master anymore but at an actual verion tag.  The first three point relases didn't work and it took me a while to think of pointing at master  while testing

TL/DR: Compile your ES6 code and point main at the resultant compiled file if you want to resue it via JSPM.
