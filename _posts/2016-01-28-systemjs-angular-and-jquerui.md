---
layout: post
title: "SystemJs Angular Jquery JqueryUi and Load Ordering"
description: Getting Angular UI Sortable to work in an Angular app using JSPM and SystemJs
headline:
date: 2016-01-28 16:10:13 -0500
category: development
tags: [angular,jspm,jquery,jqueryui,angular-ui,angular-ui-sortable]
imagefeature:
mathjax:
chart:
comments: true
featured: false
---
The title of this post really sucks but I couldn't think of anything clever.  Here is the situation I had though.

I am working on a pretty big angular 1.x application.  Within the scope of that project I am using JSPM (0.16.25) and SystemJS (0.19.17) (to load all the javascript dependencies.  I am also using JQuery and JQuery UI.  I need to have JQuery and JQuery UI loaded before some other things but I wasn't entirely sure how to do that.


When you use JSPM you get a file called config.js that has your system configuration in it.  That config is used by SystemJs to do a bunch of stuff; one of which is to tell it what javascript packages to load and, helpfully enough, what order, if necessary, to load the in.

I am using angular-ui-sortable for some drag and drop functionality on lists.  angular-ui-sortable reuqires that JqueryUi be loaded and JqueryUi requires Jquery to be loaded.  Here is how I solved that particular problem.

```js
System.config({
  baseURL: "/",
  transpiler: "babel",
  babelOptions: {
    "optional": [
      "runtime"
    ],
    "stage": 0
  },
  paths: {
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*"
  },
  buildCSS: true,
  meta: {
    'angular-ui-sortable': {
      deps: [
        'jquery',
        'jqueryui'
      ]
    }
  },
  map: {
    "jquery": "npm:jquery@2.2.0",
    "jqueryui": "github:components/jqueryui@1.11.4",
    "angular-ui-sortable": "npm:angular-ui-sortable@0.13.4",
  }
});
```

The `meta` element was the key.  Fortunately, I am able to use the mapped name for angular-ui-sortable in meta.  

There is a lot more in my `map` but I cut the rest out for simplicity.
